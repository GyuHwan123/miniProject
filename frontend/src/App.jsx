import React, { useState } from 'react';
import Header from './components/common/Header';
import Footer from './components/common/Footer';
import Loading from './components/common/Loading';
import FileUploader from './components/uploader/FileUploader';
import Result from './pages/Result';
import {uploadOCR} from "./api/ocrApi";

import './App.scss';

function App() {
  // 현재 화면 단계를 관리하는 상태 ('upload' 또는 'result')
  const [step, setStep] = useState('upload');
  const [ocrText, setOcrText] = useState('');
  /* const [summaryResult, setSummaryResult] = useState(''); //이거 테스트용임 */
  const [isLoading, setIsLoading] = useState(false);
  const [isLlmLoading, setIsLlmLoading] = useState(false);

  const [loadingMessage, setLoadingMessage] = useState('');

  // 모달에서 'OCR 실행' 버튼을 눌렀을 때 실행되는 함수
  const handleNext = async (files, ocrType) => {
    console.log('업로드할 파일들:', files, '선택한 OCR:', ocrType);
    
    if (!files || files.length === 0) return;

    setIsLoading(true);
    

    try {
      // 1️⃣ 백엔드(8000번)로 파일 전송 및 OCR 요청 (진짜 백엔드 연동 시)
      setLoadingMessage('OCR 실행 중...');
      const formData = new FormData();
      formData.append('file', files[0]);
      formData.append('ocr_type', ocrType);

      const response = await fetch('http://localhost:8000/api/ocr/upload', {
        method: 'POST',
        body: formData,
      }); //테스트

      // if (!response.ok) throw new Error('OCR 통신 실패'); // 정상
      // ⚠️ 아래에서 ocrResponse를 검사하므로 위 선언과 이름이 일치해야 합니다.
      if (!response.ok) throw new Error('OCR 통신 실패');//테스트

      const data = await response.json();
      // 백엔드가 반환한 OCR 텍스트를 App의 ocrText 상태에 저장!
      // setOcrText(data.ocr_text || data.text);
      setOcrText(data.ocr_text);
      /* const ocrData = await ocrResponse.json();
      const extractedText = ocrData.ocr_text || ''; */
      
      //setOcrText(extractedText);

      

    } /* catch (error) {
      console.error("OCR 요청 실패, 테스트용 더미 데이터를 채웁니다:", error);
      
      // 💡 백엔드가 아직 준비 안 되었거나 에러 날 때 비상용 더미 데이터 세팅!
      setOcrText(
        `[문서 분석 결과]\n1. 발행일자: 2026-08-04\n2. 담당자: 홍길동\n\n- 본 문서는 OCR 예시 데이터입니다.\n- 파일: ${files[0].name} (엔진: ${ocrType})`
      );
    } finally {
      setIsLoading(false);
      // 2️⃣ 화면 단계를 'result'로 변경하여 Result 페이지를 보여줍니다.
      setStep('result');
    } */
    catch (error) {
      console.error("OCR 요청 실패:", error);
      alert("백엔드 /api/ocr/test 통신 에러!");
    } finally {
      setIsLoading(false);
      setStep('result'); // Result 화면으로 이동
    }
  };

  return (
    <div className="app-layout">
      {/* 💡 OCR 로딩(isLoading) 또는 LLM 로딩(isLlmLoading) 중 하나라도 true면 로딩창을 띄웁니다 */}
      {(isLoading || isLlmLoading) && (
        <Loading 
          message={isLoading ? loadingMessage : "LLM 변환 중..."} 
          subMessage={
            <>
              이미지를 분석하고 텍스트를 추출하는 데 시간이 조금 걸릴 수 있어요.<br />
              잠시만 여유를 가지고 기다려주세요! 😊
            </>
          }
        />
      )}
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