import React, { useState } from 'react';
// ⭕ 자기 자신이 아닌 ResultViewer와 LlmStructuredViewer를 import 해야 합니다!
import ResultViewer from '../components/result/ResultViewer';
import LlmStructuredViewer from '../components/result/LlmStructuredViewer';
import './Result.scss';

const Result = () => {
  // OCR 추출 결과 더미 데이터
  const [ocrText] = useState(
    '이것은 OCR 기술로 문서에서 1차적으로 추출된 텍스트입니다.\n실제 백엔드 연동 시 추출된 내용이 여기에 들어옵니다.'
  );

  const [llmResult, setLlmResult] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  // OCR 다운로드 버튼
  const handleOcrDownload = () => {
    alert('OCR 텍스트 결과를 다운로드합니다.');
  };

  // LLM 요약 실행 핸들러
  const handleSummarize = () => {
    setIsLoading(true);
    setTimeout(() => {
      setLlmResult(
        '1. 주요 내용 요약\n- OCR 기술과 Ollama LLM을 결합하여 문서를 효율적으로 가공함.\n\n2. 핵심 정보\n- 문서를 분석하고 요약된 텍스트 추출 완료.'
      );
      setIsLoading(false);
    }, 1200);
  };

  // LLM 다운로드 버튼
  const handleLlmDownload = () => {
    alert('LLM 요약 결과를 다운로드합니다.');
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