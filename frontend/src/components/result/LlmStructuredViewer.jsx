import React, { useState } from 'react';
import './LlmStructuredViewer.scss';

const LlmStructuredViewer = ({ llmResult, onSummarize, onDownload, isLoading }) => {
  const [hasSummarized, setHasSummarized] = useState(false);

  const handleSummarizeClick = () => {
    setHasSummarized(true);
    if (onSummarize) {
      onSummarize();
    }
  };

  return (
    <div className="llm-structured-viewer">
      {/* 타이틀을 위한 영역 (레이아웃 상단 수평 맞춤용) */}
      <div className="viewer-header">
        <h2 className="viewer-title">LLM 구조화 요약</h2>
      </div>

      {/* 처음에는 회색 영역 전체가 클릭 가능한 'LLM 요약 하기' 버튼 */}
      {!hasSummarized ? (
        <button 
          className="summarize-trigger-box" 
          onClick={handleSummarizeClick}
          disabled={isLoading}
        >
          <span>{isLoading ? '요약 중입니다...' : 'LLM 요약 하기'}</span>
        </button>
      ) : (
        /* 요약 클릭 후 보여지는 결과 영역 */
        <div className="content-box">
          {isLoading ? (
            <div className="loading-state">LLM이 문서를 요약하고 있습니다...</div>
          ) : llmResult ? (
            <div className="result-content">{llmResult}</div>
          ) : (
            <div className="placeholder-text">요약 결과가 존재하지 않습니다.</div>
          )}
        </div>
      )}

      {/* 하단 액션 버튼 (요약 실행 후에만 노출) */}
      <div className="action-area">
        {hasSummarized && (
          <button 
            className="download-button" 
            onClick={onDownload}
            disabled={isLoading || !llmResult}
          >
            다운로드
          </button>
        )}
      </div>
    </div>
  );
};

export default LlmStructuredViewer;