import torch
import torch.nn as nn
from torchvision import transforms
from PIL import Image

# 1. 모델 정의 (학습 때와 동일하게)
class AgeGenderNet(nn.Module):
    def __init__(self):
        super(AgeGenderNet, self).__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 16, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(16, 32, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
        )
        self.flatten = nn.Flatten()
        self.age_head = nn.Linear(32 * 32 * 32, 1)
        self.gender_head = nn.Linear(32 * 32 * 32, 2)

    def forward(self, x):
        x = self.features(x)
        x = self.flatten(x)
        age = self.age_head(x).squeeze()
        gender = self.gender_head(x)
        return age, gender

# 2. 이미지 전처리 함수
def preprocess_image(image_path):
    transform = transforms.Compose([
        transforms.Resize((128, 128)),
        transforms.ToTensor()
    ])
    image = Image.open(image_path).convert("RGB")
    return transform(image).unsqueeze(0)

# 3. 예측 실행
if __name__ == "__main__":
    test_image_path = "test_image/test(1).jpg"  # 예시 경로
    model_path = "agegender_model.pth"

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # 모델 불러오기
    model = AgeGenderNet()
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.to(device)
    model.eval()

    # 이미지 불러오기 및 예측
    image_tensor = preprocess_image(test_image_path).to(device)

    with torch.no_grad():
        age_output, gender_output = model(image_tensor)
        predicted_age = int(age_output.item())
        predicted_gender = "남성" if torch.argmax(gender_output).item() == 0 else "여성"

    print("예측 결과")
    print(f"  - 나이: {predicted_age}세")
    print(f"  - 성별: {predicted_gender}")