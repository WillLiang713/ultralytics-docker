from ultralytics import YOLO

# 加载预训练模型（首次使用自动下载）
model = YOLO('yolo11n.pt')

# 使用数据集进行训练
model.train(data='/datasets/your_dataset/data.yaml', epochs=100)

# 保存训练结果
model.save('my_model.pt')