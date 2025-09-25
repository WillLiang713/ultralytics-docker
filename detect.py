import os
from ultralytics import YOLO

# 设置参数
CONFIDENCE_THRESHOLD = 0.5  # 置信度阈值，只显示高于此值的检测结果
output_dir = 'output_results'

# 创建输出目录
os.makedirs(output_dir, exist_ok=True)

# 加载训练好的模型
model = YOLO('yolo11n.pt')

# 进行预测（带置信度过滤）
results = model('test_images', conf=CONFIDENCE_THRESHOLD)

# 保存和显示结果
for i, r in enumerate(results):
    # 打印检测信息
    print(f"\n📸 图片 {i+1} 检测结果:")
    print(f"置信度阈值: {CONFIDENCE_THRESHOLD}")
    
    if r.boxes:
        print(f"检测到 {len(r.boxes)} 个目标:")
        for j, box in enumerate(r.boxes):
            conf = box.conf.item()
            cls = int(box.cls.item())
            class_name = r.names[cls]
            print(f"  目标 {j+1}: {class_name} (置信度: {conf:.3f})")
    else:
        print("未检测到任何目标")
    
    # 保存带检测框的图片
    output_path = os.path.join(output_dir, f'detected_{i}.jpg')
    r.save(output_path)
    print(f"✅ 结果已保存: {output_path}")
    
    # 显示结果（如果环境支持）
    try:
        r.show()
    except:
        print("ℹ️  无法显示图片，请查看保存的文件")

print(f"\n🎉 所有检测结果已保存到 '{output_dir}' 文件夹中")
print(f"📊 置信度阈值设置为: {CONFIDENCE_THRESHOLD}")