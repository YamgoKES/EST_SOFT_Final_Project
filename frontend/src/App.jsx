import { useState } from 'react'
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
const analyzeCustomers = async(imageFile) => {
  const formData = new FormData()
  formData.append('file', imageFile)

  const response = await axios.post('http://localhost:8000/predict' , formData, {
    headers : {
      "Content-Type" : "multipart/form-data"
    },
  });

  return response.data;
};



function App() {
  //const [count, setCount] = useState(0) 
  const [imageFile, setImageFile] = useState(null);
  const [loading, setLoading] =useState(false);
  const [result, setResult] = useState(null); //age, gender, emotion 받기
  const [feelMode, setFeelMode] = useState(null);
  const [promtText, setPromptText] = useState('');
  const [recommendItems, setRecommendItems] = useState([]);

  const handleAnalyze = async () => {
    if  (!imageFile) return;

    setLoading(true);
    try{
      const res = await analyzeCustomers(imageFile);
      setResult(res);
    }
    catch (e) {
      alert('analyze fail try again'); //추후 수정 ... 문구가 생각이 안남 ㅋㅋ
      console.error(e);
    }
    finally {
      setLoading(false);
    }
  };

  return (
  <>
  <div className="Whole-background">
    <div className="container">
    
      <div className="left-area">
        <h2>Emotion Analysis</h2>
        <UploadBox setImageFile={setImageFile}/>
        <button className="analysis-btn" onClick = {handleAnalyze} disabled={loading}>{loading ? '분석 중...' : 'Analysis'}</button>
      </div>

      <div className="right-area">
        <div className="top-right">
          <ResultBox result={result}/>
          <FeelControl setFeelMode={setFeelMode}/>
        </div>
        
        <EmotionSummary />
        <RecommendationList />
      </div>
    </div>
  </div>


  </>

  )
}

export default App
