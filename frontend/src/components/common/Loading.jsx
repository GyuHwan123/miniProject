import React from 'react';
import './Loading.scss';

const Loading = ({ message = "처리 중입니다..." , subMessage }) => {
  return (
    <div className="loading-overlay">
      <div className="loading-content">
        {/* 애니메이션 SVG 스피너 */}
        <svg className="loading-spinner" viewBox="0 0 50 50">
          <circle
            className="path"
            cx="25"
            cy="25"
            r="20"
            fill="none"
            strokeWidth="5"
          />
        </svg>

        {/* 상황별 메시지 */}
        <p className="loading-text">{message}</p>
        {subMessage && <p className="loading-sub-message">{subMessage}</p>}
      </div>
    </div>
  );
};

export default Loading;