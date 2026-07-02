# Block 2 노트 — GPU/CUDA & 블랙웰 (채점용: 명령 출력을 붙여넣어 커밋)

> ROADMAP.md § Block 2. 주차별 랩의 실제 출력이 이 파일에 있어야 study-coach가 채점할 수 있다.

## W1 — 스택 확인 랩
### nvidia-smi 출력 (클라우드 root GPU VM)
```
(붙여넣기)
```
### A-1 표 재검증 결과 (릴리스 노트 대조 — 바뀐 것 있으면 ROADMAP 부록 A-1도 갱신)
| 구성요소 | ROADMAP 기준선 | 실제 확인값 | 출처 |
|---|---|---|---|
| CUDA Toolkit | 13.x | | |
| Driver | R580 LTSB | | |
| PyTorch | 2.12.x + cu130 | | |
| cuDNN | 9.2x | | |

## W2 — 함정 재현 랩 (`no kernel image`)
### 재현 (구버전 휠 설치 → 에러)
```
(트랜스크립트 붙여넣기)
```
### 해결 (cu130 휠 설치 → 정상)
```
(트랜스크립트 붙여넣기)
```
### 배운 것 (호환성 매트릭스가 장애 1순위인 이유):

## W3 — OOM 랩
### OOM 유발 + nvidia-smi dmon 관찰
```
(출력 붙여넣기)
```
### VRAM ↔ 모델 크기 관계 정리:
### 블랙웰 특이사항 노트 (FP4/FP8, HBM3e, CDMM):
