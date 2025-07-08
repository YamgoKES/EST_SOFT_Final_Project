import { useState } from 'react'
import { useRef } from 'react' // useRef import 추가!
//import reactLogo from './assets/react.svg'
//import viteLogo from '/vite.svg'
import './App.css'
import axios from 'axios';
// import myImg from './assets/image_icon.png';
import UploadBox from './components/UploadBox';
import ResultBox from './components/ResultBox';
import FeelControl from './components/FeelControl';
import EmotionSummary from './components/EmotionSummary';
import RecommendationList from './components/RecommendationList';

//analyzeCustomers (구현부가 간단하니까 여기에 작성을 할 예정 복잡해질거 같으면 apu.js등으로 빼겠음)
const analyzeCustomers = async(imageFile, feelMode) => {
  const formData = new FormData()
  formData.append('file', imageFile)
  formData.append('feel_mode', feelMode); //추가... 

  const response = await axios.post('http://localhost:8000/predict' , formData, {
    headers : {
      "Content-Type" : "multipart/form-data"
    },
  });

  return response.data;
};



function App() {
  //const [count, setCount] = useState(0) 
  const feelRef = useRef(); // ref 생성
  const [imageFile, setImageFile] = useState(null);
  const [loading, setLoading] =useState(false);
  const [result, setResult] = useState(null); //age, gender, emotion 받기
  const [feelMode, setFeelMode] = useState(null);
  const [promptText, setPromptText] = useState('');
  const [recommendationItems, setRecommendItems] = useState([]);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [uploadedFileName, setUploadedFileName] = useState('');

const handleAnalyze = async () => {
  if (!imageFile) return;

  if (!feelMode) {
    // UX: 흔들리기 + 로딩 잠깐 보여주기
    setLoading(true);
    feelRef.current.classList.add('shake');
    setTimeout(() => {
      feelRef.current.classList.remove('shake');
      setLoading(false);
    }, 600);
    return;
  }

  setLoading(true);
  try {
    const res = await analyzeCustomers(imageFile, feelMode);
    setResult(res);
  } catch (e) {
    alert('분석 실패! 다시 시도해주세요.');
    console.error(e);
  } finally {
    setLoading(false);
  }
};

  return (
  <>
  <div className="Whole-background">
    <div className="container">
    
      <div className="left-area">
        <h2>Emotion Analysis</h2>
        <UploadBox 
          setImageFile={setImageFile}
          previewUrl={previewUrl}
          uploadedFileName={uploadedFileName}
          setUploadedFileName={setUploadedFileName}
          setPreviewUrl={setPreviewUrl}
        />
        <button className="analysis-btn" onClick = {handleAnalyze} disabled={loading}>{loading ? '분석 중...' : 'Analysis'}</button>
      </div>

      <div className="right-area">
        <div className="top-right">
          <ResultBox result={result}/>
          <FeelControl
            setFeelMode={setFeelMode}
            feelRef={feelRef}
            currentFeelMode={feelMode}
          />
        </div>
        
      
        <EmotionSummary 
          promptText={feelMode ? result?.recommendationtext : "추천을 보려면 느낌 상태를 선택해주세요."} 
        />
        <RecommendationList 
          items={feelMode ? (result?.recommendationItems || []) : []} 
        />
     
      </div>
    </div>
  </div>


  </>

  )
}

export default App;
