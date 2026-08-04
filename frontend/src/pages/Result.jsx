import React, { useState } from 'react';
import { useParams, useLocation } from 'react-router-dom';
import ResultViewer from '../components/result/ResultViewer';
import LlmStructuredViewer from '../components/result/LlmStructuredViewer';
import './Result.scss';

const Result = ({ ocrText: propsOcrText }) => {
  const { summaryId } = useParams();
  const location = useLocation();

  // 1. OCR 텍스트 상태 (가상의 OCR 출력 완료물)
  /* const [ocrText] = useState(
    `[문서 분석 결과]\n\n1. 발행일자: 2026-08-04\n2. 담당자: 홍길동\n\n[상세 내용]\n- 본 문서는 OCR 개행 테스트용 예시 데이터입니다.\n- 줄바꿈과 목록 형태가 올바르게 표시되는지 확인합니다.\n- 공백과 엔터가 그대로 유지되는지 체크해 보세요.`
  ); */
  
 // 1. props로 온 게 없다면, 이전 페이지에서 navigate로 넘겨준 location.state.ocrText를 사용!
  const ocrText = propsOcrText || location.state?.ocrText || '';
  const [llmResult, setLlmResult] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  // 2. OCR 다운로드 핸들러
  const handleOcrDownload = () => {
    const blob = new Blob([ocrText], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `ocr_result_${summaryId || 'text'}.txt`;
    link.click();
    URL.revokeObjectURL(url);
  };

  // 3. 백엔드 API 규격에 맞춘 LLM 요약 실행 핸들러
  const handleSummarize = async () => {
    if (!ocrText) {
      alert("요약할 OCR 텍스트가 없습니다.");
      return;
    }

    setIsLoading(true);
    try {
      // 👈 기존 백엔드 라우터 주소 (/llm/summary)로 변경
      const response = await fetch('http://localhost:8000/api/summarize', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          task_id: summaryId || 'temp_id',
          text: ocrText
        }),
      });

      if (!response.ok) {
        throw new Error('요약 실패');
      }

      const data = await response.json();
      // 백엔드가 준 응답 데이터 저장 (응답 키값이 summary인지 text인지 확인 필요)
      /* setLlmResult(data.summary || data.result || JSON.stringify(data)); */
      // 백엔드가 llm_result 나 summary 중 어떤 걸 주더라도 받아먹도록 설정!
      setLlmResult(data.llm_result || data.summary || data.result);
    } catch (error) {
      console.error("요약 가져오기 실패:", error);
      alert("LLM 요약 데이터를 가져오지 못했습니다.");
    } finally {
      setIsLoading(false);
    }
  };

  // 4. LLM 결과 다운로드 핸들러
  const handleLlmDownload = () => {
    if (!llmResult) return;
    const blob = new Blob([llmResult], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `summary_result_${summaryId || 'text'}.txt`;
    link.click();
    URL.revokeObjectURL(url);
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