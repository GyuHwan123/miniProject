import React from 'react';
import './ResultViewer.scss';

const ResultViewer = ({ ocrText, onDownload }) => {
  return (
    <div className="result-viewer">
      <h2 className="viewer-title">OCR 텍스트 추출 결과</h2>
      
      {/* 회색 박스 영역 */}
      <div className="content-box">
        {ocrText ? (
          <div className="text-content">{ocrText}</div>
        ) : (
          <div className="placeholder-text">OCR로 추출된 텍스트가 표시됩니다.</div>
        )}
      </div>

      {/* 하단 액션 버튼 */}
      <div className="action-area">
        <button className="download-button" onClick={onDownload}>
          다운로드
        </button>
      </div>
    </div>
  );
};

export default ResultViewer;