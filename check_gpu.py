import torch

print("=== PyTorch GPU Detection ===")
print(f"PyTorch version: {torch.__version__}")
print(f"CUDA available: {torch.cuda.is_available()}")

if torch.cuda.is_available():
    print(f"GPU count: {torch.cuda.device_count()}")
    print(f"Current GPU: {torch.cuda.current_device()}")
    print(f"GPU name: {torch.cuda.get_device_name(0)}")
    
    # 测试张量是否能移动到GPU
    test_tensor = torch.randn(3, 3)
    print(f"\nTest tensor on CPU: {test_tensor.device}")
    
    gpu_tensor = test_tensor.cuda()
    print(f"Test tensor on GPU: {gpu_tensor.device}")
    print("✅ GPU 正在工作中!")
else:
    print("❌ 未检测到GPU, 只有CPU正在工作")

print("\n=== Detection Complete ===")