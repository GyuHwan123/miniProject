import React, { useState } from 'react';
// import { useParams } from 'react{/* react-router-dom 사용 시 */}-dom'; // ⭕ React Router Hook 가져오기 DB있는경우
import { useParams } from 'react-router-dom'; //DB없을경우
import ResultViewer from '../components/result/ResultViewer';
import LlmStructuredViewer from '../components/result/LlmStructuredViewer';
import './Result.scss';


const Result = () => {
  const { summaryId } = useParams(); // 작업 단위 구분용 ID (옵션)

  // 1. OCR 텍스트 상태 (실제로는 이전 페이지에서 넘겨받거나 props로 받아온 텍스트)
  const [ocrText] = useState(
    '이것은 OCR 기술로 문서에서 1차적으로 추출된 텍스트입니다.'
  ); // DB없는경우
/* const Result = () => {
  // ⭕ URL 경로(e.g., /result/:summaryId)에서 실제 ID를 자동으로 추출!
  const { summaryId } = useParams(); 

  const [ocrText] = useState('OCR 추출 텍스트...'); */ // DB있는경우
  const [llmResult, setLlmResult] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  /* // 현재 조회하려는 summaryId (URL 파라미터나 전달받은 ID 값)테스트용
  const summaryId = "123"; */

    const handleOcrDownload = () => {
    const blob = new Blob([ocrText], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `ocr_result_${summaryId || 'text'}.txt`;
    link.click();
    URL.revokeObjectURL(url);
  };

  // 3. ⭕ DB 없는 구조에 맞춘 LLM 요약 실행 핸들러 (POST 방식으로 텍스트 직접 전송)
  const handleSummarize = async () => {
    if (!ocrText) {
      alert("요약할 OCR 텍스트가 없습니다.");
      return;
    }

    setIsLoading(true);
    try {
      // POST 요청으로 요약할 텍스트를 Body에 담아 백엔드로 보냅니다.
      const response = await fetch('http://localhost:8000/api/summarize', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          task_id: summaryId || 'temp_id',
          text: ocrText // 👈 핵심! DB가 없으므로 요약할 텍스트를 직접 넘겨줍니다.
        }),
      });

      if (!response.ok) {
        throw new Error('요약 실패');
      }

      const data = await response.json();
      // 백엔드가 즉시 생성해서 돌려준 llm_result 저장
      setLlmResult(data.llm_result); 
    } catch (error) {
      console.error("요약 가져오기 실패:", error);
      alert("LLM 요약 데이터를 가져오지 못했습니다.");
    } finally {
      setIsLoading(false);
    }
  };

  // 4. LLM 결과 다운로드 (브라우저 자체 다운로드 활용)
  const handleLlmDownload = () => {
    if (!llmResult) return;
    const blob = new Blob([llmResult], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `summary_result_${summaryId || 'text'}.txt`;
    link.click();
    URL.revokeObjectURL(url);
  }; //DB없는경우
  /* // OCR 다운로드 버튼
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
  }; */ //DB있는경우

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