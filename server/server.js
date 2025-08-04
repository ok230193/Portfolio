// backend/server.js
const express = require('express');
const cors = require('cors');
const sqlite3 = require('sqlite3').verbose();
const path = require('path');

const app = express();
const PORT = 3001;

// === DB 接続（絶対パス + ログ）===
const DB_PATH = path.join(__dirname, 'zaikoTable', 'zaiko.sqlite3');
console.log('[DB] open =>', DB_PATH);
const db = new sqlite3.Database(DB_PATH);

// ロック対策
db.run('PRAGMA busy_timeout = 5000');
db.run('PRAGMA journal_mode = WAL');

app.use(cors());
app.use(express.json());

// === 起動時に cart を用意（無ければ作成） ===
db.run(`
  CREATE TABLE IF NOT EXISTS cart (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product TEXT UNIQUE,
    qty INTEGER NOT NULL DEFAULT 1
  )
`);
db.run(`CREATE UNIQUE INDEX IF NOT EXISTS idx_cart_product_unique ON cart(product)`);

// 正規化（後方互換：product名で叩かれてもOK）
const normalizeName = (s) => (s ?? '').toString().trim().normalize('NFC');

// ========== API ==========

// 在庫一覧
app.get('/api/products', (req, res) => {
  db.all('SELECT * FROM ZaikoTable', (err, rows) => {
    if (err) return res.status(500).json({ message: 'DB error' });
    res.json(rows);
  });
});

// カゴ一覧
app.get('/api/cart', (req, res) => {
  db.all('SELECT * FROM cart', (err, rows) => {
    if (err) return res.status(500).json({ message: 'DB error' });
    res.json(rows);
  });
});

// カゴに追加（在庫減算も実施）— productId 優先、無ければ product 名
app.post('/api/cart/add', (req, res) => {
  const { productId, product, qty = 1 } = req.body;
  const nQty = Number(qty);
  if (!Number.isFinite(nQty) || nQty <= 0) {
    return res.status(400).json({ message: 'qty(>0) が必要です' });
  }

  const whereSql = productId ? 'ID = ?' : 'product = ?';
  const whereVal = productId ? Number(productId) : normalizeName(product);

  db.serialize(() => {
    db.get(`SELECT ID, product, zaiko FROM ZaikoTable WHERE ${whereSql}`, [whereVal], (err, row) => {
      if (err) return res.status(500).json({ message: 'DB error(select)' });
      if (!row) return res.status(404).json({ message: '商品が見つかりません' });

      const current = Number(row.zaiko);
      if (!Number.isFinite(current)) return res.status(500).json({ message: '在庫データが不正です' });
      if (current < nQty) return res.status(409).json({ message: '在庫不足' });

      db.run('BEGIN', (eBegin) => {
        if (eBegin) return res.status(500).json({ message: 'TRX begin 失敗' });

        db.run('UPDATE ZaikoTable SET zaiko = zaiko - ? WHERE ID = ?', [nQty, row.ID], function (e1) {
          if (e1 || this.changes === 0) {
            return db.run('ROLLBACK', () => res.status(500).json({ message: '在庫更新エラー' }));
          }

          db.run(
            `INSERT INTO cart (product, qty) VALUES (?, ?)
             ON CONFLICT(product) DO UPDATE SET qty = qty + excluded.qty`,
            [row.product, nQty],
            function (e2) {
              if (e2) {
                return db.run('ROLLBACK', () => res.status(500).json({ message: 'カゴ更新エラー' }));
              }

              db.get('SELECT zaiko FROM ZaikoTable WHERE ID = ?', [row.ID], (e3, row2) => {
                if (e3 || !row2) {
                  return db.run('ROLLBACK', () => res.status(500).json({ message: '在庫再取得エラー' }));
                }
                db.run('COMMIT', (eCommit) => {
                  if (eCommit) return res.status(500).json({ message: 'TRX commit 失敗' });
                  res.json({ product: row.product, stock: Number(row2.zaiko) });
                });
              });
            }
          );
        });
      });
    });
  });
});

// カゴから削除（在庫を戻す）
app.post('/api/cart/remove', (req, res) => {
  const { productId, product, qty = 1 } = req.body;
  const nQty = Number(qty);
  if (!Number.isFinite(nQty) || nQty <= 0) {
    return res.status(400).json({ message: 'qty(>0) が必要です' });
  }

  const whereSql = productId ? 'ID = ?' : 'product = ?';
  const whereVal = productId ? Number(productId) : normalizeName(product);

  db.serialize(() => {
    db.get(`SELECT ID, product FROM ZaikoTable WHERE ${whereSql}`, [whereVal], (e1, prod) => {
      if (e1) return res.status(500).json({ message: 'DB error(select product)' });
      if (!prod) return res.status(404).json({ message: '商品が見つかりません' });

      db.get(`SELECT qty FROM cart WHERE product = ?`, [prod.product], (e2, c) => {
        if (e2) return res.status(500).json({ message: 'DB error(select cart)' });
        if (!c || Number(c.qty) <= 0) return res.status(404).json({ message: 'カートに商品がありません' });

        const removeQty = Math.min(Number(c.qty), nQty);

        db.run('BEGIN', (eBegin) => {
          if (eBegin) return res.status(500).json({ message: 'TRX begin 失敗' });

          db.run(`UPDATE cart SET qty = qty - ? WHERE product = ?`, [removeQty, prod.product], function (eU) {
            if (eU || this.changes === 0) {
              return db.run('ROLLBACK', () => res.status(500).json({ message: 'カート更新エラー' }));
            }

            db.run(`DELETE FROM cart WHERE product = ? AND qty <= 0`, [prod.product], (eDel) => {
              if (eDel) {
                return db.run('ROLLBACK', () => res.status(500).json({ message: 'カート削除エラー' }));
              }

              db.run(`UPDATE ZaikoTable SET zaiko = zaiko + ? WHERE ID = ?`, [removeQty, prod.ID], function (eZ) {
                if (eZ || this.changes === 0) {
                  return db.run('ROLLBACK', () => res.status(500).json({ message: '在庫更新エラー' }));
                }
                db.run('COMMIT', (eC) => {
                  if (eC) return res.status(500).json({ message: 'TRX commit 失敗' });
                  res.json({ product: prod.product, removed: removeQty });
                });
              });
            });
          });
        });
      });
    });
  });
});

// ★ カートの中身を全削除（購入完了時に使用）— 可視化ログ & 残件数返却
app.post('/api/cart/clear', (req, res) => {
  console.log('[API] POST /api/cart/clear called');
  db.serialize(() => {
    db.run('BEGIN');
    db.run('DELETE FROM cart', function (err) {
      if (err) { db.run('ROLLBACK'); return res.status(500).json({ ok:false, message:'cart clear error' }); }
      const deleted = this.changes;
      db.run('COMMIT', (e) => {
        if (e) return res.status(500).json({ ok:false, message:'commit error' });
        db.get('SELECT COUNT(*) AS remaining FROM cart', (e2, row) => {
          console.log('[API] cart cleared. deleted =', deleted, 'remaining =', row?.remaining);
          res.json({ ok:true, deleted, remaining: row?.remaining ?? -1 });
        });
      });
    });
  });
});

// =========================
app.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
});
