import io
import base64
from typing import List
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from PIL import Image
from ultralytics import YOLO
import uvicorn

app = FastAPI()
model = YOLO('yolo11n.pt')


def base64_to_image(base64_str: str) -> Image.Image:
    if 'base64,' in base64_str:
        base64_str = base64_str.split('base64,')[1]
    image_data = base64.b64decode(base64_str)
    return Image.open(io.BytesIO(image_data))


def image_to_base64(image: Image.Image) -> str:
    buffer = io.BytesIO()
    image.save(buffer, format='JPEG')
    return f"data:image/jpeg;base64,{base64.b64encode(buffer.getvalue()).decode()}"


def process_results(results) -> List[dict]:
    detections = []
    for r in results:
        if r.boxes:
            for i, box in enumerate(r.boxes):
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                conf = float(box.conf.item())
                cls = int(box.cls.item())
                detections.append({
                    'id': i + 1,
                    'class_name': r.names[cls],
                    'confidence': round(conf, 3),
                    'bbox': {
                        'x1': float(x1), 'y1': float(y1),
                        'x2': float(x2), 'y2': float(y2),
                        'width': float(x2 - x1), 'height': float(y2 - y1)
                    }
                })
    return detections


@app.post("/detect")
async def detect_base64(data: dict):
    try:
        if 'image' not in data:
            raise HTTPException(status_code=400, detail="缺少图片数据")
        
        image = base64_to_image(data['image'])
        confidence = data.get('confidence', 0.5)
        results = model(image, conf=confidence)
        
        annotated_image = image_to_base64(Image.fromarray(results[0].plot()))
        detections = process_results(results)
        
        return {
            "success": True,
            "detections_count": len(detections),
            "detections": detections,
            "annotated_image": annotated_image
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"处理失败: {str(e)}")


@app.post("/detect/file")
async def detect_file(file: UploadFile = File(...), confidence: float = Form(0.5)):
    try:
        image = Image.open(io.BytesIO(await file.read()))
        results = model(image, conf=confidence)
        
        annotated_image = image_to_base64(Image.fromarray(results[0].plot()))
        detections = process_results(results)
        
        return {
            "success": True,
            "filename": file.filename,
            "detections_count": len(detections),
            "detections": detections,
            "annotated_image": annotated_image
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"处理失败: {str(e)}")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)