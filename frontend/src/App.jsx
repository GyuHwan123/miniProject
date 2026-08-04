import React, { useState } from 'react';
import Header from './components/common/Header';
import Footer from './components/common/Footer';
import FileUploader from './components/uploader/FileUploader';
import Result from './pages/Result';
import './App.scss';

function App() {
  // 현재 화면 단계를 관리하는 상태 ('upload' 또는 'result')
  const [step, setStep] = useState('upload');

  // 💡 OCR 결과를 담아둘 중앙 상태
  const [ocrText, setOcrText] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  // 모달에서 'OCR 실행' 버튼을 눌렀을 때 실행되는 함수
  const handleNext = async (files, ocrType) => {
    console.log('업로드할 파일들:', files, '선택한 OCR:', ocrType);
    
    if (!files || files.length === 0) return;

    setIsLoading(true);

    try {
      // 1️⃣ 백엔드(8000번)로 파일 전송 및 OCR 요청 (진짜 백엔드 연동 시)
      const formData = new FormData();
      formData.append('file', files[0]);
      formData.append('ocr_type', ocrType);

      const response = await fetch('http://localhost:8000/api/ocr/test', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) throw new Error('OCR 통신 실패');

      const data = await response.json();
      // 백엔드가 반환한 OCR 텍스트를 App의 ocrText 상태에 저장!
      /* setOcrText(data.ocr_text || data.text); */
      setOcrText(data.ocr_text);

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
            {/* 👈 🔑 가장 중요: Result 컴포넌트에 가져온 ocrText를 내려줍니다! */}
            <Result ocrText={ocrText} />
          </div>
        )}
      </main>

      <Footer />
    </div>
  );
}

export default App;