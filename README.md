# Ultralytics Docker

一个用于运行 Ultralytics YOLO 目标检测模型的 Docker 容器化解决方案。

## 项目描述

此项目提供了预配置的 Docker 环境，用于快速部署和运行 Ultralytics YOLO 模型，支持目标检测、实例分割和图像分类任务。

## 功能特性

- 🚀 预配置的 Ultralytics 环境
- 📦 包含常用的深度学习依赖
- 🔧 支持 GPU 加速
- 📊 模型训练和推理支持
- 🐳 容器化部署

## 快速开始

### 前提条件

- Docker 已安装
- 可选：NVIDIA Docker 运行时（用于 GPU 支持）

### 构建镜像

```bash
docker build -t ultralytics-docker .
```

### 运行容器

```bash
# CPU 版本
docker run -it --rm ultralytics-docker

# GPU 版本（需要 NVIDIA Docker）
docker run -it --rm --gpus all ultralytics-docker
```

## 使用示例

在容器内运行 YOLO 模型：

```python
from ultralytics import YOLO

# 加载预训练模型
model = YOLO('yolov8n.pt')

# 进行目标检测
results = model('path/to/image.jpg')
results[0].show()
```

## 项目结构

```
ultralytics-docker/
├── Dockerfile          # Docker 构建文件
├── requirements.txt    # Python 依赖
├── scripts/           # 实用脚本
├── models/           # 模型文件
└── README.md         # 项目说明
```

## 配置

### 环境变量

- `MODEL_PATH`: 模型文件路径
- `DATA_DIR`: 数据目录
- `GPU_ENABLED`: 是否启用 GPU

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License