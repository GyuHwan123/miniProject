import React, { useState, useRef } from 'react';
import { X, FolderPlus } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

import './FileUploader.scss';

const FileUploader = ({ onClose, onNext }) => {
  const navigate = useNavigate();
  const [selectedFiles, setSelectedFiles] = useState([]);
  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef(null);

  const MAX_FILES = 1;
  // 20MB 제한 설정 (20 * 1024 * 1024 bytes)
  const MAX_FILE_SIZE = 20 * 1024 * 1024;
  const ALLOWED_EXTENSIONS = ['jpg', 'jpeg', 'png', 'pdf', 'hwp', 'docs', 'doc'];

  const validateAndAddFiles = (newFiles) => {
    const fileList = Array.from(newFiles);

    if (selectedFiles.length + fileList.length > MAX_FILES) {
      alert(`한번에 ${MAX_FILES}개 파일까지 업로드할 수 있습니다.`);
      return;
    }
    // 2. 용량 체크 (20MB 미만)
    const overSizedFiles = fileList.filter((file) => file.size >= MAX_FILE_SIZE);
    if (overSizedFiles.length > 0) {
      alert('20MB 미만의 파일만 업로드할 수 있습니다.');
    }

    const validFiles = fileList.filter((file) => {
      const ext = file.name.split('.').pop().toLowerCase();
      return ALLOWED_EXTENSIONS.includes(ext);
    });

    if (validFiles.length !== fileList.length) {
      alert('.jpg, .png, .pdf, .hwp, .docs 형식의 파일만 업로드 가능합니다.');
    }

    setSelectedFiles((prevFiles) => [...prevFiles, ...validFiles]);
  };

  /* const handleOcrSuccess = (extractedOcrText) => {
    // 8001번이나 8000번에서 받아온 OCR 텍스트를 state로 전달하며 이동!
    navigate(`/result/${summaryId}`, { 
      state: { ocrText: extractedOcrText } 
    });
  }; */
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

  // OCR 종류를 인자로 받아 상위 컴포넌트(onNext)로 전달
  /* const handleOcrSubmit = async (ocrType) => {
    if (selectedFiles.length === 0) return;

    const formData = new FormData();
    formData.append('file', selectedFiles[0]); // 선택된 파일
    formData.append('ocr_type', ocrType);     // 'easy' 또는 'paddle'

    try {
      // 1. 백엔드(8000번)로 파일 전송 및 OCR 처리 요청
      const response = await fetch('http://localhost:8000/api/ocr/test', {
        method: 'POST',
        body: formData, // FormData 전송 시 Content-Type 헤더는 자동으로 설정됨
      });

      if (!response.ok) {
        throw new Error('OCR 처리 실패');
      }

      const data = await response.json();
      
      // 2. OCR 성공 시 가져온 텍스트를 가지고 Result 페이지로 이동!
      // (백엔드가 주는 키값에 맞게 data.ocr_text 또는 data.text 등으로 수정)
      const extractedText = data.ocr_text || data.text || data.summary;
      const taskId = data.task_id || data.summary_id || 'temp_id';

      navigate(`/result/${taskId}`, {
        state: { ocrText: extractedText }
      });

    } catch (error) {
      console.error("OCR 요청 실패:", error);
      alert("OCR 실패! 백엔드(8000번) 서버가 켜져있는지 확인해주세요.");
    }
  }; */

  // OCR 종류를 인자로 받아 상위 컴포넌트(App.jsx의 onNext)로 전달
  const handleOcrSubmit = (ocrType) => {
    console.log("선택한 OCR:", ocrType);
    if (selectedFiles.length === 0) return;

    // 💡 직접 fetch하지 않고 App.jsx의 handleNext(files, ocrType)를 실행시킵니다!
    if (onNext) {
      onNext(selectedFiles, ocrType);
    }
  };

  return (
    <div className="modal-card">
      {/* 모달 헤더 */}
      <div className="modal-header">
        <div>
          <h2 className="modal-title">미디어 업로드</h2>
          <p className="modal-subtitle">
            여기에 문서를 추가하세요. 한번에 {MAX_FILES}개까지 업로드할 수 있습니다.
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
          accept=".jpg,.jpeg,.png,.pdf,.hwp,.docs,.doc"
          className="hidden-file-input"
        />
      </div>

      {/* 안내 문구 */}
      <p className="support-text">.jpg, .png, .pdf, .hwp, .docs 파일만 지원합니다.</p>

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

      {/* 푸터 영역: OCR 선택 가이드 및 action 버튼 */}
      <div className="modal-footer-container">
        <p className="ocr-select-title">사용하실 OCR을 선택해주세요</p>
        <div className="modal-footer">
          <button type="button" className="cancel-button" onClick={onClose}>
            취소
          </button>
          
          <div className="ocr-button-group">
            <button
              type="button"
              className="next-button easy-ocr"
              disabled={selectedFiles.length === 0}
              onClick={(e) => {
                e.preventDefault();
                handleOcrSubmit('easy');
              }}
            >
              EasyOCR 실행
            </button>
            <button
              type="button"
              className="next-button paddle-ocr"
              disabled={selectedFiles.length === 0}
              onClick={(e) => {
                e.preventDefault();
                handleOcrSubmit('paddle');
              }}
            >
              PaddleOCR 실행
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default FileUploader;