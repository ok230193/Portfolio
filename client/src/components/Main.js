import React from 'react';
import { Link } from 'react-router-dom';
import Lesson from './Lesson';
import PRICE_MAP from './PriceMap';

// 画像のインポート
import orvenImage from '../image/orven.png';
import coffeeImage from '../image/coffee.png';
import denkiImage from '../image/denki.png';
import hedohonImage from '../image/hedhon.png';
import pcImage from '../image/PC.png';
import senpukiImage from '../image/senpuki.png';
import sentakukiImage from '../image/sentakuki.png';
import suihankiImage from '../image/suihanki.png';
import tabletImage from '../image/tablet.png';
import tvImage from '../image/TV.png';

// 在庫APIのURL
const API_URL = 'http://localhost:3001/api/products';

class Main extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      stockData: [], // ZaikoTable の行（ID, product, zaiko）
      loading: true,
      error: null,
    };
  }

  componentDidMount() {
    fetch(API_URL)
      .then((res) => {
        if (!res.ok) throw new Error('Network response was not ok');
        return res.json();
      })
      .then((data) => {
        const normalized = data.map((row) => ({
          ...row,
          zaiko: isNaN(Number(row.zaiko)) ? row.zaiko : Number(row.zaiko),
        }));
        this.setState({ stockData: normalized, loading: false });
      })
      .catch((err) => {
        console.error('Fetch error:', err);
        this.setState({ error: err.message, loading: false });
      });
  }

  // product 名→在庫数
  getStockByName = (productName) => {
    const m = this.state.stockData.find((item) => item.product === productName);
    return m ? m.zaiko : null;
  };

  // product 名→ID（サーバに productId を渡せるように）
  getIdByName = (productName) => {
    const m = this.state.stockData.find((item) => item.product === productName);
    return m ? m.ID : null;
  };

  render() {
    const { loading, error } = this.state;

    const lessonList = [
      { name: 'オーブン',        image: orvenImage,
        introduction: 'パンや料理をふっくら焼き上げる、毎日の食卓をワンランクアップさせるオーブンです！' },
      { name: 'コーヒーメーカー', image: coffeeImage,
        introduction: '挽きたての香りと味わいをご自宅で！忙しい朝も、ゆったりした午後も贅沢な一杯を！' },
      { name: '電気スタンド',    image: denkiImage,
        introduction: 'やさしい灯りで、デスクやベッドサイドを快適に！空間をおしゃれに演出する電気スタンド。' },
      { name: 'ヘッドホン',      image: hedohonImage,
        introduction: '迫力のサウンドで、音楽も映画も没入体験。ワイヤレスでストレスフリーに楽しめます！' },
      { name: 'パソコン',        image: pcImage,
        introduction: '仕事もエンタメも快適にこなす、高性能でスタイリッシュなノートパソコンです！' },
      { name: '扇風機',          image: senpukiImage,
        introduction: '優しい風で心地よく涼しく！デザインもシンプルで、どんな部屋にもなじみます。' },
      { name: '洗濯機',          image: sentakukiImage,
        introduction: '大容量＆節水設計！忙しい毎日でも、しっかり汚れを落とす頼れる味方です。' },
      { name: '炊飯器',          image: suihankiImage,
        introduction: 'お米本来の甘みと旨味を引き出します。毎日食べたくなるふっくらごはんを！' },
      { name: 'タブレット',      image: tabletImage,
        introduction: '持ち運び自由！仕事も遊びもこれ一台。鮮やかな画面で動画も快適。' },
      { name: 'テレビ',          image: tvImage,
        introduction: '映画やスポーツを大画面で楽しめます。高画質・高音質で臨場感たっぷり！' },
    ];

    return (
      <div className="main-wrapper">
        <div className="main">
          <div className="copy-container">
            <h1>家電.com.</h1>
            <h2>あなたの日常にすこしの「便利」を。</h2>
          </div>

          <div className="lesson-container">
            {/* 見出しと「カートを見る」ボタンを横並びに */}
            <div className="list-header">
              <h3>商品一覧</h3>
              <Link to="/cart" className="cart-link-btn">カートを見る</Link>
            </div>

            {loading && <p>在庫データ取得中...</p>}
            {error && <p style={{ color: 'red' }}>エラーが発生しました：{error}</p>}

            {!loading && !error &&
              lessonList.map((lessonItem) => (
                <Lesson
                  key={lessonItem.name}
                  id={this.getIdByName(lessonItem.name)}          // productId
                  name={lessonItem.name}
                  image={lessonItem.image}
                  introduction={lessonItem.introduction}
                  stock={this.getStockByName(lessonItem.name)}
                  price={PRICE_MAP[lessonItem.name]}               // 価格
                  apiBase="http://localhost:3001"
                />
              ))
            }
          </div>
        </div>
      </div>
    );
  }
}

export default Main;
