import React, { useState, useEffect } from 'react';
import { toJPY } from './PriceMap';

function Lesson({ id, name, image, introduction, stock, price = 0, apiBase = '' }) {
  // 表示用の在庫
  const [localStock, setLocalStock] = useState(0);
  const [loading, setLoading] = useState(false);
  const [justAdded, setJustAdded] = useState(false); // 追加完了表示

  useEffect(() => {
    const n = Number(stock);
    setLocalStock(Number.isFinite(n) ? n : 0);
  }, [stock]);

  const isSoldOut = localStock <= 0;

  const handleAddToCart = async () => {
    if (isSoldOut || loading) return;
    setLoading(true);
    try {
      const url = `${apiBase}/api/cart/add`;
      const body = id ? { productId: id, qty: 1 } : { product: name, qty: 1 };
      const res = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
      });
      const data = await res.json().catch(() => ({}));
      if (!res.ok) throw new Error(data.message || '追加に失敗しました');

      // サーバが返す最新在庫
      setLocalStock(Number.isFinite(Number(data.stock)) ? Number(data.stock) : localStock - 1);

      // 「追加しました」を一時表示
      setJustAdded(true);
      setTimeout(() => setJustAdded(false), 1500);
    } catch (e) {
      alert(e.message || 'サーバーに接続できませんでした');
    } finally {
      setLoading(false);
    }
  };

  return (
    <article className={`lesson-card ${isSoldOut ? 'soldout' : ''}`}>
      <div className="lesson-item">

        {/* 売り切れバナー */}
        {isSoldOut && (
          <>
            <div className="soldout-overlay"><span>すみません。　品切れです。</span></div>
            <span className="soldout-ribbon">売り切れ</span>
          </>
        )}

        <h4 className="lesson-title">{name}</h4>

        <div className="image-wrap">
          <img src={image} alt={name} />
        </div>

        {/* 価格表示 */}
        <p className="price">{toJPY(price)}</p>

        {/* 在庫表示 */}
        <p className="stock">{isSoldOut ? '在庫数：0（売り切れ）' : `在庫数：${localStock}`}</p>

        {/* 紹介文 */}
        <p className="intro">{introduction}</p>

        {/* 追加ボタン */}
        <button
          className="add-btn"
          onClick={handleAddToCart}
          disabled={isSoldOut || loading}
          aria-disabled={isSoldOut || loading}
        >
          {isSoldOut ? '売り切れ' : loading ? '追加中…' : 'カゴに追加'}
        </button>

        {/* 追加完了メッセージ */}
        {justAdded && <p className="notice ok">カートに追加しました！</p>}
      </div>
    </article>
  );
}

export default Lesson;
