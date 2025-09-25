FROM nvidia/cuda:11.8.0-devel-ubuntu20.04

# 国内镜像源
ARG USE_CHINA_MIRROR=true

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN if [ "$USE_CHINA_MIRROR" = "true" ]; then \
        sed -i 's@//.*archive.ubuntu.com@//mirrors.ustc.edu.cn@g' /etc/apt/sources.list && \
        sed -i 's@//.*security.ubuntu.com@//mirrors.ustc.edu.cn@g' /etc/apt/sources.list; \
    fi && \
    apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    git \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# 创建Python3符号链接
RUN ln -s /usr/bin/python3 /usr/bin/python

# 复制requirements文件
COPY requirements.txt .

# 安装Python依赖
RUN if [ "$USE_CHINA_MIRROR" = "true" ]; then \
        pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt; \
    else \
        pip install --no-cache-dir -r requirements.txt; \
    fi

# 复制项目文件
COPY . .

# 设置环境变量
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# 默认命令
CMD ["python", "--version"]