import json
from openai import OpenAI
import pandas as pd
from datetime import datetime

emotion_labels = {
    'happy': '기쁨',
    'sadness': '슬픔',
    'anger': '화남',
    'panic': '놀람/당황'
}

def load_openai_key(path):
    try:
        with open(path, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        raise RuntimeError(f"❌ OpenAI API 키 파일이 존재하지 않습니다: {path}")

def get_main_emotion(json_path):
    """
    result.json처럼 단일 결과 구조인 경우에 맞춰 감정 추출
    {
        "emotion": "happy",
        "probability": { ... },
        "alpha": ...
    }
    """
    with open(json_path, "r") as f:
        data = json.load(f)
    return data["emotion"] 


def get_gender_age(csv_path):
    df = pd.read_csv(csv_path)
    if '예측 성별' not in df.columns or '예측 나이' not in df.columns:
        raise ValueError("❌ '예측 성별' 또는 '예측 나이' 컬럼이 누락되었습니다.")
    if df.empty:
        raise ValueError("❌ 입력 CSV가 비어 있습니다.")
    gender = df.iloc[0]['예측 성별']
    age = df.iloc[0]['예측 나이']
    return gender, age

def build_prompt_v2(emotion, gender, age, feel_mode=None): #추가 
    today = datetime.today().strftime("%Y-%m-%d")

    emotion_context_map = {
        "express": {
            "anger": "사용자가 현재 '화남' 감정을 느끼고 있으며, 이 감정을 분출하거나 강하게 표현하고 싶어 합니다. 스트레스를 발산하거나 직접적인 에너지 소비로 풀어낼 수 있는 아이템을 추천해주세요.",
            "happy": "사용자가 현재 '기쁨' 감정을 느끼고 있으며, 이 기쁜 감정을 주변과 공유하고 더 크게 표현하고 싶어 합니다. 축하하거나 즐거운 분위기를 확장시켜줄 아이템을 추천해주세요.",
            "panic": "사용자가 현재 '놀람/당황' 감정을 느끼고 있으며, 이 감정을 웃음이나 표현을 통해 털어내고 싶어 합니다. 긴장을 전환시키거나 유쾌하게 승화시킬 수 있는 아이템을 추천해주세요.",
            "sadness": "사용자가 현재 '슬픔' 감정을 느끼고 있으며, 이 감정을 자연스럽게 표현하거나 감정에 몰입해 위로받고 싶어 합니다. 감성을 자극하거나 감정을 공감할 수 있는 아이템을 추천해주세요."
        },
        "calmdown": {
            "anger": "사용자가 현재 '화남' 감정을 느끼고 있으며, 이 감정을 진정시키고 마음을 가라앉히고자 합니다. 분노를 누그러뜨리고 감정을 안정시켜 줄 수 있는 아이템을 추천해주세요.",
            "happy": "사용자가 현재 '기쁨' 감정을 느끼고 있으며, 이 감정을 조용히 음미하고 스스로 만족하고 싶어 합니다. 혼자만의 여유와 기쁨을 유지할 수 있는 차분한 아이템을 추천해주세요.",
            "panic": "사용자가 현재 '놀람/당황' 감정을 느끼고 있으며, 이 감정을 진정시키고 평온하게 되돌아가고자 합니다. 마음을 차분하게 하고 안정을 줄 수 있는 아이템을 추천해주세요.",
            "sadness": "사용자가 현재 '슬픔' 감정을 느끼고 있으며, 이 감정을 이겨내고 위로받고자 합니다. 마음을 따뜻하게 하고 안정감을 줄 수 있는 힐링 아이템을 추천해주세요."
        }
    }

    emotion_ko = emotion_labels.get(emotion, emotion)
    emotion_context = emotion_context_map.get(feel_mode, {}).get(emotion, '')
    
    base_prompt = f"""
한 사람이 '{emotion_ko}' 감정을 느끼고 있습니다. 이 사람의 성별은 {gender}성이고 나이는 {round(age, 0)}세입니다.
오늘 날짜는 {today}이며, 사용자는 한국인입니다.

사용자는 현재 다음과 같은 느낌 상태를 원합니다: {emotion_context}
단계적으로 차례차례 생각하여 답변하세요.
1. 이 감정 상태에 공감하는 자연스러운 대화를 한두 문장으로 생성해주세요.
2. 이 감정, 성별, 나이, 계절에 어울리는 쇼핑 카테고리를 자연스럽게 추천해주세요.
3. 오늘 날짜{today}와 계절을 고려하세요.
4. 유행 아이템도 웹에서 검색하여 고려해주세요.
5. 추천할 카테고리는 실제 쇼핑몰에서 검색 가능한 구체적인 명사 형태여야 합니다.
   반드시 한 줄에 <[카테고리명]> 형식으로 3개만 나열해주세요.
   예시: <[아로마 캔들]>, <[런닝화]>, <[요가매트]>
6. 각 카테고리별로 추천 이유를 간단하게 적어주세요.

다음과 같은 표현은 피하세요.
a. "웹에서 검색한 결과~" 와 같이 다른곳에서 검색했다는 표현 (검색을 하지 말라는게 아닙니다. 검색했다고 얘기하지 말아주세요.)
b. 추천이 너무 뻔하지 않도록 하세요. 가능한 한 신선하거나 감정에 잘 어울리는 색다른 아이디어도 고려해주세요.
c. 반드시 <[카테고리]> 형식만 사용해주세요. 다른 괄호나 텍스트 포맷은 사용하지 마세요.
d. 문장앞에 번호를 매기지 말아주세요.
"""

    # base_prompt += f"\n추가 정보: {emotion_context_map.get(emotion, '')}\n"
    # if feel_mode in feel_mode_context:
    #     base_prompt += f"추가 감정 모드 정보: {feel_mode_context[feel_mode]}\n"
    return base_prompt

def ask_chatgpt(prompt, api_key, model="gpt-4o"):
    client = OpenAI(api_key=api_key)
    try:
        response = client.chat.completions.create(
            model=model,
            temperature=1.2, ### 다양성 추가
            messages=[
                {"role": "system", "content": "You are a shopping category recommender."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        raise RuntimeError(f"❌ OpenAI API 호출 실패: {e}")
