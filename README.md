# 얼굴 기반 감정・성별・나이 분석 및 감정 완화 추천 시스템

---

## 📌 프로젝트 개요

본 프로젝트는 이미지 속 얼굴을 인식하여 감정, 나이, 성별을 **딥러닝 모델**로 예측하고,  
이 결과를 바탕으로 사용자에게 맞춤형 감정 완화 콘텐츠를 추천하는 웹 서비스입니다.  

팀원 간 협업을 통해 **React 프론트엔드**와 **FastAPI 백엔드**를 연동하여 실시간 예측 및 추천 기능을 구현하였습니다.

---
## 📁 데이터셋 정보

본 프로젝트에서 사용한 데이터셋은 아래 링크에서 다운로드할 수 있습니다:
- [데이터셋 다운로드 링크](https://drive.google.com/drive/folders/1lezY7r41lsvtlk9MgKO9bXjCY329IL3z?usp=drive_link)

데이터는 얼굴 이미지, 감정 라벨, 나이 및 성별 정보로 구성되어 있으며,  
전처리 과정을 거쳐 모델 학습에 활용되었습니다.


## ✨ 주요 기능

- 📷 얼굴 이미지에서 감정, 성별, 나이 예측
- 💡 감정 상태에 맞는 맞춤형 감정 표출 및 완화 관련 상품 추천 (Naver 검색 api활용)
- 🔄 React 기반 사용자 인터페이스 및 FastAPI 서버 연동
- ⚙️ 모델 서빙 및 실시간 API 응답 처리

---

## 🛠️ 사용 기술 스택

| 분야       | 기술                                                                                                     |
|------------|----------------------------------------------------------------------------------------------------------|
| **Frontend** | <img src="https://cdn.jsdelivr.net/npm/simple-icons@v8/icons/react.svg" alt="React" width="20" /> React &nbsp;&nbsp; <img src="https://cdn.jsdelivr.net/npm/simple-icons@v8/icons/axios.svg" alt="Axios" width="20" /> Axios &nbsp;&nbsp; <img src="https://cdn.jsdelivr.net/npm/simple-icons@v8/icons/css3.svg" alt="CSS3" width="20" /> Vanilla CSS |
| **Backend**  | <img src="https://cdn.jsdelivr.net/npm/simple-icons@v8/icons/python.svg" alt="Python" width="20" /> Python &nbsp;&nbsp; <img src="https://cdn.jsdelivr.net/npm/simple-icons@v8/icons/fastapi.svg" alt="FastAPI" width="20" /> FastAPI &nbsp;&nbsp; <img src="https://cdn.jsdelivr.net/npm/simple-icons@v8/icons/openai.svg" alt="OpenAI" width="20" /> OpenAI API &nbsp;&nbsp; EmotionFAN (감정 예측) |
| **AI/ML**    | <img src="https://cdn.jsdelivr.net/npm/simple-icons@v8/icons/pytorch.svg" alt="PyTorch" width="20" /> PyTorch &nbsp;&nbsp;  TorchVision &nbsp;&nbsp;  ResNet50 &nbsp;&nbsp; <img src="https://cdn.jsdelivr.net/npm/simple-icons@v8/icons/pandas.svg" alt="Pandas" width="20" /> Pandas |
| **기타**     | <img src="https://cdn.jsdelivr.net/npm/simple-icons@v8/icons/numpy.svg" alt="NumPy" width="20" /> NumPy &nbsp;&nbsp; Matplotlib &nbsp;&nbsp;  Pillow &nbsp;&nbsp; <img src="https://cdn.jsdelivr.net/npm/simple-icons@v8/icons/json.svg" alt="JSON" width="20" /> JSON |


---

## 🚀 실행 방법
### 1. 프론트엔드 실행 
cd frontend
npm install
npm run dev


### 2. 백엔드 서버 실행
cd backend

#### 가상환경 생성 (원하는 이름으로)
python -m venv <env_name>

#### 가상환경 활성화
#### Windows (PowerShell) 버전
<env_name>\Scripts\Activate.ps1

#### Windows (cmd) 버전
<env_name>\Scripts\activate.bat

#### macOS / Linux 버전
source <env_name>/bin/activate

#### 필요한 패키지 설치 
pip install fastapi uvicorn torch torchvision torchmetrics pandas numpy pillow matplotlib

#### FastAPI 서버 실행
uvicorn main:app --reload

---
## 💡 회고 및 추후 방향

- 나이 성별에 대한 데이터 불균형 문제에 대해 가중치 조정과 샘플링을 적용하며 모델 성능 향상을 도모했습니다.  자세한 설명은 하위폴더 README참
- 멀티태스크 학습 방식을 도입해 나이, 성별 예측을 동시에 처리하는 구조를 설계하였습니다.  
- 프론트엔드와 백엔드의 API 연동을 완료하고, 실시간 예측 결과를 UI에 반영하는 데 성공하였습니다.  
- 앞으로는 나이/성별모델의 후반부 레이어 미세조정, 오토인코더 기반 추가 실험 등을 통해 성능을 더 개선할 계획입니다.  
- 최종 발표 후, 데이터 보완 및 모델 튜닝에 집중할 예정이며, 사용자 피드백을 반영하여 UI/UX도 개선할 예정입니다.

