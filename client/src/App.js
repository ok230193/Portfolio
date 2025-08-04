// client/src/App.js
import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import Footer from './components/Footer';
import Main from './components/Main';
import CartPage from './components/CartPage';

export default function App() {
  return (
    <>
      <Header />
      <Routes>
        <Route path="/" element={<Main />} />
        <Route path="/cart" element={<CartPage />} />
        {/* 404 の時はトップへ */}
        <Route path="*" element={<Main />} />
      </Routes>
      <Footer />
    </>
  );
}
