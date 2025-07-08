import React, { useRef } from 'react';
import myImg from '../assets/image_icon2.png';


function UploadBox({
  setImageFile,
  previewUrl,
  uploadedFileName,
  setPreviewUrl,
  setUploadedFileName
}) {
  const fileInputRef = useRef();

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setImageFile(file);
      setUploadedFileName(file.name);
      setPreviewUrl(URL.createObjectURL(file));
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    if (file) {
      setImageFile(file);
      setUploadedFileName(file.name);
      setPreviewUrl(URL.createObjectURL(file));
    }
  };

  const handleDragOver = (e) => e.preventDefault();

  const openFileDialog = () => {
    if (fileInputRef.current) {
      fileInputRef.current.click();
    }
  };

  const handleReset = (e) => {
    e.stopPropagation();
    setImageFile(null);
    setUploadedFileName('');
    setPreviewUrl(null);
    // input 초기화 (같은 파일 다시 선택 가능하게)
    if (fileInputRef.current) {
      fileInputRef.current.value = null;
    }
  };

  return (
    <div
      className="upload-box"
      onDrop={handleDrop}
      onDragOver={handleDragOver}
      onClick={() => {
        if (!previewUrl) openFileDialog();
      }}
    >
      <input
        type="file"
        accept="image/*"
        ref={fileInputRef}
        style={{ display: 'none' }}
        onChange={handleFileChange}
      />

      {!previewUrl ? (
        <>
          <img src={myImg} alt="이미지 아이콘" className="my-image" />
          <p>Drag & drop an image here, or click to upload</p>
          <button
            className="upload-btn"
            onClick={(e) => {
              e.stopPropagation();
              openFileDialog();
            }}
          >
            Upload
          </button>
        </>
      ) : (
        <>
          <img src={previewUrl} alt="preview" className="preview-img" />
          <button
            className="delete-btn"
            onClick={handleReset}
            style={{ marginTop: '10px', backgroundColor: '#cde9f0', color: '#FDFFFD' }}
          >
            Delete
          </button>
        </>
      )}
    </div>
  );
}

export default UploadBox;