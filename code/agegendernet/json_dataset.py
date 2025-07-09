import os
import json
import chardet
from torch.utils.data import Dataset

class JSONDataset(Dataset):
    def __init__(self, json_path, image_root=None, transform=None):
        self.transform = transform
        self.image_root = image_root
        self.samples = []

        # 인코딩 자동 감지
        with open(json_path, 'rb') as f:
            raw_data = f.read()
            result = chardet.detect(raw_data)
            encoding = result['encoding']

        # 감지된 인코딩으로 JSON 읽기
        with open(json_path, 'r', encoding=encoding) as f:
            data = json.load(f)

        # gender: '남'/'여' 대응 처리
        for item in data:
            filename = item.get("filename")
            age = item.get("age")
            gender_str = item.get("gender")

            if filename is None or age is None or gender_str not in ["남", "여"]:
                continue

            gender = 0 if gender_str == "남" else 1
            self.samples.append((filename, age, gender))

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        filename, age, gender = self.samples[idx]
        return {"filename": filename, "age": age, "gender": gender}

# 테스트: 라벨 정보만 출력
if __name__ == "__main__":
    json_path = os.path.join("data", "json", "train_sadness.json")

    dataset = JSONDataset(
        json_path=json_path,
        image_root=None,
        transform=None
    )

    print(f"전체 샘플 수: {len(dataset)}\n")

    for i in range(min(3, len(dataset))):
        sample = dataset[i]
        print(f"샘플 {i+1}")
        print(f" - 파일명: {sample['filename']}")
        print(f" - 나이: {sample['age']}")
        print(f" - 성별: {'남자' if sample['gender'] == 0 else '여자'}")
        print("------")