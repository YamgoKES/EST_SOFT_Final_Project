import torch
import torch.nn as nn

class BasicBlock(nn.Module):
    expansion = 1
    def __init__(self, inplanes, planes, stride=1, downsample=None):
        super().__init__()
        self.conv1 = nn.Conv2d(inplanes, planes, 3, stride, 1, bias=False)
        self.bn1 = nn.BatchNorm2d(planes)
        self.relu = nn.ReLU(inplace=True)
        self.conv2 = nn.Conv2d(planes, planes, 3, 1, 1, bias=False)
        self.bn2 = nn.BatchNorm2d(planes)
        self.downsample = downsample

    def forward(self, x):
        identity = x
        out = self.relu(self.bn1(self.conv1(x)))
        out = self.bn2(self.conv2(out))
        if self.downsample:
            identity = self.downsample(x)
        out += identity
        return self.relu(out)


class ResNet_AT_Attention(nn.Module):
    def __init__(self, block, layers, num_classes=4, dropout_rate=0.3):
        super().__init__()
        self.inplanes = 64

        self.conv1 = nn.Conv2d(3, 64, 7, 2, 3, bias=False)
        self.bn1 = nn.BatchNorm2d(64)
        self.relu = nn.ReLU(inplace=True)
        self.maxpool = nn.MaxPool2d(3, 2, 1)

        self.layer1 = self._make_layer(block, 64, layers[0])
        self.layer2 = self._make_layer(block, 128, layers[1], 2)
        self.layer3 = self._make_layer(block, 256, layers[2], 2)
        self.layer4 = self._make_layer(block, 512, layers[3], 2)

        self.dropout1 = nn.Dropout(dropout_rate)
        self.dropout2 = nn.Dropout(dropout_rate)
        self.dropout3 = nn.Dropout(dropout_rate)

        self.avgpool = nn.AdaptiveAvgPool2d(1)
        self.dropout = nn.Dropout(dropout_rate)

        self.alpha = nn.Sequential(
            nn.Linear(512, 1),
            nn.Sigmoid()
        )

        self.pred_fc1 = nn.Linear(512, num_classes)

    def _make_layer(self, block, planes, blocks, stride=1):
        downsample = None
        if stride != 1 or self.inplanes != planes * block.expansion:
            downsample = nn.Sequential(
                nn.Conv2d(self.inplanes, planes * block.expansion, 1, stride, bias=False),
                nn.BatchNorm2d(planes * block.expansion),
            )
        layers = [block(self.inplanes, planes, stride, downsample)]
        self.inplanes = planes * block.expansion
        for _ in range(1, blocks):
            layers.append(block(self.inplanes, planes))
        return nn.Sequential(*layers)

    def forward(self, x=None, phrase="eval", AT_level="first_level", vm=None):
        if phrase == "eval" and AT_level == "first_level":
            x = self.relu(self.bn1(self.conv1(x)))
            x = self.maxpool(x)
            x = self.layer1(x)
            x = self.layer2(x)
            x = self.dropout1(x)
            x = self.layer3(x)
            x = self.dropout2(x)
            x = self.layer4(x)
            x = self.dropout3(x)
            x = self.avgpool(x).squeeze(-1).squeeze(-1)
            alpha = self.alpha(self.dropout(x))
            return x, alpha

        elif phrase == "eval" and AT_level == "pred":
            return self.pred_fc1(self.dropout(vm))
        else:
            raise ValueError("Invalid phrase or AT_level")


def get_emotion_model(weight_path, device=None):
    if device is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"
    model = ResNet_AT_Attention(block=BasicBlock, layers=[2, 2, 2, 2], num_classes=4, dropout_rate=0.3)
    checkpoint = torch.load(weight_path, map_location=device)
    model.load_state_dict(checkpoint)
    model = model.to(device)
    model.eval()
    return model
