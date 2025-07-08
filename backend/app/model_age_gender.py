import torch
import torch.nn as nn
from torchvision.models import resnet50
import os

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model_e_v1 = resnet50(pretrained=False)
model_e_v1.fc = nn.Sequential(
    nn.Linear(model_e_v1.fc.in_features,256),
    nn.BatchNorm1d(256),
    nn.ReLU(),
    nn.Dropout(0.4),
    
    nn.Linear(256,128),
    nn.BatchNorm1d(128),
    nn.ReLU(),
    nn.Dropout(0.3),
    
    nn.Linear(128,64),
    nn.BatchNorm1d(64),
    nn.ReLU(),
    nn.Dropout(0.2),
    
    nn.Linear(64,3)
)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.abspath(os.path.join(BASE_DIR, '..', 'trained', 'model_e_v1.pth'))

model_e_v1.load_state_dict(torch.load(MODEL_PATH, map_location=device))

model_e_v1.to(device)

model_e_v1.eval()