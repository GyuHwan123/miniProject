import React, { useState } from 'react';
import FileUploader from '../components/uploader/FileUploader';
import Result from './Result';

const Main = () => {
  // 'upload' | 'result' 상태로 화면 전환 제어
  const [step, setStep] = useState('upload'); 

  // 파일 업로드 모달에서 '다음' 버튼 눌렀을 때 호출되는 함수
  const handleNextStep = (selectedFiles) => {
    console.log('선택된 파일 목록 (더미):', selectedFiles);
    // 백엔드 요청 대신 바로 결과 화면 단계로 변경
    setStep('result'); 
  };

  return (
    <main className="main-container">
      {step === 'upload' && (
        <FileUploader 
          onClose={() => alert('닫기 버튼 클릭')} 
          onNext={handleNextStep} 
        />
      )}

      {step === 'result' && (
        <div>
          {/* 다시 업로드 화면으로 돌아가는 임시 버튼 */}
          <button 
            onClick={() => setStep('upload')}
            style={{ margin: '20px', padding: '8px 16px', cursor: 'pointer' }}
          >
            ← 다시 업로드하기
          </button>
          
          {/* 결과 화면 컴포넌트 */}
          <SearchResult />
        </div>
      )}
    </main>
  );
};

export default Main;