from PIL import Image,ImageOps
from torchvision import transforms
from ultralytics import YOLO
from huggingface_hub import hf_hub_download

yolo_model_path = hf_hub_download(repo_id="arnabdhar/YOLOv8-Face-Detection", filename="model.pt")

transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406],
                         [0.229, 0.224, 0.225])
])

class YoloTransform:
    def __init__(self, yolo_model_path=None, conf_threshold=0.7, transform=None) :
        
        self.model=YOLO(yolo_model_path)
        self.conf_threshold=conf_threshold
        self.transform=transform
        
    
    def detect_best_cropping(self, image: Image.Image) :
        image = ImageOps.exif_transpose(image).convert("RGB")
        #yolo추론
        results = self.model(image)
        boxes = results[0].boxes.xyxy
        confs = results[0].boxes.conf
        
        best_box=None
        best_conf=-1
        
        for box, conf in zip(boxes,confs) :
            if conf >=self.conf_threshold and conf>best_conf :
                best_box=box
                best_conf =conf 
                
        
        if best_box is not None :
            x1,y1,x2,y2 = map(int, best_box)
            face_crop = image.crop((x1,y1,x2,y2)).resize((224,224))
        else :
            face_crop = image.resize((224,224))
        
        return self.transform(face_crop).unsqueeze(0)