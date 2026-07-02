# docker/ — Block 1: 컨테이너 & GPU 노출

> 로드맵: [`ROADMAP.md` § Block 1](../ROADMAP.md#block-1--컨테이너--gpu-노출-2주)

## 여기에 채울 것
- `Dockerfile` — Block 0 학습 스크립트를 담은 GPU 컨테이너 (멀티스테이지)
- `.dockerignore` — 데이터/모델/`.venv` 제외
- CUDA 베이스 이미지(`nvidia/cuda:*` 또는 NGC PyTorch) 기반

## 핵심 학습 포인트
- NVIDIA Container Toolkit: `--gpus all`이 컨테이너에 드라이버를 주입하는 원리 (GPU 실행 검증은 Block 2 Day 1)
- 이미지에 데이터·웨이트를 굽지 말고 **볼륨/마운트로 분리**
- 회사 서버가 GB200/GB300(arm64)이면 **멀티아키 빌드** 필요 (ROADMAP 부록 A-2)
- **시크릿 규칙**: NGC API key·HF 토큰은 환경변수/키링으로만 — Dockerfile·커밋에 절대 금지 (W1 D1 PAT 노출 재발 방지)

## 완료 기준 (Block 1 게이트)
(a) CPU에서 빌드·실행되는 Dockerfile 커밋 + (b) `../docs/notes/gpu-access-decision.md` 커밋.
**(b) 없이 Block 2 진입 금지** — 이론만 읽는 블록을 만들지 않기 위한 장치.
