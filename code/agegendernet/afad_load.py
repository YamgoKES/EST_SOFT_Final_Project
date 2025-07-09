import os
import pandas as pd

def load_afad_dataset(root_dir):
    data = []
    valid_exts = ('.jpg', '.jpeg', '.png')  # 🔥 허용 확장자 지정

    for age in os.listdir(root_dir):
        age_path = os.path.join(root_dir, age)
        if not os.path.isdir(age_path):
            continue
        for gender_folder in os.listdir(age_path):
            gender_path = os.path.join(age_path, gender_folder)
            if not os.path.isdir(gender_path):
                continue
            gender = 'male' if gender_folder == '111' else 'female'
            for img_name in os.listdir(gender_path):
                if not img_name.lower().endswith(valid_exts):  # 🔥 이미지 파일만 추가
                    continue
                img_path = os.path.join(gender_path, img_name)
                data.append({
                    'age': int(age),
                    'gender': gender,
                    'image_path': img_path
                })
    return pd.DataFrame(data)

# 실행 테스트용 코드
if __name__ == "__main__":
    df = load_afad_dataset("data/AFAD-Full")
    print(df.head())
    print(f"총 샘플 수: {len(df)}개")