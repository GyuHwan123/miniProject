import React, { useState } from 'react';
import { useParams } from 'react{/* react-router-dom 사용 시 */}-dom'; // ⭕ React Router Hook 가져오기
import ResultViewer from '../components/result/ResultViewer';
import LlmStructuredViewer from '../components/result/LlmStructuredViewer';
import './Result.scss';

const Result = () => {
  // ⭕ URL 경로(e.g., /result/:summaryId)에서 실제 ID를 자동으로 추출!
  const { summaryId } = useParams(); 

  const [ocrText] = useState('OCR 추출 텍스트...');
  const [llmResult, setLlmResult] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  /* // 현재 조회하려는 summaryId (URL 파라미터나 전달받은 ID 값)테스트용
  const summaryId = "123"; */

  // OCR 다운로드 버튼
  const handleOcrDownload = () => {
    // 백엔드 OCR 다운로드 API 호출
    window.location.href = `http://localhost:8000/download/${summaryId}?type=ocr`;
  };

  // ⭕ LLM 요약 실행 핸들러 (진짜 백엔드 통신으로 변경!)
  const handleSummarize = async () => {
    setIsLoading(true);
    try {
      // GET /api/summary/{summaryId} 호출
      const response = await fetch(`http://localhost:8000/api/summary/${summaryId}`);
      
      if (!response.ok) {
        throw new Error('요약 실패');
      }

      const data = await response.json();
      // 백엔드에서 받은 llm_result를 상태에 저장
      setLlmResult(data.llm_result); 
    } catch (error) {
      console.error("요약 가져오기 실패:", error);
      alert("LLM 요약 데이터를 가져오지 못했습니다.");
    } finally {
      setIsLoading(false);
    }
  };

 // LLM 다운로드 버튼
  const handleLlmDownload = () => {
    // 백엔드 LLM 다운로드 API 호출
    window.location.href = `http://localhost:8000/download/${summaryId}?type=llm`;
  };

  return (
    <div className="search-result-container">
      <div className="result-grid">
        {/* 왼쪽 OCR 텍스트 영역 */}
        <div className="grid-item">
          <ResultViewer ocrText={ocrText} onDownload={handleOcrDownload} />
        </div>

        {/* 오른쪽 LLM 요약 영역 */}
        <div className="grid-item">
          <LlmStructuredViewer
            llmResult={llmResult}
            onSummarize={handleSummarize}
            onDownload={handleLlmDownload}
            isLoading={isLoading}
          />
        </div>
      </div>
    </div>
  );
};

export default Result;