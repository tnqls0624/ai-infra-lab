# Block 3 노트 — 서버·OS·네트워크 (채점용: 명령 출력을 붙여넣어 커밋)

> ROADMAP.md § Block 3. GPU 서버가 물리적·시스템적으로 어떻게 구성되는지 — 범용 지식 우선.

## W1 — Linux 서버 실무
### systemd로 드라이버/서비스 관찰 (GPU VM에서)
```
(systemctl status / journalctl 출력 붙여넣기)
```
### 드라이버 설치 일반론 정리 (패키지 vs DKMS, Secure Boot의 영향):
### SSH·권한·패키지 관리에서 새로 안 것:

## W2 — GPU 서버 아키텍처 개념
### 왜 PCIe만으로는 부족한가 (NVLink/NVSwitch가 푸는 문제):
### NUMA와 CPU-GPU 배치:
### 노드 간 네트워크 (이더넷 vs IB/RoCE, RDMA·GPUDirect):
### 스토리지 계층 (데이터/체크포인트/웨이트를 어디에 두나):

## W3 — 토폴로지 읽기
### nvidia-smi topo -m 출력 + 줄 단위 해석
```
(실측 또는 공개 출력 붙여넣기)
```
### (실측 시) nccl-tests all_reduce_perf 대역폭
```
(붙여넣기)
```
### 해석 — 이 서버에서 GPU들은 어떻게 연결되어 있고, 무엇이 병목인가:
