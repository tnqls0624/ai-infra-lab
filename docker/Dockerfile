FROM nvidia/cuda:12.4.1-runtime-ubuntu22.04

WORKDIR /app

# TODO: python3 + pip 설치 (베이스에 파이썬 없음 — apt 사용, D3에서 해본 것)
RUN apt install && pip install

# 의도적으로 requirements를 소스보다 먼저 COPY → pip 레이어를 캐시에 태우기 위함
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt --index-url https://download.pytorch.org/whl/cpu

# TODO: train_mnist.py COPY
COPY train_mnist.py .

# TODO: CMD 작성 (컨테이너 시작 시 학습 실행)
CMD "echo start!"