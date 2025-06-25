//import { useState } from 'react'
//import reactLogo from './assets/react.svg'
//import viteLogo from '/vite.svg'
import './App.css'
import React from 'react';
import myImg from './assets/image_icon.png';


function App() {
  //const [count, setCount] = useState(0) 

  return (
  <>
  <div className="Whole-background">
  <div className="container">
    
    <div className="left-area">
      <h2>Emotion Analysis</h2>

      <div className="upload-box">
        <img src={myImg} alt="설명 텍스트" className="my-image" />
        <p>Drag & drop an image here, or click to upload</p>
        <button className="upload-btn">Upload</button>
      </div>

      <button className="analysis-btn">Analysis</button>
    </div>

    <div className="right-area">
      <div className="top-right">
        <div className="results">
          <h3>Results</h3>
          <p className="info-line">
            <strong>Age :</strong>
            <span>20대</span>
          </p>
          <p className="info-line">
            <strong>Gender :</strong>
            <span>Female</span>
          </p>
          <p className="info-line">
            <strong>Emotion :</strong>
            <span>Sadness</span>
          </p>
        </div>

        <div className="feel-control">
          <h3>How do you want to feel?</h3>
          <div className="feel-buttons">
            <button className="express-btn">Express</button>
            <button className="calmdown-btn">Calm down</button>
          </div>
        </div>
      </div>

      <div className="emotion-summary">
        <p>오늘은 기분이 좀 우울해 보이네요,</p>
        <p>20대 여성인 당신에게 위로가 될 수 있는 아이템들을 추천해드릴게요</p>
      </div>

      <div className="recommand">
        <h3>You might like</h3>

        <div className="items">
          <div className="item-card">
            <img src="이미지경로" alt="non-image" />
            <p>상품명</p>
            <span>shop now</span>
          </div>

          <div className="item-card">
            <img src="이미지경로" alt="non-image" />
            <p>상품명</p>
            <span>shop now</span>
          </div>

          <div className="item-card">
            <img src="이미지경로" alt="non-image" />
            <p>상품명</p>
            <span>shop now</span>
          </div>
          
          <div className="item-card">
            <img src="이미지경로" alt="non-image" />
            <p>상품명</p>
            <span>shop now</span>
          </div>
          
          <div className="item-card">
            <img src="이미지경로" alt="non-image" />
            <p>상품명</p>
            <span>shop now</span>
          </div>
        
        </div>
      </div>
    </div>
    
  </div>
</div>


  </>

  )
}

export default App
