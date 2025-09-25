FROM nvidia/cuda:11.8.0-runtime-ubuntu20.04 AS base

# 国内镜像源
ARG USE_CHINA_MIRROR=true

# 设置工作目录
WORKDIR /app

# 安装运行时依赖与 Python 3.10
RUN if [ "$USE_CHINA_MIRROR" = "true" ]; then \
        sed -i 's@//.*archive.ubuntu.com@//mirrors.ustc.edu.cn@g' /etc/apt/sources.list && \
        sed -i 's@//.*security.ubuntu.com@//mirrors.ustc.edu.cn@g' /etc/apt/sources.list; \
    fi && \
    apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    tzdata \
    curl \
    ca-certificates \
    software-properties-common \
    libgl1 \
    libglib2.0-0 \
    && add-apt-repository -y ppa:deadsnakes/ppa \
    && apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    python3.10 \
    python3.10-venv \
    python3.10-distutils \
    && python3.10 -m ensurepip --upgrade \
    && ln -fs /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && dpkg-reconfigure -f noninteractive tzdata \
    && apt-get remove -y software-properties-common \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

FROM base AS builder

ARG USE_CHINA_MIRROR=true

# 构建阶段安装最小化编译工具
RUN if [ "$USE_CHINA_MIRROR" = "true" ]; then \
        sed -i 's@//.*archive.ubuntu.com@//mirrors.ustc.edu.cn@g' /etc/apt/sources.list && \
        sed -i 's@//.*security.ubuntu.com@//mirrors.ustc.edu.cn@g' /etc/apt/sources.list; \
    fi && \
    apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN python3.10 -m venv /opt/venv && \
    /opt/venv/bin/python -m ensurepip --upgrade
ENV PATH="/opt/venv/bin:$PATH"

RUN pip install --no-cache-dir --upgrade pip setuptools wheel

COPY requirements.txt .

RUN if [ "$USE_CHINA_MIRROR" = "true" ]; then \
        pip install --no-cache-dir torch torchvision --index-url https://mirrors.nju.edu.cn/pytorch/whl/cu118 && \
        pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt; \
    else \
        pip install --no-cache-dir torch torchvision --index-url https://download.pytorch.org/whl/cu118 && \
        pip install --no-cache-dir -r requirements.txt; \
    fi

FROM base AS runtime

ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

COPY --from=builder /opt/venv /opt/venv
COPY . .

# 默认命令
CMD ["/opt/venv/bin/python", "--version"]
