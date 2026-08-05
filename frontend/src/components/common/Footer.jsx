import React from 'react';
import './Footer.scss';

const Footer = () => {
  return (
    <footer className="common-footer">
      <p>OCR 인식 기술과 Ollama LLM을 결합하여 문서를 효율적으로 가공하는 툴 입니다.</p>
      <p>다양한 형태의 문서를 지원합니다.</p>
      <p className="copyright">© 2026 .miniproject.</p>
    </footer>
  );
};

export default Footer;