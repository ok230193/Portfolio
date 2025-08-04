import React, { useEffect, useMemo, useRef, useState } from 'react';
import { Link } from 'react-router-dom';
import PRICE_MAP, { toJPY } from './PriceMap';

const API = 'http://localhost:3001';
const SHIPPING_FEE = 660; // ← 送料

export default function CartPage() {
  const [items, setItems] = useState([]);     // [{ID, product, qty}]
  const [loading, setLoading] = useState(true);
  const [showPay, setShowPay] = useState(false);
  const [paid, setPaid] = useState(false);
  const [purchased, setPurchased] = useState(false);   // 購入完了フラグ

  // お届け先情報
  const [customer, setCustomer] = useState({
    name: '',
    address: '',
    phone: '',
    cardNumber: '',
    cardName: '',
    cardExp: '',
    cardCvc: '',
  });

  // 「購入完了画面でのカート消去」を二重実行しないためのフラグ
  const clearedRef = useRef(false);

  const fetchCart = async () => {
    setLoading(true);
    try {
      const res = await fetch(`${API}/api/cart`);
      const data = await res.json();
      setItems(Array.isArray(data) ? data : []);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };
  useEffect(() => { fetchCart(); }, []);

  const rows = useMemo(() => {
    return items.map((it) => {
      const price = PRICE_MAP[it.product] ?? 0;
      return { ...it, price, subtotal: price * Number(it.qty || 0) };
    });
  }, [items]);

  const itemsTotal = useMemo(
    () => rows.reduce((acc, r) => acc + r.subtotal, 0),
    [rows]
  );
  const hasItems = rows.length > 0;
  const grandTotal = hasItems ? itemsTotal + SHIPPING_FEE : 0;

  const removeOne = async (product) => {
    try {
      const res = await fetch(`${API}/api/cart/remove`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ product, qty: 1 }),
      });
      if (!res.ok) throw new Error('削除に失敗しました');
      fetchCart();
    } catch (e) {
      alert(e.message);
    }
  };

  const removeAll = async (product, qty) => {
    try {
      await fetch(`${API}/api/cart/remove`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ product, qty }),
      });
    } catch (e) {
      console.error(e);
    } finally {
      fetchCart();
    }
  };

  // サーバのカートを空にする
  const clearCartOnServer = async () => {
    try {
      const res = await fetch(`${API}/api/cart/clear`, { method: 'POST' });
      if (!res.ok) {
        const t = await res.text().catch(() => '');
        console.error('clear failed', res.status, t);
      }
    } catch (e) {
      console.error('clear error', e);
    }
  };

  // 簡易バリデーション
  const validate = () => {
    if (!customer.name.trim()) return '氏名を入力してください';
    if (!customer.address.trim()) return '住所を入力してください';
    if (!/^[0-9+\-]{10,14}$/.test(customer.phone.replace(/\s/g, '')))
      return '連絡先はハイフン可・半角数字で入力してください';
    if (!/^[0-9 ]{12,19}$/.test(customer.cardNumber)) return 'カード番号を正しく入力してください';
    if (!customer.cardName.trim()) return '名義を入力してください';
    if (!/^[0-9]{2}\/[0-9]{2}$/.test(customer.cardExp)) return '有効期限は MM/YY 形式で入力してください';
    if (!/^[0-9]{3,4}$/.test(customer.cardCvc)) return 'CVCを正しく入力してください';
    return null;
  };

  // 購入ボタン→決済送信（見せかけ）
  const onSubmitPayment = (e) => {
    e.preventDefault();
    const err = validate();
    if (err) { alert(err); return; }

    setPaid(true);
    setTimeout(async () => {
      // 1) 先にサーバのカートを空に
      await clearCartOnServer();
      // 2) 画面上の状態を「購入完了」に
      setItems([]);
      setPurchased(true);
      setShowPay(false);
      setPaid(false);
      clearedRef.current = true;
    }, 1000);
  };

  // 念のため：purchased=true になった瞬間にもサーバへ消去要求
  useEffect(() => {
    if (purchased && !clearedRef.current) {
      clearedRef.current = true;
      clearCartOnServer();
    }
  }, [purchased]);

  const onChange = (key) => (e) => setCustomer((c) => ({ ...c, [key]: e.target.value }));

  return (
    <div className="main-wrapper">
      <div className="main cart-container">
        <div className="cart-header">
          <h2>カート</h2>
          <Link to="/" className="cart-link-btn">← 買い物を続ける</Link>
        </div>

        {purchased ? (
          // 購入完了画面のみを描画（テーブルは出さない）
          <div className="purchase-complete">
            <h3>購入が完了しました。</h3>
            <p>ありがとうございました！</p>
            <Link to="/" className="btn-buy">トップへ戻る</Link>
          </div>
        ) : (
          <>
            {loading && <p>読み込み中…</p>}

            {!loading && hasItems && (
              <>
                <table className="cart-table">
                  <thead>
                    <tr>
                      <th>商品名</th>
                      <th>単価</th>
                      <th>数量</th>
                      <th>小計</th>
                      <th></th>
                    </tr>
                  </thead>
                  <tbody>
                    {rows.map(r => (
                      <tr key={r.ID}>
                        <td>{r.product}</td>
                        <td>{toJPY(r.price)}</td>
                        <td>{r.qty}</td>
                        <td>{toJPY(r.subtotal)}</td>
                        <td className="cart-actions">
                          <button onClick={() => removeOne(r.product)} className="btn-sub">-1</button>
                          <button onClick={() => removeAll(r.product, r.qty)} className="btn-del">削除</button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>

                {/* 注文サマリー（商品合計 + 送料 + お支払い合計） */}
                <div className="order-summary">
                  <div className="row">
                    <span>商品合計</span>
                    <span>{toJPY(itemsTotal)}</span>
                  </div>
                  <div className="row">
                    <span>送料</span>
                    <span>{toJPY(SHIPPING_FEE)}</span>
                  </div>
                  <div className="row total">
                    <span>お支払い合計</span>
                    <span>{toJPY(grandTotal)}</span>
                  </div>
                </div>

                <div className="cart-actions-bottom">
                  <button className="btn-buy" onClick={() => setShowPay(true)}>
                    購入手続きへ
                  </button>
                </div>
              </>
            )}

            {/* カートが空のときは何も表示しない */}
          </>
        )}

        {/* 決済モーダル（見せかけ） */}
        {showPay && (
          <div className="modal">
            <div className="modal-inner">
              {paid ? (
                <p>決済処理中…</p>
              ) : (
                <>
                  <h3>お支払い</h3>

                  {/* お届け先情報 */}
                  <form onSubmit={onSubmitPayment} className="pay-form">
                    <fieldset className="ship-fieldset">
                      <legend>お届け先</legend>
                      <label>
                        氏名
                        <input
                          value={customer.name}
                          onChange={onChange('name')}
                          required
                          placeholder="山田 太郎"
                        />
                      </label>
                      <label>
                        住所
                        <textarea
                          value={customer.address}
                          onChange={onChange('address')}
                          required
                          rows={3}
                          placeholder="〒100-0001 東京都千代田区千代田1-1 ○○マンション101"
                        />
                      </label>
                      <label>
                        連絡先（ハイフン可）
                        <input
                          value={customer.phone}
                          onChange={onChange('phone')}
                          inputMode="tel"
                          pattern="[0-9+\-]{10,14}"
                          required
                          placeholder="090-1234-5678"
                        />
                      </label>
                    </fieldset>

                    {/* カード情報 */}
                    <fieldset className="card-fieldset">
                      <legend>カード情報</legend>
                      <label>
                        カード番号
                        <input
                          value={customer.cardNumber}
                          onChange={onChange('cardNumber')}
                          inputMode="numeric"
                          pattern="[0-9 ]{12,19}"
                          required
                          placeholder="4242 4242 4242 4242"
                        />
                      </label>
                      <label>
                        名義（ローマ字）
                        <input
                          value={customer.cardName}
                          onChange={onChange('cardName')}
                          required
                          placeholder="TARO YAMADA"
                        />
                      </label>
                      <div className="pay-row">
                        <label>
                          有効期限 (MM/YY)
                          <input
                            value={customer.cardExp}
                            onChange={onChange('cardExp')}
                            required
                            placeholder="12/29"
                          />
                        </label>
                        <label>
                          CVC
                          <input
                            value={customer.cardCvc}
                            onChange={onChange('cardCvc')}
                            inputMode="numeric"
                            pattern="[0-9]{3,4}"
                            required
                            placeholder="123"
                          />
                        </label>
                      </div>
                    </fieldset>

                    {/* 合計の確認 */}
                    <div className="pay-total">
                      <div>商品合計：{toJPY(itemsTotal)}</div>
                      <div>送料：{toJPY(SHIPPING_FEE)}</div>
                      <div className="grand">お支払い金額：{toJPY(grandTotal)}</div>
                    </div>

                    <div className="pay-actions">
                      <button type="button" onClick={() => setShowPay(false)}>キャンセル</button>
                      <button type="submit" className="btn-buy">購入する</button>
                    </div>
                  </form>
                </>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
