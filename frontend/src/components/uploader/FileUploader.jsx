import React, { useState, useRef } from 'react';
import { X, FolderPlus } from 'lucide-react';

import './FileUploader.scss';

const FileUploader = ({ onClose, onNext }) => {
  const [selectedFiles, setSelectedFiles] = useState([]);
  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef(null);

  const MAX_FILES = 5;
  const ALLOWED_EXTENSIONS = ['jpg', 'png', 'svg', 'zip'];

  const validateAndAddFiles = (newFiles) => {
    const fileList = Array.from(newFiles);

    if (selectedFiles.length + fileList.length > MAX_FILES) {
      alert(`최대 ${MAX_FILES}개 파일까지 업로드할 수 있습니다.`);
      return;
    }

    const validFiles = fileList.filter((file) => {
      const ext = file.name.split('.').pop().toLowerCase();
      return ALLOWED_EXTENSIONS.includes(ext);
    });

    if (validFiles.length !== fileList.length) {
      alert('.jpg, .png, .svg, .zip 형식의 파일만 업로드 가능합니다.');
    }

    setSelectedFiles((prevFiles) => [...prevFiles, ...validFiles]);
  };

  const handleButtonClick = () => {
    fileInputRef.current?.click();
  };

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files.length > 0) {
      validateAndAddFiles(e.target.files);
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      validateAndAddFiles(e.dataTransfer.files);
    }
  };

  const handleRemoveFile = (indexToRemove) => {
    setSelectedFiles((prev) => prev.filter((_, index) => index !== indexToRemove));
  };

  return (
    <div className="modal-card">
      {/* 모달 헤더 */}
      <div className="modal-header">
        <div>
          <h2 className="modal-title">미디어 업로드</h2>
          <p className="modal-subtitle">
            여기에 문서를 추가하세요. 최대 {MAX_FILES}개까지 업로드할 수 있습니다.
          </p>
        </div>
        <button className="close-button" onClick={onClose} aria-label="닫기">
          <X size={20} />
        </button>
      </div>

      {/* 파일 드롭 영역 */}
      <div
        className={`drop-zone ${isDragging ? 'dragging' : ''}`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
      >
        <div className="icon-wrapper">
          <FolderPlus size={28} />
        </div>
        <p className="drop-text">업로드할 파일을 여기에 끌어다 놓으세요</p>
        <div className="divider">
          <span>또는</span>
        </div>
        <button className="browse-button" onClick={handleButtonClick}>
          파일 찾아보기
        </button>
        <input
          type="file"
          ref={fileInputRef}
          onChange={handleFileChange}
          multiple
          accept=".jpg,.jpeg,.png,.svg,.zip"
          className="hidden-file-input"
        />
      </div>

      {/* 안내 문구 */}
      <p className="support-text">.jpg, .png, .svg 및 .zip 파일만 지원합니다.</p>

      {/* 선택된 파일 목록 */}
      {selectedFiles.length > 0 && (
        <ul className="file-list">
          {selectedFiles.map((file, index) => (
            <li key={index} className="file-item">
              <span className="file-name">{file.name}</span>
              <button
                className="remove-file-button"
                onClick={() => handleRemoveFile(index)}
              >
                <X size={14} />
              </button>
            </li>
          ))}
        </ul>
      )}

      {/* 푸터 액션 버튼 */}
      <div className="modal-footer">
        <button className="cancel-button" onClick={onClose}>
          취소
        </button>
       {/*  <button
          className="next-button"
          disabled={selectedFiles.length === 0}
          onClick={() => onNext && onNext(selectedFiles)}
        >
          다음
        </button> */}
        <button
            type="button" // 👈 필수! (페이지 리로드 및 Form Submit 방지)
            className="next-button"
            disabled={selectedFiles.length === 0}
            onClick={(e) => {
                e.preventDefault(); // 👈 혹시 모를 기본 제출 이벤트 차단
                if (onNext) {
                onNext(selectedFiles);
                }
            }}
            >
            다음
        </button>
      </div>
    </div>
  );
};
export default FileUploader;