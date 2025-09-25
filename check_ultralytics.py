import torch
from ultralytics import YOLO

print("=== Ultralytics GPU Detection ===")

# 检查PyTorch GPU
print(f"PyTorch version: {torch.__version__}")
print(f"CUDA available: {torch.cuda.is_available()}")

if torch.cuda.is_available():
    print(f"GPU count: {torch.cuda.device_count()}")
    print(f"GPU name: {torch.cuda.get_device_name(0)}")

# 检查Ultralytics
print(f"\nUltralytics version: {YOLO.__module__}")

# 创建一个简单的YOLO模型实例来测试
try:
    model = YOLO('yolo11n.pt')  # 使用nano版本，下载快
    print("✅ YOLO模型加载成功")
    
    # 检查模型是否在GPU上
    if torch.cuda.is_available():
        model.cuda()
        print("✅ 模型已移动到GPU")
    
    # 创建一个测试图像张量
    test_image = torch.randn(1, 3, 640, 640)
    if torch.cuda.is_available():
        test_image = test_image.cuda()
        print("✅ 测试图像已移动到GPU")
    
    # 简单的推理测试
    with torch.no_grad():
        results = model(test_image)
    print("✅ 推理测试成功")
    
except Exception as e:
    print(f"❌ 测试失败: {e}")

print("\n=== Ultralytics Detection Complete ===")