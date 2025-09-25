# Ultralytics Docker

一个用于运行 Ultralytics YOLO 目标检测模型的 Docker 容器化解决方案。

## 项目描述

此项目提供了预配置的 Docker 环境，用于快速部署和运行 Ultralytics YOLO 模型，支持目标检测、实例分割和图像分类任务。

## 功能特性

- 🚀 预配置的 Ultralytics 环境
- 📦 包含常用的深度学习依赖
- 🔧 支持 GPU 加速 (CUDA 11.8)
- 📊 模型训练和推理支持
- 🐳 容器化部署
- 📁 数据集挂载支持
- 💾 镜像大小优化

## 快速开始

### 前提条件

- Docker 和 Docker Compose 已安装
- NVIDIA Container Toolkit 已安装（用于 GPU 支持）

### 1. 准备数据集（可选）

在项目目录下创建 `datasets` 文件夹，或挂载现有数据集：
```bash
mkdir datasets
# 将你的数据集放入 datasets/ 文件夹
```

### 2. 构建和启动

```bash
# 构建镜像并启动容器
docker-compose up --build

# 后台运行
docker-compose up -d

# 停止服务
docker-compose down
```

### 3. 进入容器

```bash
# 进入容器交互模式
docker-compose exec ultralytics bash

# 或直接运行Python脚本
docker-compose exec ultralytics python your_script.py
```

## 使用示例

### 基础训练脚本

创建 `train.py` 文件：
```python
from ultralytics import YOLO

# 加载预训练模型（首次使用自动下载）
model = YOLO('yolo11n.pt')

# 使用数据集进行训练
model.train(data='/datasets/your_dataset/data.yaml', epochs=100)

# 保存训练结果
model.save('my_model.pt')
```

### 推理示例
```python
from ultralytics import YOLO

# 加载训练好的模型
model = YOLO('my_model.pt')

# 进行预测
results = model('/datasets/test_images/')
for r in results:
    r.show()  # 显示结果
```

### 验证环境
```python
import torch
print(f"CUDA available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"Current GPU: {torch.cuda.get_device_name(0)}")
```

## 目录结构

```
ultralytics-docker/
├── Dockerfile              # Docker 构建文件
├── docker-compose.yml      # Docker Compose 配置
├── requirements.txt        # Python 依赖
├── .dockerignore          # Docker 忽略文件
├── .gitignore             # Git 忽略文件
├── datasets/              # 数据集文件夹（本地挂载）
└── your_scripts/          # 你的Python脚本
```

## 数据集挂载

容器内可通过 `/datasets` 路径访问数据集：
- 训练配置：`/datasets/your_dataset/data.yaml`
- 训练数据：`/datasets/your_dataset/images/`
- 测试结果：`/datasets/your_dataset/test/`

## 预训练模型

首次使用时会自动下载到容器的 `~/.cache/ultralytics/` 目录：
- `yolo11n.pt` -  Nano 模型（最小最快）
- `yolo11s.pt` - Small 模型
- `yolo11m.pt` - Medium 模型
- `yolo11l.pt` - Large 模型
- `yolo11x.pt` - Extra 模型（最大最准）

## 常用命令

```bash
# 查看日志
docker-compose logs -f

# 重新构建镜像
docker-compose build --no-cache

# 清理容器和镜像
docker-compose down --rmi all

# 进入Python交互模式
docker-compose exec ultralytics python
```

## 故障排除

### GPU不可用
确保已安装 NVIDIA Container Toolkit：
```bash
sudo apt-get install -y nvidia-container-toolkit
sudo systemctl restart docker
```

### 权限问题
```bash
# 添加用户到docker组
sudo usermod -aG docker $USER
# 重新登录后生效
```

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License