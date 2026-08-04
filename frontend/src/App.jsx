import React, { useState } from 'react';
import Header from './components/common/Header';
import Footer from './components/common/Footer';
import FileUploader from './components/uploader/FileUploader';
import Result from './pages/Result';
import {uploadOCR} from "./api/ocrApi";

import './App.scss';

function App() {
  // 현재 화면 단계를 관리하는 상태 ('upload' 또는 'result')
  const [step, setStep] = useState('upload');
  const [ocrText, setOcrText] = useState(""); // OCR 결과 텍스트 상태

  // 모달에서 '다음' 버튼을 눌렀을 때 실행되는 함수
  const handleNext = async (files) => {
    console.log("업로드할 파일들:", files);

    try {
      // OCR 서버 호출
      const result = await uploadOCR(files);

      console.log("OCR 결과:", result);

      // OCR 텍스트 저장
      setOcrText(result.ocr_text);   // ← 응답 형식에 따라 수정될 수 있음

      // 결과 페이지 이동
      setStep("result");

    } catch (error) {
      console.error(error);
      alert("OCR 실행에 실패했습니다.");
    }
  };

  return (
    <div className="app-layout">
      <Header />

      <main className="app-content">
        {/* step이 'upload'일 때는 파일 업로더 표시 */}
        {step === 'upload' && (
          <FileUploader
            onClose={() => alert('닫기 버튼')}
            onNext={handleNext}
          />
        )}

        {/* step이 'result'일 때는 OCR/LLM 결과 페이지 표시 */}
        {step === 'result' && (
          <div className="result-wrapper">
            {/* 다시 업로드 화면으로 돌아가는 테스트용 버튼 */}
            <button 
              className="back-button"
              onClick={() => setStep('upload')}
            >
              ← 다시 업로드하기
            </button>
            <Result ocrText={ocrText} />
          </div>
        )}
      </main>

      <Footer />
    </div>
  );
}

export default App;