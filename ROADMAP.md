# AI 인프라 학습 로드맵

> **목표**: 백엔드 개발자 → **AI 인프라 엔지니어**. GPU 서버 위에서 모델이 학습·서빙되는 전체 스택을 기초부터 이해하고 직접 다룬다.
> **원칙**: **학습 우선** — 회사 서버 도입 일정과 무관하게 기초부터 순서대로 쌓는다. 특정 하드웨어(블랙웰)에 종속된 내용은 부록으로 분리.
> **페이스**: 주 10시간+, **19주 계획 + 조건부 2주 + 버퍼 3주 = 최대 24주**
> 서버 용도(학습 vs 추론)는 미정 → 양쪽을 얇게 병렬로 커버, 확정 시 재조정.

이 문서는 학습 순서의 **정본**이다. 일일 진도·회고는 [`docs/log.md`](docs/log.md), 운영 규칙은 [`README.md`](README.md) 참고.
*(v3, 2026-07-02: 학습 우선으로 재정렬 — 납품 대비 요소를 부록으로 이동, 본문은 범용 AI 인프라 기초 중심)*

---

## 전체 구조 (7블록)

| 블록 | 주제 | 핵심 질문 | 기간 | 산출물 위치 |
|---|---|---|---|---|
| **Block 0** | 기초 최소화 | 코드를 읽고 돌릴 수 있는가 | 2주 (진행 중) | `python/` |
| **Block 1** | 컨테이너 & GPU 노출 | GPU를 컨테이너에 어떻게 태우는가 | 2주 | `docker/`, `docs/notes/` |
| **Block 2** ★ | GPU / CUDA | 드라이버·CUDA·GPU 메모리는 어떻게 맞물리는가 | 3주 | `docs/notes/block2-gpu-cuda.md` |
| **Block 3** | 서버·OS·네트워크 | GPU 서버는 어떻게 구성되는가 | 3주 | `docs/notes/block3-server-network.md` |
| **Block 4** | 쿠버네티스 + GPU | 여러 작업이 GPU를 어떻게 나눠 쓰는가 | 2주 (+조건부 2주) | `kubernetes/` |
| **Block 5** | 서빙 & 학습 (병렬) | 모델은 어떻게 서빙되고 학습되는가 | 4주 | `serving/`, `training/`, `mlflow/` |
| **Block 6** | 관측성 & 운영 | 안정적으로 굴리려면 무엇을 봐야 하는가 | 3주 | `monitoring/`, `docs/` |

> **핵심 원칙 — "직접 손으로 돌려본다"**
> CPU 노트북에서 되는 것(컨테이너, K8s `kind`, 파이썬)은 로컬에서, GPU가 필요한 것은 클라우드 GPU에서.
> 매주 **실행되는 산출물 1개** — 읽기만 하는 주를 만들지 않는다.

---

## GPU 실습 환경 (Block 1 중 결정 — 학습의 전제)

Block 2부터는 GPU가 필요하다. 학습용으로는 저렴한 단일 GPU면 충분하다.

| 용도 | 필요한 것 | 예시 | 예상 비용 |
|---|---|---|---|
| Block 2~3, 5~6 (대부분의 실습) | **root 있는 단일 GPU VM**, Turing 이상 | Lambda/AWS 등 단일 GPU 인스턴스 ($1~4/hr) | 총 15~25h ≈ **$50~100** |
| Block 3 W3 (선택 — NVLink 실측) | 멀티 GPU(NVLink) VM | 8x SXM 인스턴스 세션 2~3h | ~$100 (선택) |

⚠️ 주의:
- **RunPod/Vast 등 컨테이너 대여로는 Block 2 드라이버 실습 불가** — 드라이버가 이미 깔린 컨테이너만 주므로 root VM 필요.
- **V100/Pascal 인스턴스 금지** — CUDA 13.x가 Volta 이하 타깃을 제거해 현행 스택이 안 돌아감. Turing 이상(권장 Ampere+).
- **EKS는 Block 4에서만** — Block 2~3은 일반 GPU VM에서.

---

## Block 0 — 기초 최소화 (진행 중, 2주 · **종료일 고정: W2 말 강제 진행**)

**목표**: 인프라 엔지니어가 "코드를 읽고 돌릴" 최소 역량. 개별 문법 드릴 대신 **통합 산출물 1개**를 증분으로 완성한다.

**단일 산출물**: `python/train_mnist.py` — CLI 학습 스크립트 하나에 Block 0의 모든 파이썬 주제를 녹인다.

- **W1**: 스크립트 뼈대 — `argparse`(하이퍼파라미터 입력) + `logging` + 타입힌트로 구조 잡기, 데이터 로드까지 (커밋)
- **W2**: 학습 루프(`nn.Module`, `.to(device)`, `torch.cuda.is_available()` 의미 체감) + 예외처리 + 모델 save/load 완성
- Linux 기본(`top`, systemd, 권한, `nvidia-smi` 읽는 법)은 **Ubuntu 컨테이너에서**(`docker run -it ubuntu`) — macOS엔 systemd/nvidia-smi가 없다. Docker 설치가 부담이면 Block 1로 이월.

**✅ 완료 기준**: `python train_mnist.py --epochs 1`이 CPU에서 돌고, 모델 파일 저장/재로드가 되고, 커밋돼 있다.
**⚠️ 주의**: W2 말이 되면 완성도와 무관하게 Block 1로 강제 진행 (study-coach가 이 규칙으로 채점).

---

## Block 1 — 컨테이너 & GPU 노출 (2주)

**목표**: AI 인프라의 배포 단위는 컨테이너. GPU를 컨테이너에 태우는 원리를 이해하고, 이후 학습에 쓸 GPU 환경을 확정한다.

- **W1**: Docker 기본(이미지/레이어/볼륨/네트워크) → `Dockerfile` 작성 — CUDA 베이스(`nvidia/cuda:*` 또는 NGC PyTorch) + 멀티스테이지, Block 0 스크립트 탑재, **CPU 경로로 로컬 빌드·실행 검증**, `.dockerignore`
  - **시크릿 규칙 확립**(W1 D1의 PAT 노출 재발 방지): NGC API key·HF 토큰은 환경변수/키링으로만, 커밋·Dockerfile 하드코딩 금지
- **W2**: NVIDIA Container Toolkit 원리(`--gpus all`이 컨테이너에 드라이버를 주입하는 구조 — 실행 검증은 Block 2 Day 1로), NGC 카탈로그 구조, 레지스트리 개념
  - `docs/notes/gpu-access-decision.md` — 실습용 GPU 프로바이더·인스턴스 타입·시간당 비용 결정·기록

**✅ 완료 기준 (게이트)**: (a) CPU에서 빌드·실행되는 Dockerfile 커밋 + (b) `gpu-access-decision.md` 커밋. **(b) 없이는 Block 2 진입 금지** — 이론만 읽는 블록을 만들지 않기 위한 장치다.
**⚠️ 베스트 프랙티스**: 데이터·웨이트는 이미지에 굽지 말고 볼륨으로.

---

## Block 2 — GPU / CUDA (3주) ★

**목표**: 드라이버·CUDA·GPU 메모리 구조를 **직접 겪어서** 안다. AI 인프라 장애의 1순위인 "버전 호환성"을 몸으로 배우는 블록.
**산출물 파일**: `docs/notes/block2-gpu-cuda.md` (명령 출력을 붙여넣어 커밋 — study-coach가 이것으로 채점)

- **W1 — 스택 확인 랩**: 클라우드 root GPU VM에서 `nvidia-smi`로 드라이버/CUDA 런타임 확인. GPU vs CPU 연산 모델, SM/CUDA 코어/텐서 코어 개념. **드라이버 ↔ CUDA Toolkit ↔ cuDNN ↔ 프레임워크(PyTorch)가 어떻게 맞물리는지** 호환성 매트릭스를 직접 정리 (2026-07 기준: 드라이버 R580 LTSB · CUDA 13.x · PyTorch 2.12+cu130 · cuDNN 9.2x — 실행 시점에 릴리스 노트로 재확인)
- **W2 — 함정 재현 랩**: 구버전 torch 휠을 일부러 설치해 `CUDA error: no kernel image is available` **재현** → 현행 휠(cu130)로 해결. 전 과정 트랜스크립트를 노트에 커밋. `torch.cuda.is_available()`=True여도 연산이 죽을 수 있는 이유(휠에 해당 아키텍처 커널 부재)를 체감
- **W3 — OOM 랩**: 텐서를 키워가며 CUDA OOM 유발, `nvidia-smi dmon`으로 관찰. VRAM ↔ 모델 크기 관계, OOM 원인과 대응(배치 축소, 정밀도, gradient checkpointing 개념) 정리

**✅ 완료 기준**: 노트에 3개 랩의 실제 출력 + 직접 정리한 호환성 매트릭스.
**⚠️ 주의**: GPU 생태계는 빠르게 움직인다 — 블로그보다 **공식 릴리스 노트가 1차 소스**. (회사 서버가 블랙웰이면 부록 A의 특화 사항을 곁들여 읽기)

---

## Block 3 — 서버·OS·네트워크 (3주)

**목표**: GPU 서버가 물리적·시스템적으로 어떻게 구성되는지 이해한다. 범용 지식 우선 — 특정 하드웨어 브링업은 부록 B로 분리.
**산출물 파일**: `docs/notes/block3-server-network.md`

- **W1 — Linux 서버 실무**: systemd 서비스 관리(start/enable/status/journalctl), 커널 모듈 개념과 드라이버 설치 일반론(패키지 vs DKMS, Secure Boot이 모듈 로딩에 미치는 영향), SSH·권한·패키지 관리. GPU VM에서 실제 드라이버 상태를 systemd/journalctl로 관찰
- **W2 — GPU 서버 아키텍처 개념**: 왜 PCIe만으로는 부족한가 → NVLink/NVSwitch(GPU 간), NUMA와 CPU-GPU 배치, `nvidia-smi topo -m` 읽는 법. 노드 간 네트워크: 이더넷 vs InfiniBand/RoCE, RDMA·GPUDirect 개념. 스토리지 계층: 학습 데이터/체크포인트/웨이트를 어디에 두나(NFS, 병렬 FS, 로컬 NVMe 캐시)
- **W3 — 토폴로지 읽기 실습**: 멀티 GPU VM에서 `topo -m`·`nvlink -s` 실측 + nccl-tests `all_reduce_perf`로 GPU 간 대역폭 측정 (예산 여유 시). *대안: NVIDIA 공개 topo 출력을 줄 단위로 주석 달아 해석 — 실측은 나중에 기회가 오면*

**✅ 완료 기준**: 노트(systemd/드라이버 관찰 기록 + 토폴로지 해석 + 네트워크·스토리지 개념 정리).
**참고**: 전력/냉각/펌웨어/벤더 계약 같은 "서버 반입" 주제는 학습 범위가 아니라 **부록 B**(서버 도입이 실제로 진행될 때 참고)로 분리했다.

---

## Block 4 — 쿠버네티스 + GPU (코어 2주 + 조건부 2주)

**목표**: GPU 오케스트레이션. **단, 단일 노드 서버는 Docker+systemd+DCGM만으로 운영 시작 가능** — K8s는 GPU 운영의 전제조건이 아니라 규모가 커질 때의 도구임을 이해한다.

**코어 (2주)**:
- **W1**: `kind`로 K8s 개념(Pod/Deployment/Service/namespace) + Helm 기본 — CPU 로컬, 매니페스트 커밋
- **W2**: 클라우드 GPU 노드에 **NVIDIA GPU Operator** 배포(드라이버·toolkit·device plugin·DCGM 자동화) → GPU Pod 1개 스케줄링 (`resources.limits."nvidia.com/gpu"`), `kubectl describe` 출력 커밋

**조건부 (+2주, 필요해지면)**:
- **MIG**(GPU 분할): 여러 팀이 GPU를 나눠 쓰는 수요가 생기면
- 배치 스케줄러(Kueue/Volcano/Slurm) 비교는 **1페이지 결정 노트**로 한정 — 용도가 '학습'으로 확정되면 Slurm 실습 추가

**✅ 완료 기준**: kind 매니페스트 + GPU Operator 배포 기록 + GPU Pod 스케줄링 증적.

---

## Block 5 — 서빙 & 학습 (병렬, 4주) — **산출물 4개로 명시 한정**

**목표**: 용도 미정이므로 두 트랙을 얇게. 아래 4개 산출물이 전부다 — 그 이상 파면 다른 블록이 밀린다.

| # | 산출물 | 위치 | 배분 |
|---|---|---|---|
| 1 | **vLLM**으로 오픈소스 LLM 1개 서빙(OpenAI 호환 API) + **처리량/지연 벤치마크 1회** | `serving/` | 1.5주 |
| 2 | **TensorRT-LLM/NIM은 NGC 프리빌트 컨테이너 실행만** (엔진 빌드 금지) | `serving/` | 0.5주 |
| 3 | **DDP 토이 학습**(2 GPU) + 체크포인트 저장/재개 (FSDP/DeepSpeed는 읽기 노트로만) | `training/` | 1.5주 |
| 4 | **MLflow에 학습 1런 기록** (파라미터·메트릭·아티팩트) | `mlflow/` | 0.5주 |

- 개념 학습: PagedAttention·continuous batching, 양자화(FP8/INT8 등)와 처리량-지연 트레이드오프, NCCL·AMP, 왜 멀티 GPU인가(DDP vs 모델 샤딩)
- **서빙 보안 (필수)**: vLLM OpenAI 서버는 **기본 무인증** — 노출 전 API key/게이트웨이(`gateway/` 활용) 최소 1겹. 모델 웨이트는 **safetensors만**(pickle `.bin`은 로드 시 임의 코드 실행 위험), 오픈 모델의 **상용 라이선스** 확인 습관.

**✅ 완료 기준**: 위 4개 산출물 커밋 + 서빙 인증 1겹.

---

## Block 6 — 관측성 & 운영 (3주)

**목표**: "돌아가게"에서 "안정적으로"로. GPU 인프라 운영의 표준 도구 체인을 손에 익힌다.

- **W1 — 메트릭 파이프라인**: **DCGM / DCGM Exporter**(GPU 사용률·온도·전력·ECC·XID 메트릭) → Prometheus → **Grafana GPU 대시보드**(NVIDIA 레퍼런스 대시보드 활용)
- **W2 — 알림과 장애 대응**: 알림 규칙(OOM·XID·온도 임계) + 장애 플레이북 작성 — 드라이버 크래시, "GPU fallen off the bus"(XID 79), ECC 에러의 의미와 대응. 패치 위생: Security Bulletin 구독, 변경 전 스냅샷·롤백 개념, 드라이버 브랜치 EOL 추적
- **W3 — 지속 가능한 운영**: 백업 개념(체크포인트·웨이트 — `models/`는 git 미추적이라 백업 별도 필요), GPU 유휴율 추적과 효율, (선택) Terraform/Ansible로 구성 코드화
  - **🎓 캡스톤 — ops 노트 종합**: Block 2~6에서 쌓은 노트를 "GPU 인프라 운영 핸드북" 하나로 종합 — 버전 호환성 매트릭스, 장애 플레이북, 검증 명령 모음. 학습의 총정리이자 실무 투입 시 바로 쓸 자산

**✅ 완료 기준**: Grafana 대시보드 1개 + 장애 플레이북 + 캡스톤 핸드북.

---

## 학습 운영 방식 (study-coach 체계)

- **일일 포맷**: `docs/log.md` 4줄 유지 — `오늘 한 것 / 발생한 문제 / 해결·확인 / 다음에 할 것`. 블록 전환 시 `[Block N 시작]` 표기
- **채점 가능 규칙**: 모든 마일스톤은 **커밋 가능한 산출물 + 경로**로 정의돼 있다(위 각 블록). 노트류는 `docs/notes/`에 — vault에 쓰면 study-coach가 못 본다. 명령 실습은 **출력 붙여넣기**까지가 산출물
- **버퍼 규칙**: 19주 계획 + 3주 버퍼. 블록 종료마다 잔여 버퍼를 로그에 기록 — 지연을 보이게 만든다
- **자리 뜨기 전 `git push`** / Mac 이동 시 양쪽 repo `git pull` (기존 규칙 유지)

## 시간 압축 시 컷 우선순위

일정이 밀리면 **이 순서로 잘라낸다** (피해 최소 순):

1. Terraform (이미 선택) → 2. MLflow → 3. TensorRT-LLM (vLLM만으로 서빙 학습 충분) → 4. FSDP/DeepSpeed 읽기 노트 → 5. Block 1 이미지 최적화 → 6. Block 4 조건부 전체 → 7. Block 3 W3 실측(주석 대안으로 대체)

**절대 컷 불가**: Block 2 전체(호환성·함정·OOM 랩) · DCGM 기본 · Docker+Container Toolkit · vLLM 서빙 1회.

## 리스크 & 주의사항

- **GPU 실습 조달이 최대 병목**: Block 1 게이트(gpu-access-decision.md) 미통과 시 Block 2 진입 금지 — 이론만 읽는 블록을 만들지 않는다
- **용도 확정 시 재조정**: '학습' → Block 4에 Slurm 추가, 5B 심화 / '추론' → 5A 심화, TRT-LLM 승격
- **회사 서버 구체화 시**: 기종이 확정되면 부록 A(블랙웰 특화)를 해당 블록에 곁들여 읽고, 도입이 실제 진행되면 부록 B 참고. **그 전까지는 신경 쓰지 않는다**
- **과욕 금지**: 각 블록은 "핵심 원리 + 손으로 1회". 완벽주의로 갇히지 말 것

---

## 부록 A — 블랙웰 특화 레퍼런스 (선택 — 회사 서버가 블랙웰 계열일 때 곁들여 읽기)

> 본문 커리큘럼은 하드웨어 세대와 무관하게 유효하다. 아래는 블랙웰(B200/B300/GB200급)에서 달라지는 점만 모은 참고 자료. 버전은 2026-07 기준 검증 — 실행 시점 재확인.

### A-1. 소프트웨어 기준선

| 구성요소 | 2026-07 현행 | 비고 |
|---|---|---|
| Compute Capability | B200/GB200 = **sm_100** · B300/GB300 = **sm_103** · RTX 50 = sm_120 | family arch `compute_100f` 빌드 시 sm_100+sm_103 동시 커버 |
| CUDA Toolkit | **13.x 계열** (하한 12.8) | 13.x는 드라이버 ≥R580 요구, Volta 이하 타깃 제거 |
| NVIDIA Driver | **R580 LTSB 권장** (지원 2028-08까지) | R570은 2026-02 EOL — 구자료의 "R570 설치" 주의 |
| PyTorch | **2.12.x + cu130 휠** (PyPI 기본) | cu128 휠은 삭제됨 — 구자료의 "cu128" 처방 무효 |
| cuDNN | **9.2x** (CUDA 13.x와 짝) | 마이너 버전 짝 맞추기가 실무 포인트 |

**전형적 함정**: `torch.cuda.is_available()`=True인데 연산 시 `no kernel image available` → 휠에 해당 sm 커널 부재. 해결: cu130 휠. (Block 2 W2 랩과 동일 패턴)

### A-2. GB200/GB300 = ARM 아키텍처
- Grace CPU = ARM(aarch64) — x86 이미지 실행 불가, 컨테이너는 멀티아키(`amd64`+`arm64`) 빌드 필요
- PyTorch 2.11+부터 PyPI가 aarch64 CUDA 휠 기본 제공 — 휠 수급 부담은 해소됨

### A-3. NVSwitch 시스템: Fabric Manager (+ NVL72는 IMEX)
- NVSwitch 기반 시스템은 `nvidia-fabricmanager` 서비스 필수 — 미기동 시 NVLink 미형성. **드라이버·FM 버전 정확 일치** + NVLink 스택 lockstep 업데이트
- NVL72 한정: 멀티노드 NVLink에 `nvidia-imex` 서비스 필수. K8s에선 DRA ComputeDomains가 관리
- 확인: `nvidia-smi nvlink -s` · `systemctl status nvidia-fabricmanager`

### A-4. 전력·냉각·서빙 경제학
- B200 TDP 공랭 1000W/수랭 1200W, NVL72 = 랙당 ~120kW 수랭 전제 — 시설은 시설팀/벤더 영역
- 5세대 텐서 코어 **FP4/FP8**이 추론 처리량 핵심 (TensorRT-LLM이 FP4 최적 경로, HBM3e 대용량: B200 180GB/B300 288GB)
- NVAIE 라이선스: NIM 등 프로덕션 사용엔 필요(~$4,500/GPU/년), 블랙웰 미번들 — NGC 공개 컨테이너는 무료

### A-5. 검증 명령 치트시트

```bash
# 상태 확인
nvidia-smi                      # 드라이버/CUDA/GPU 인식 (Block 2)
nvidia-smi topo -m              # GPU 토폴로지 (Block 3)
nvidia-smi nvlink -s            # NVLink 상태 (Block 3)
systemctl status nvidia-fabricmanager   # NVSwitch 패브릭
dcgmi discovery -l              # DCGM GPU 인식 (Block 6)
kubectl get nodes -o json | grep nvidia.com/gpu   # k8s GPU 리소스 (Block 4)

# 합격/불합격 판정 (부록 B 인수검사)
dcgmi diag -r 3                 # 하드웨어 진단 (-r 4 = 장시간)
./all_reduce_perf -b 8 -e 4G -f 2 -g 8   # nccl-tests: GPU 간 대역폭 실측
gpu-burn 3600                   # 열 안정성 burn-in
fio --name=read --rw=read ...   # 스토리지 대역폭
```

---

## 부록 B — 서버 브링업·인수검사 체크리스트 (참고용 — 서버 도입이 실제 진행될 때)

> **지금은 신경 쓰지 않는다.** 회사 서버 도입이 실제로 진행되면 그때 꺼내 쓰는 참고 자료다. Block 2~3, 6을 마쳤다면 아래를 이해하고 실행할 수 있는 상태가 된다.

### 도입 전 확인 (이메일 수준)
- [ ] 기종(x86 vs ARM — 이미지 빌드 전략이 갈림) / 벤더·납품 OS / 지원계약(SLA·RMA 창구) / NVAIE·BCM 번들 여부 / 서버실 망 정책(폐쇄망이면 NGC 미러 필요) / 랙 전력·냉각(시설팀 영역)

### 브링업 (순서대로)
- [ ] ① BMC 접속 → 기본 자격증명 변경 → 펌웨어 인벤토리 기록 ② OS 설치 ③ 드라이버(open kernel module) + 동일 버전 fabricmanager ④ `nvidia-smi`→`topo -m`→`nvlink -s` 검증 ⑤ persistence mode ⑥ DCGM → `dcgmi diag -r 3` 통과 ⑦ burn-in(24h+, 초기 불량은 지금 잡는 게 가장 쉽다) ⑧ nccl-tests 대역폭 **베이스라인 기록** ⑨ fio 스토리지 실측 ⑩ known-good 버전 스냅샷을 repo에 커밋 ⑪ 최소 모니터링(DCGM+기본 알림) 가동

### 자주 만나는 장애 2개
- **FM 기동 실패** → 드라이버-FM 버전 불일치 (A-3) · **`no kernel image`** → 휠의 sm 커널 부재 (A-1)

---

## 참고: 1차 소스 (블로그보다 우선)
- NVIDIA CUDA Toolkit / Data Center Driver 릴리스 노트
- NVIDIA GPU Operator · Container Toolkit · MIG · DCGM · Fabric Manager 공식 문서
- NGC 카탈로그 · vLLM 공식 문서 · PyTorch Get Started (CUDA 빌드 선택)
- nccl-tests GitHub
