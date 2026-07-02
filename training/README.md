# training/ — Block 5B: 학습 트랙 (+ Block 0 실습)

> 로드맵: [`ROADMAP.md` § Block 5](../ROADMAP.md)

## 산출물 (한정)
- Block 0: `../python/train_mnist.py` (단일 GPU 이전의 CPU 학습 감잡기 — Block 0 참고)
- Block 5B: **DDP 토이 학습(2 GPU) + 체크포인트 저장/재개** (1.5주)
- **FSDP/DeepSpeed는 읽기 노트로만** — 실습 금지 (시간 압축 시 컷 4순위)

## 핵심 개념
- 왜 멀티 GPU인가 (모델/데이터가 한 GPU에 안 들어갈 때), DDP vs FSDP
- **NCCL** — 학습 통신이자 브링업 검증 도구(nccl-tests, 부록 B) 이중 가치
- mixed precision(AMP), 실험 추적은 `../mlflow/` 연동

## 완료 기준
DDP 토이 1회 성공 + 체크포인트 저장 → 재개 증적.
