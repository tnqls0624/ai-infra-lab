# syntax=docker/dockerfile:1

# =========================
# 1. Dependency builder
# =========================
FROM nvidia/cuda:12.4.1-runtime-ubuntu22.04 AS builder

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-venv \
    && rm -rf /var/lib/apt/lists/*

# 설치된 패키지를 한 번에 복사할 수 있도록 가상환경 사용
RUN python3 -m venv /opt/venv

ENV PATH="/opt/venv/bin:${PATH}"

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir \
        torch==2.12.1 \
        torchvision==0.27.1 \
        --index-url https://download.pytorch.org/whl/cpu

# =========================
# 2. Runtime
# =========================
FROM nvidia/cuda:12.4.1-runtime-ubuntu22.04 AS runner

ENV DEBIAN_FRONTEND=noninteractive

# 최종 이미지에는 pip, venv 설치 도구가 필요 없음
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        python3 \
        ca-certificates \
        libgomp1 \
    && rm -rf /var/lib/apt/lists/*

ENV PATH="/opt/venv/bin:${PATH}" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

COPY --from=builder /opt/venv /opt/venv
COPY python/W1/D5/train_mnist.py ./train_mnist.py

CMD ["python", "train_mnist.py", "--epochs", "1"]