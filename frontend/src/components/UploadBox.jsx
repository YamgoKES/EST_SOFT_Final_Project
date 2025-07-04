import React, { useRef } from 'react';
import myImg from '../assets/image_icon2.png';

function UploadBox({setImageFile}) {
    const fileInputRef  = useRef();

    const handleFileChange = (e) => {
        const file = e.target.files[0];
        if(file) {
            setImageFile(file); //전달
        }
    };

    const handleDrop = (e) => {
        e.preventDefault();
        const file = e.dataTransfer.files[0];
        if (file) setImageFile(file);
    };

    const handleDragOver = (e) =>{
        e.preventDefault();
    }

    return (
        <div 
            className="upload-box"
            onDrop={handleDrop} //드레그 엔 드롭 기능 추가
            onDragOver = {handleDragOver} 
            onClick={()=>fileInputRef.current.click()}
        >
            <img src={myImg} alt="설명 텍스트" className="my-image" />
            <p>Drag & drop an image here, or click to upload</p>
            <input 
                type="file"
                accept="image/*"
                ref={fileInputRef}
                style={{display : "none"}} // 파일 선택 안보이게 숨기기
                onChange={handleFileChange}
            />
            <button className="upload-btn" 
            onClick={()=>fileInputRef.current.click()}>Upload</button>
        </div>
    );
}

export default UploadBox;