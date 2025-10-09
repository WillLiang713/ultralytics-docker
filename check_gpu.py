import torch

print("=== PyTorch GPU 检测 ===")
print(f"PyTorch 版本: {torch.__version__}")
print(f"CUDA 可用: {torch.cuda.is_available()}")

if torch.cuda.is_available():
    print(f"GPU 数量: {torch.cuda.device_count()}")
    print(f"当前 GPU: {torch.cuda.current_device()}")
    print(f"GPU 名称: {torch.cuda.get_device_name(0)}")
    
    # 测试张量是否能移动到GPU
    test_tensor = torch.randn(3, 3)
    print(f"\n测试张量在 CPU 上: {test_tensor.device}")
    
    gpu_tensor = test_tensor.cuda()
    print(f"测试张量在 GPU 上: {gpu_tensor.device}")
    print("✅ GPU 正在工作中!")
else:
    print("❌ 未检测到GPU, 只有CPU正在工作")

print("\n=== 检测完成 ===")