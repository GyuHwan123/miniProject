import React, { useState } from 'react';
import Header from './components/common/Header';
import Footer from './components/common/Footer';
import FileUploader from './components/uploader/FileUploader';
import Result from './pages/Result';
import './App.scss';

function App() {
  // 현재 화면 단계를 관리하는 상태 ('upload' 또는 'result')
  const [step, setStep] = useState('upload');

  // 모달에서 '다음' 버튼을 눌렀을 때 실행되는 함수
  const handleNext = (files) => {
    console.log('업로드할 파일들:', files);
    // 💡 화면 단계를 'result'로 변경하여 SearchResult 컴포넌트를 보여줍니다.
    setStep('result');
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
            <Result />
          </div>
        )}
      </main>

      <Footer />
    </div>
  );
}

export default App;