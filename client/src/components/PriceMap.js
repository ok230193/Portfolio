const PRICE_MAP = {
  'オーブン':        49800,
  'コーヒーメーカー': 9800,
  '電気スタンド':    4980,
  'ヘッドホン':      32800,
  'パソコン':        128000,
  '扇風機':          7980,
  '洗濯機':          69800,
  '炊飯器':          55800,
  'タブレット':      29800,
  'テレビ':          99800,
};

export default PRICE_MAP;
export const toJPY = (v) => '¥' + Number(v ?? 0).toLocaleString('ja-JP');
