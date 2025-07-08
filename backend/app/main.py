from fastapi import FastAPI, UploadFile, File, Form
import torch
from PIL import Image
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
import re

#모델 및 전처리 임포트란
from .process_age_gender import YoloTransform, transform, yolo_model_path
from .model_age_gender import model_e_v1, device
from .EA_predictor import EmotionFANPredictor_Attention 
from .openai_helper import build_prompt_v2, ask_chatgpt
from .naver_api import search_naver_items

app = FastAPI()

# CORS 허용 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 또는 ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

processor = YoloTransform(
    yolo_model_path=yolo_model_path,
    conf_threshold=0.7,
    transform=transform
)

#감정예측
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EMOTION_MODEL_PATH = os.path.abspath(os.path.join(BASE_DIR, '..', 'trained', 'best_model.pth'))

emotion_predictor=EmotionFANPredictor_Attention(
    model_path=EMOTION_MODEL_PATH,
    device = None,
    face_model_path=yolo_model_path,
    use_face_crop = True
)

@app.post('/predict')
async def predict(file: UploadFile = File(...), feel_mode: str =Form(...)) :
    print(f"📦 받은 feel_mode 값: {feel_mode}")
    image = Image.open(file.file).convert('RGB')
    input_tensor = processor.detect_best_cropping(image)
    input_tensor = input_tensor.to(device)

    #나이 성별 예측
    with torch.no_grad():
        out_put = model_e_v1(input_tensor)
        predicted_age = out_put[:,0].item()
        predicted_gender_idx = torch.argmax(out_put[:,1:3], dim=1).item()
        predicted_gender = 'Male' if predicted_gender_idx==1 else 'Female'
    
    #감정분석
    emotion_result = emotion_predictor.predict(image)
    emotion=emotion_result['emotion']
    
    # 프롬프트 생성 (feel_mode 포함)
    load_dotenv() 
    api_key=os.getenv('OPENAI_API_KEY')
    prompt = build_prompt_v2(emotion, predicted_gender, predicted_age * (60-10) + 10, feel_mode)
    recommendation_text = ask_chatgpt(prompt, api_key=api_key)
    
    #Navershopping api / recommendation
    categories = re.findall(r"<\[(.*?)\]>", recommendation_text)
    
    #추천 카테고리 ( 각 추천카테고리 별(3개) 랜덤 5개 뽑아내기)
    recommendation_items = []
    seen_links = set()

    num_cats = len(categories)
    min_per_cat = 1
    remaining_slots = 5 - (min_per_cat * num_cats)

    # 카테고리별로 3~5개씩 미리 받아오기 (한 번에 많이 요청)
    fetch_count_per_cat = 5

    cat_items_map = {}  # 카테고리별 받은 아이템 저장

    for cat in categories:
        items = search_naver_items(cat, display=fetch_count_per_cat)
        cat_items_map[cat] = items or []

    # 1단계: 각 카테고리별 최소 1개씩 중복 없이 추가
    for cat in categories:
        items = cat_items_map[cat]
        for item in items:
            link = item.get('link')
            if link and link not in seen_links:
                recommendation_items.append(item)
                seen_links.add(link)
                break

    # 2단계: 남은 슬롯 채우기 (전체 카테고리 아이템 순회하며 중복 없이 추가)
    if len(recommendation_items) < 5:
        for cat in categories:
            items = cat_items_map[cat]
            for item in items:
                if len(recommendation_items) >= 5:
                    break
                link = item.get('link')
                if link and link not in seen_links:
                    recommendation_items.append(item)
                    seen_links.add(link)

    # 결과 최대 5개
    recommendation_items = recommendation_items[:5]
    return {
        'age' : int(round(predicted_age * (60-10) +10, 1)), #역정규화..
        'gender' : predicted_gender ,
        'emotion' : emotion, 
        'recommendationtext': recommendation_text, #summary부분
        "recommendationItems": recommendation_items #추천상품
    }
        


