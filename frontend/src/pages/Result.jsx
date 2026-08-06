import React, { useState } from 'react';
import { useParams, useLocation } from 'react-router-dom';
import ResultViewer from '../components/result/ResultViewer';
import LlmStructuredViewer from '../components/result/LlmStructuredViewer';
import Loading from '../components/common/Loading';
import './Result.scss';

const Result = ({ ocrText: propsOcrText }) => {
  const { summaryId } = useParams();
  const location = useLocation();
  
  
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
      {/* 💡 2. isLoading이 true일 때 전체 화면 로딩 오버레이 띄우기! */}
      {isLoading && (
        <Loading 
          message="LLM이 문서를 요약하고 있습니다..." 
          subMessage={
            <>
              문서 길이에 따라 텍스트를 분석하는 데 시간이 조금 더 걸릴 수 있어요.<br />
              잠시만 여유를 가지고 기다려주세요! 😊
            </>
          }
        />
      )}
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