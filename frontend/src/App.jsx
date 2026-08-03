import {BrowserRouter, Routes, Route } from "react-router-dom";
import { useState, useEffect } from 'react';
import React from 'react';

import Header from './components/common/Header';
import Footer from './components/common/Footer';
import Loading from './components/common/Loading';
import Main from './pages/Main';
import Join from './pages/Join';
import Login from './pages/Login';
import FileUploader from "./components/uploader/FileUploader";

import "./App.scss";


function App() {
  const handleClose = () => {
    console.log('닫기 버튼 클릭');
  };

  const handleNext = (files) => {
    console.log('업로드할 파일들:', files);
    // 여기서 서버로 파일 전송 API를 호출하면 됩니다.
  };

  return (
    <div className="app-layout">
      <Header />
      <main className="app-content">
        <FileUploader onClose={handleClose} onNext={handleNext} />
      </main>
      <Footer />
    </div>
  );
}

export default App;
