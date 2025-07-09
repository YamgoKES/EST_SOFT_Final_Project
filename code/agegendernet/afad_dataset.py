import torch
from torch.utils.data import Dataset
from PIL import Image
import pandas as pd
import torchvision.transforms as transforms

class AFADDataset(Dataset):
    def __init__(self, dataframe, transform=None):
        self.data = dataframe
        self.transform = transform
        self.gender_map = {'male': 0, 'female': 1}

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        row = self.data.iloc[idx]
        image = Image.open(row['image_path']).convert("RGB")
        age = int(row['age'])
        gender = self.gender_map[row['gender']]

        if self.transform:
            image = self.transform(image)

        # 나이와 성별을 함께 반환 (Multitask)
        return image, {'age': age, 'gender': gender}

if __name__ == "__main__":
    from afad_load import load_afad_dataset

    df = load_afad_dataset("data/AFAD-Full")

    transform = transforms.Compose([
        transforms.Resize((128, 128)),
        transforms.ToTensor()
    ])

    dataset = AFADDataset(df, transform=transform)
    img, labels = dataset[0]
    print(f"Image shape: {img.shape}, Labels: {labels}")