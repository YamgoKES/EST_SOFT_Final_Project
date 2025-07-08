import torch
import torch.nn.functional as F
from torchvision import transforms
from PIL import Image
import json
from .EA_model import get_emotion_model
from ultralytics import YOLO
import numpy as np

class EmotionFANPredictor_Attention:
    def __init__(self, model_path, norm_path="custom_norm.json", device=None, face_model_path=None, use_face_crop=True):
        # 자동 device 설정 (cuda or cpu)
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.model = get_emotion_model(weight_path=model_path, device=self.device)
        self.use_face_crop = use_face_crop
        self.face_detector = YOLO(face_model_path) if face_model_path else None

        # 정규화 값 로딩
        try:
            with open(norm_path, "r") as f:
                norm_stats = json.load(f)
        except FileNotFoundError:
            print(f"⚠ 정규화 파일 {norm_path} 없음. 기본값 사용.")
            norm_stats = {"mean": [0.485, 0.456, 0.406], "std": [0.229, 0.224, 0.225]}

        mean = norm_stats.get("mean", [0.485, 0.456, 0.406])
        std = norm_stats.get("std", [0.229, 0.224, 0.225])

        # 이미지 전처리 파이프라인 구성
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=mean, std=std),
        ])

        self.label_map = {
            0: "anger",
            1: "happy",
            2: "panic",
            3: "sadness"
        }

    def predict(self, image_input):
        if isinstance(image_input, str):
            image = Image.open(image_input).convert('RGB')
        elif isinstance(image_input, Image.Image):
            image = image_input.convert('RGB')
        else:
            raise ValueError("Input must be a file path or PIL Image")

        if self.use_face_crop and self.face_detector:
            img_np = np.array(image)
            results = self.face_detector(img_np, verbose=False)[0]

            if results.boxes is not None and len(results.boxes) > 0:
                # box 좌표, confidence 추출
                boxes = results.boxes.xyxy.cpu().numpy()
                scores = results.boxes.conf.cpu().numpy()

                # confidence ≥ 0.7 필터링
                valid = [(b, s) for b, s in zip(boxes, scores) if s >= 0.7]

                if valid:
                    # 신뢰도 가장 높은 박스 선택
                    best_box = max(valid, key=lambda x: x[1])[0]
                    x1, y1, x2, y2 = map(int, best_box)
                    image = image.crop((x1, y1, x2, y2))

        image_tensor = self.transform(image).unsqueeze(0).to(self.device)

        with torch.no_grad():
            vm, alpha = self.model(image_tensor, phrase="eval", AT_level="first_level")
            output = self.model(phrase="eval", AT_level="pred", vm=vm)
            probs = F.softmax(output, dim=1).cpu().numpy().flatten()
            pred_label = int(probs.argmax())
            pred_name = self.label_map[pred_label]
            alpha_value = float(alpha.squeeze().cpu().item())

        result = {
            "emotion": pred_name,
            "probability": {self.label_map[i]: float(p) for i, p in enumerate(probs)},
            "alpha": alpha_value
        }
        return result

    def __call__(self, image_input):
        return self.predict(image_input)
