FROM nvidia/cuda:12.4.1-runtime-ubuntu22.04

WORKDIR /app

# 베이스 이미지에 파이썬 없음 → apt로 설치. 목록 캐시 삭제로 레이어 경량화
RUN apt-get update && apt-get install -y python3 python3-pip && rm -rf /var/lib/apt/lists/*

# CPU wheel 인덱스 — CUDA wheel(~2.5GB) 대신 경량 빌드. GPU 전환은 Block 2에서
# pip 설치를 소스 COPY보다 앞에 두어 소스 수정 시에도 이 레이어의 캐시 유지
RUN pip3 install --no-cache-dir torch torchvision --index-url https://download.pytorch.org/whl/cpu

COPY python/W1/D5/train_mnist.py .

CMD ["python3", "train_mnist.py", "--epochs", "1"]
