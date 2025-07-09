import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader
from torchvision import transforms

from afad_load import load_afad_dataset
from afad_dataset import AFADDataset

# 1. 데이터 로딩 및 분할
df = load_afad_dataset("data/AFAD-Full")
train_df, val_df = train_test_split(df, test_size=0.2, random_state=42)

transform = transforms.Compose([
    transforms.Resize((128, 128)),
    transforms.ToTensor()
])
train_dataset = AFADDataset(train_df, transform=transform)
val_dataset = AFADDataset(val_df, transform=transform)
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False)

# 2. 모델 정의
class AgeGenderNet(nn.Module):
    def __init__(self):
        super(AgeGenderNet, self).__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 16, 3, 1, 1), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(16, 32, 3, 1, 1), nn.ReLU(), nn.MaxPool2d(2),
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

# 3. 학습 설정
model = AgeGenderNet()
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
optimizer = optim.Adam(model.parameters(), lr=0.001)
age_criterion = nn.MSELoss()
gender_criterion = nn.CrossEntropyLoss()

# 4. 학습 루프 (Epoch 9회)
for epoch in range(9):
    model.train()
    total_loss = 0
    correct_gender, total_gender = 0, 0
    age_preds, age_labels = [], []

    for images, labels in train_loader:
        images = images.to(device)
        age = labels['age'].float().to(device)
        gender = labels['gender'].to(device)

        optimizer.zero_grad()
        age_out, gender_out = model(images)
        loss = age_criterion(age_out, age) + gender_criterion(gender_out, gender)
        loss.backward()
        optimizer.step()

        total_loss += loss.item()
        _, pred_gender = torch.max(gender_out, 1)
        correct_gender += (pred_gender == gender).sum().item()
        total_gender += gender.size(0)
        age_preds.extend(age_out.detach().cpu().numpy())
        age_labels.extend(age.cpu().numpy())

    train_acc = 100 * correct_gender / total_gender
    train_mae = mean_absolute_error(age_labels, age_preds)
    train_rmse = np.sqrt(mean_squared_error(age_labels, age_preds))
    train_within5 = np.mean(np.abs(np.array(age_preds) - np.array(age_labels)) <= 5)

    # 5. 검증 (Validation)
    model.eval()
    val_gender_correct, val_gender_total = 0, 0
    val_age_preds, val_age_labels = [], []
    with torch.no_grad():
        for images, labels in val_loader:
            images = images.to(device)
            age = labels['age'].float().to(device)
            gender = labels['gender'].to(device)

            age_out, gender_out = model(images)
            _, pred_gender = torch.max(gender_out, 1)
            val_gender_correct += (pred_gender == gender).sum().item()
            val_gender_total += gender.size(0)
            val_age_preds.extend(age_out.cpu().numpy())
            val_age_labels.extend(age.cpu().numpy())

    val_acc = 100 * val_gender_correct / val_gender_total
    val_mae = mean_absolute_error(val_age_labels, val_age_preds)
    val_rmse = np.sqrt(mean_squared_error(val_age_labels, val_age_preds))
    val_within5 = np.mean(np.abs(np.array(val_age_preds) - np.array(val_age_labels)) <= 5)

    print(f"\n Epoch {epoch+1}")
    print(f" Train Loss: {total_loss:.4f}")
    print(f"  성별 정확도: {train_acc:.2f}% | 나이 MAE: {train_mae:.2f} | RMSE: {train_rmse:.2f} | ±5세 정확도: {train_within5:.2f}")
    print(f"  Val 성별 정확도: {val_acc:.2f}% | 나이 MAE: {val_mae:.2f} | RMSE: {val_rmse:.2f} | ±5세 정확도: {val_within5:.2f}")

    torch.save(model.state_dict(), "agegender_model.pth")
    print(" 모델 'agegender_model.pth' 저장완료")