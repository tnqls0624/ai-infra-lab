# AI Infra 학습 로그 (ai-infra-lab)

## 2026-06-29 (월) — W1 D1

- **오늘 한 것**: ai-infra-lab repo 생성, 디렉토리 골격(training/serving/gateway/docker/kubernetes/mlflow/workflows/monitoring/terraform/docs/notebooks/models) 커밋, GitHub(private) push
- **발생한 문제**: git remote URL에 PAT가 평문으로 박혀 노출됨
- **해결하거나 확인한 내용**: `git remote set-url`로 토큰 제거, gh keyring 인증으로 전환. (노출된 토큰은 GitHub에서 폐기·재발급 예정.) models/는 .gitignore 처리, origin 연결 확인
- **다음에 할 것**: W1 D2 — venv + PyTorch(CPU) 설치, requirements.txt 커밋

## 2026-06-30 (화) — W1 D2 · D3

- **오늘 한 것**: `python -m venv .venv` 가상환경 생성, PyTorch CPU 빌드 설치(torch 2.12.1 + torchvision 0.27.1) 및 numpy·scikit-learn·jupyter 설치, `pip freeze > requirements.txt`(113줄) 버전 고정 커밋
- **발생한 문제**: 특이사항 없음(설치 정상). `.venv/`가 git에 올라갈 뻔함
- **해결하거나 확인한 내용**: `import torch` 무오류, `torch.cuda.is_available()` = **False** (GPU 없는 CPU 환경이라 정상 — 블록2에서 EKS GPU 노드 붙이면 True로 바뀔 예정). `.gitignore`에 `.venv/`·`__pycache__/`·`*.pyc` 추가해 가상환경·캐시가 추적되지 않도록 처리(요구사항은 `requirements.txt`만으로 재현)
- **다음에 할 것**: W1 D4 — 점프투파이썬에서 comprehension·f-string·타입힌트 복습 + 예제 1개

## 2026-06-30 (화) — W1 D4

- **오늘 한 것**: for문을 사용하여 배열안의 int형 숫자를 f-string을 사용하여 print 출력
- **발생한 문제**: 특이사항 없음
- **해결하거나 확인한 내용**: 잘출력됨
- **다음에 할 것**: `ROADMAP.md` 확정(학습 우선) → **Block 0 계속**: `python/train_mnist.py` 뼈대 시작 — argparse/logging/타입힌트로 CLI 구조 잡고 데이터 로드까지 (W2 말 강제 종료 규칙 있음)

## 2026-07-05 (일) — W1 D5

- 오늘 한 것: S2~S5 구현 완료, --epochs 1 실행 검증, batch 64 vs 256 시간/loss 비교 실험
  y=ax+b 1차 방정식 및 그래프 공부, 텐서에서는 y = w(가중치)x(데이터) + b(바이어스(기본값))
- 발생한 문제: load_data가 Dataset을 반환하던 버그 (DataLoader로 안 감싸고 해당 객체 return 안함), tuple() 사용법 혼동
- 해결하거나 확인한 내용: loader 2개 반환으로 수정. batch 크기가 시간엔 영향 미미(총 연산 동일), loss엔 영향 큼(업데이트 938 vs 235회)
- 다음에 할 것: Block 0 W2 — Linux 기본기(`docker run -it ubuntu`에서 top/권한/systemd 감각) + 수학 병행(정승제 50일 수학 선별: 함수/이차함수/지수로그). Block 0 완료 기준은 달성 상태

## 2026-07-06 (월) — W2 D3

- 오늘 한 것: lscpu로 core개수 체크, top 로 loadaverige 체크(코어개수가 11이니까 1분, 5분, 15분의 최대 수치가 11까지 증가할수 있음), free -m 으로 사용가능한 메모리 수치 확인, df -h 로 디스크 용량 확인, apt update && apt install 커맨드 사용하여 패키지 다운로드, whoami; id, journalctl 사용해보려 했으나 실패, vmstat 1,
- root@1e001715902c:/# touch /tmp/a; chmod 400 /tmp/a; ls -l /tmp/a
  -r-------- 1 root root 0 Jul 6 14:23 /tmp/a
  root@1e001715902c:/# chmod 600 /tmp/a
  root@1e001715902c:/# ls -l /tmp/a
  -rw------- 1 root root 0 Jul 6 14:23 /tmp/a
  컨테이너는 기본 root + 최소 이미지라 top/htop조차 없다 → apt로 직접 설치
  journalctl 실패 이유: 컨테이너엔 systemd(init)가 없고 PID 1이 내 셸 → 컨테이너 ≠ 완전한 서버
  chmod 400 = -r-------- (소유자 읽기만), 600 = -rw------- (읽기+쓰기)
- 발생한 문제: 없음
- 해결하거나 확인한 내용: 없음
- 다음에 할 것: Block 0 회고(버퍼 잔여 기록) + Block 1 시작 — Docker 이미지/컨테이너/레이어/볼륨 개념 정리

## 2026-07-09 (목) — W2 D4 [Block 1 시작]

오늘 한 것: 이미지, 컨테이너, 레이어 캐시, 데이터를 볼륨으로 분리하는 이유에 대해서 아는것을 적어봄.

- 이미지란?
  - 애플리케이션을 실행하기위한 종속성 라이브러리 등을 포함한 독립적인 실행 환경을 갖는 하나의 스냅샷이라고 생각함
  - 이미지 자체만으로는 실행할 수 없고, 컨테이너를 통해서 이미지를 실행할 수 있다. 컨테이너는 이미지를 실행할때 베이스 이미지는 변경 불가 상태로 만들고, 똑같은 변경 가능한 이미지를 복사하여 실행한다.
  - 이미지는 여러 레이어가 겹겹이 쌓인 구조로 이루어져 있으며, 변경된 부분은 기존 이미지 레이어에 쌓이는 구조로 만들어진다. (캐싱되어 재활용 될 수 있다)
- 컨테이너란?
  - 보통 컨테이너에 대해서 이야기할때 VM과 비교를 많이 하고는 한다. VM은 하이퍼 바이저 위에서 여러 게스트 OS를 배치하여 하드웨어 수준의 가상화를 통하여 격리한다. VM이 하드웨어 수준의 가상화인것에 비해 컨테이너는 OS 수준의 가상화를 진행한다. 리눅스 커널을 사용하여, cgroups기능으로 자원 리소스(cpu, memory, disk)를 격리하며 namespace를 사용하여 프로세스를 격리하여 제한할 수 있다. 그렇기에 VM보다 가볍고 관리가 편한 장점이 있다.
- 볼륨이란?
  - 컨테이너가 삭제되었을때 데이터가 사라지게 됨으로, 호스트 머신의 디렉토리에 마운트하여 데이터의 영속성을 보장시키기 위해 사용
  - 컨테이너를 다시 종료하고 실행했을때도 데이터를 그대로 사용가능
- 발생한 문제: 회사에서 교보생명 채팅상담 솔루션 구축 업무를 진행할때, 온프레미스 환경에서 배포를 하다보니 보안적으로 배포 패키지를 반입하기가 까다로웠고, 이미지 용량이 커서 새로 빌드하고 배포하는 시간이 너무 오래걸렸고, 반입하는 절차가 너무 까다로웠음. 100MB 이상의 파일은 CD롬을 통해서 직접 서버실로 들어가서 마운트해야하는 문제. 30MB이하일경우 메일로도 전송 가능한 상태.
  해결하거나 확인한 내용: base 이미지를 온프레미스 환경의 서버에 registry에 저장 및 로드시켜놓고, 이미지의 레이어 기능을 활용해서 기존 이전 버전의 베이스이미지에서 diff한 레이어만 이미지로 만들어서 메일로 전송. 현장에 저장되어있는 기존 버전의 이미지와 메일로 전송한 새로 배포할 이미지를 합처서 완전한 이미지로 만들어서 배포하는 방식으로 변경.
  배포 시간 및 반입 절차 문제를 해결함.
  다음에 할 것: 오늘 정리한 개념을 손으로 검증 — `docker volume create` + `-v` 마운트로 컨테이너 삭제 후 데이터 생존 확인, `docker history`로 레이어 캐시 실측. 이어서 Block 1 W1 본작업 — Docker 네트워크(브리지/포트 매핑) 개념 + `python/train_mnist.py` 탑재 Dockerfile 작성 시작(멀티스테이지, CPU 로컬 빌드·실행 검증, `.dockerignore`). 시크릿(PAT·토큰)은 Dockerfile/커밋에 하드코딩 금지.

## 2026-07-11 (토) — W2 D5

- 오늘 한 것: CUDA 베이스(`nvidia/cuda:12.4.1-runtime-ubuntu22.04`) Dockerfile 작성 → `docker build`/`docker run` 통과, 컨테이너 안에서 CPU 학습 1 epoch 완주(loss=0.0898, 모델 저장/재로드 검증까지). `.dockerignore` 추가. 소스 1줄 변경 후 재빌드로 레이어 캐시 무효화 실측.
- 발생한 문제: 빌드 에러 4종을 순서대로 겪음
  - `RUN apt install && pip install` 실패 — `apt update` 선행 없음 + 설치할 패키지명 없음 + pip은 아직 설치 전이라 command not found
  - `COPY requirements.txt .` 실패 — COPY는 빌드 컨텍스트 밖의 파일을 절대 못 봄 (컨텍스트가 `docker/`여서 루트의 requirements.txt 접근 불가)
  - `pip install -r requirements.txt --index-url .../whl/cpu` 실패 — pytorch CPU 인덱스에는 torch 계열만 있어서 scikit-learn/jupyterlab을 못 찾음
- 해결하거나 확인한 내용:
  - 빌드 컨텍스트를 리포 루트로 바꾸고 `-f docker/Dockerfile`로 Dockerfile 위치를 분리 지정. `.dockerignore`(.venv 991MB, data 63MB 등 제외)로 transferring context 약 1GB → 136B
  - 컨테이너에는 torch/torchvision CPU wheel만 직접 설치 — 로컬 개발 의존성(jupyterlab 등)과 컨테이너 실행 의존성은 다르다. 이미지에는 실행에 필요한 최소만
  - CMD는 exec form(JSON 배열)으로 — sh를 거치지 않고 python이 직접 PID 1이 됨 (D3에서 확인한 "컨테이너 PID 1 = 내 프로세스"와 연결)
  - 실행 시 "NVIDIA Driver was not detected" 경고 = 이미지에는 CUDA **런타임**만 있고 **드라이버**는 호스트 것을 빌려 씀. `--gpus all` + NVIDIA Container Toolkit이 드라이버를 주입하는 구조 (Block 2 Day 1에서 검증 예정)
  - 캐시 실측(D4 정밀도 ② 검증 완료): train_mnist.py에 주석 1줄 추가 후 재빌드 → apt/pip 레이어는 CACHED, COPY 레이어만 재실행. 이미지 해시가 aa98f3→b537d6으로 변경 = 레이어는 불변이고 바뀐 레이어를 얹은 새 이미지가 생성됨. 캐시는 바뀐 명령부터 아래로 전부 무효화 → 비싸고 안 바뀌는 명령은 위에, 자주 바뀌는 소스는 아래에
  - MNIST 데이터와 models/mnist.pt가 컨테이너 안에 생성되고 `--rm` 종료와 함께 소멸 — D4에 정리한 "볼륨 분리가 필요한 이유"를 직접 확인
- 다음에 할 것: `-v` 마운트로 data/models 호스트 분리 + named volume vs bind mount 비교(정밀도 ③), `docker diff`로 CoW 확인(정밀도 ①), Block 1 게이트 (b) `docs/notes/gpu-access-decision.md` 작성

## 2026-07-12 (일) — W2 D5

오늘 한 것: 멀티스테이지로 이미지 슬림화, .dockerignore로 빌드 컨텍스트 정리, 시크릿 커밋 금지 규칙
발생한 문제:

- 멀티스테이지 첫 빌드는 통과했지만 실행하면 `import torch`가 `ModuleNotFoundError: No module named 'ctypes'`로 죽음 — venv를 COPY해도 따라오는 것은 site-packages(torch 등)뿐이고, ctypes 같은 표준 라이브러리는 시스템 파이썬 몫(`libpython3.10-stdlib`)이라 runner의 `python3-minimal`에는 없었음. runner를 full `python3`로 교체해 해결.
- Dockerfile의 torch 핀을 고친 뒤 빌드·실행까지 했는데 이미지 안은 여전히 torch 2.5.1 — 파일 저장(13:01) 전에 빌드(12:58)를 돌려 옛 내용으로 빌드된 것(시각 대조로 발견). 이후 `docker run --rm <이미지> python -c "import torch; print(torch.__version__)"`로 이미지 내부를 직접 열어 2.12.1+cpu 확인 — "빌드했다"가 아니라 아티팩트 안을 확인하는 게 검증.

(아래는 멀티스테이지 개념 정리)

컨테이너가 실행될 때는 이미 Python 패키지 설치가 끝났기 때문에 다음 도구는 필요하지 않아.

- gcc
- build-essential
- python3-dev
- pip
  그런데 단일 스테이지에서는 빌드 도구와 실행 환경이 같은 이미지에 남게 되어, 불필요한 크기를 잡아먹는 요소가 됨.
  빌드 도구는 크기가 큰 경우가 많다
- gcc
- make
- cmake
- git
- curl
- 개발 헤더
- Node.js devDependencies
- Java JDK
- Go 컴파일러

이런 도구를 빌드 스테이지에만 두면 최종 이미지에는 들어가지 않아.

또한, 최종 이미지에 도구가 적을수록 공격에 사용할 수 있는 요소도 줄어든다.
예를 들어 최종 이미지에 다음 도구가 없다고 해보자.

- gcc
- curl
- wget
- git
- make
- shell
- package manager

컨테이너에 취약점이 생겨 공격자가 접근하더라도 추가 프로그램을 다운로드하거나 컴파일하기가 더 어려워져.

포함된 패키지가 많음
→ 취약점이 발견될 가능성 증가

포함된 패키지가 적음
→ 검사 대상과 공격 표면 감소

멀티스테이지 자체가 보안을 완벽하게 보장하는 것은 아니지만, 불필요한 도구를 제거하는 데 효과적이야

또한, Dockerfile 역할이 명확해짐

각 스테이지가 목적별로 나뉘기 때문에 Dockerfile을 이해하기 쉬워져.

FROM ... AS deps
FROM ... AS builder
FROM ... AS tester
FROM ... AS runner

예를 들면 다음과 같이 구성할 수 있음

1. deps
   의존성 설치

2. builder
   소스 컴파일

3. tester
   테스트 실행

4. runner
   프로덕션 실행

위처럼 활용한다면 특정 부분만 빌드를 진행시킬수도 있다

docker build --target builder -t myapp-builder .

또는 테스트 스테이지만 빌드할 수도 있어.

docker build --target tester -t myapp-test .

해결하거나 확인한 내용:

1. 멀티스테이지를 진행하면 이점

- 이미지 크기 감소
- 불필요한 패키지 제거
- 보안 공격 표면 감소
- 빌드 환경과 실행 환경 분리
- Dockerfile 역할 명확화
- 원본 소스와 빌드 도구 제외 가능

그렇지만 멀티스테이지를 사용하는것이 꼭 이미지의 크기를 줄이는것은 아님..
최종 실행에 필요한 라이브러리가 큰 경우에는 줄일수가 없기때문에.

2. 이미지 크기 전후 실측 (docker images / docker history)

- 단일 스테이지 mnist-train:latest: 3.22GB
- 멀티스테이지 mnist-train:multistage: 2.90GB → 약 320MB 감소 (−9.9%)
- 줄어든 곳: apt 레이어 345MB → 32.3MB. runtime 스테이지에서 pip·venv와 그 의존성을 뺀 효과가 절감분의 거의 전부
- 안 줄어든 곳: torch venv 레이어 779MB → 772MB로 사실상 동일. 실행에 필요한 라이브러리는 멀티스테이지로 못 줄인다는 걸 수치로 확인
- 나머지 약 2.1GB는 nvidia/cuda:12.4.1-runtime 베이스 이미지 몫. CPU 전용이면 python:3.11-slim 베이스로 1GB 아래도 가능하지만 Block 2 GPU 전환 계획이 있어 CUDA 베이스 유지
- 동작 검증: 컨테이너 안에서 torch 2.12.1+cpu / torchvision 0.27.1+cpu import 정상 — venv COPY 방식 동작 확인

3. `-v` 마운트 + `docker diff` CoW 대조 실측 (D4 정밀도 ①③ 마감)

- `-v "$(pwd)/data:/app/data" -v "$(pwd)/models:/app/models"`로 실행 → 호스트 models/mnist.pt의 mtime이 컨테이너 로그의 저장 시각과 초 단위 일치 = 컨테이너가 마운트 통해 호스트에 직접 씀. `--rm` 뒤에도 산출물 생존 확인
- 호스트 data/ 재사용으로 재다운로드 없음 — 다운로드 포함 13초, 캐시 상태면 3.5초
- docker diff 대조 실험:
  - 마운트 없음: /app/data 밑 MNIST 파일 8개 + /app/models/mnist.pt 전부 `A` = 쓰기 레이어(CoW)에 쌓임 → docker rm과 함께 소멸
  - 마운트 있음: `A /app/data`, `A /app/models` 빈 마운트 지점 디렉터리만 남고 내용물 0줄 — 실제 쓰기는 CoW 레이어를 우회해 호스트 직행
  - /tmp/perf-1.map, /tmp/torchinductor_root는 양쪽 모두 `A` — PyTorch 런타임 흔적. diff는 프로세스가 쓴 모든 파일을 잡음
- diff 기호: A=추가, C=변경, D=삭제. 디렉터리는 자식 엔트리가 생기면 부모가 `C`로 표시됨
- 학습 도중 ^C가 컨테이너 안 python까지 전달돼 KeyboardInterrupt로 종료 — exec form CMD라 python이 PID 1로 SIGINT를 직접 받은 것 (shell form이었으면 sh가 PID 1이라 전달 안 됨)
- 로그의 loss는 에포크 평균이 아니라 마지막 배치 값이라 실행마다 다르다 (0.057 / 0.445 / 0.183)

다음에 할 것: named volume 실습 비교(`docker volume create/inspect`, bind mount와 차이 실측 — 정밀도 ③ 나머지), Block 1 게이트 (b) `docs/notes/gpu-access-decision.md` 작성


## 2026-07-16 (목) — W3 D1

> CUDA 컨테이너에서 본 다음 경고는 정확히 어느 계층이 없다는 뜻인가?
>
> ```text
> WARNING: The NVIDIA Driver was not detected.
> GPU functionality will not be available.
> Use the NVIDIA Container Toolkit to start this container with GPU support.
> ```

---

# 1. 공식 자료를 보기 전에 그린 스택 지도

## 1.1 내가 처음 이해한 구조

```text
┌───────────────────────────────────────────────────────────────┐
│ 컨테이너                                                     │
│                                                               │
│  Python / PyTorch / CUDA 애플리케이션                         │
│                 │                                             │
│                 ▼                                             │
│  CUDA 런타임 라이브러리                                       │
│  - libcudart                                                  │
│  - cuBLAS, cuDNN 등                                           │
│                 │                                             │
│  CUDA 툴킷이 포함된 이미지라면 nvcc, 헤더, 개발 도구도 존재   │
└──────────────────────────┬────────────────────────────────────┘
                           │
                   컨테이너 경계
                           │
          GPU 장치와 드라이버를 자동으로 볼 수 없음
                           │
┌──────────────────────────▼────────────────────────────────────┐
│ 호스트 사용자 공간                                            │
│                                                               │
│  Docker / containerd                                          │
│  NVIDIA Container Toolkit                                     │
│  NVIDIA 사용자 공간 드라이버 라이브러리                       │
│  - libcuda.so                                                  │
│  - libnvidia-ml.so                                             │
└──────────────────────────┬────────────────────────────────────┘
                           │ 시스템 콜 / ioctl
┌──────────────────────────▼────────────────────────────────────┐
│ 호스트 Linux 커널                                             │
│                                                               │
│  NVIDIA 커널 드라이버 모듈                                    │
│  - nvidia                                                     │
│  - nvidia_uvm                                                 │
│  - nvidia_modeset 등                                          │
│                                                               │
│  GPU 장치 파일                                                 │
│  - /dev/nvidia0                                               │
│  - /dev/nvidiactl                                             │
│  - /dev/nvidia-uvm                                            │
└──────────────────────────┬────────────────────────────────────┘
                           │ PCIe
┌──────────────────────────▼────────────────────────────────────┐
│ NVIDIA GPU 하드웨어                                            │
└───────────────────────────────────────────────────────────────┘
```

## 1.2 최초 가설

1. 컨테이너는 호스트와 커널을 공유하므로 NVIDIA 커널 드라이버를 컨테이너 안에 따로 설치하는 구조가 아니다.
2. CUDA 이미지 안에는 CUDA 런타임이나 툴킷이 들어 있을 수 있지만, 그것만으로 GPU를 사용할 수는 없다.
3. 실제 GPU 제어는 호스트에 로드된 NVIDIA 커널 드라이버가 담당한다.
4. NVIDIA Container Toolkit은 호스트의 GPU 장치와 필요한 드라이버 구성요소를 컨테이너에 연결하는 다리 역할을 한다.
5. 따라서 경고는 컨테이너에서 호스트 NVIDIA 드라이버 쪽으로 내려가는 연결이 보이지 않는다는 뜻일 것이다.

## 1.3 최초 결론

```text
CUDA 런타임·툴킷이 없는 경고가 아니다.

컨테이너 안의 프로그램이 사용할 수 있는 NVIDIA 드라이버 인터페이스와
GPU 장치가 컨테이너에 제공되지 않은 상태를 뜻한다.
```

단, 이 시점에는 다음 두 경우를 구분하지 못했다.

- 호스트에 NVIDIA 드라이버 자체가 설치되지 않은 경우
- 호스트 드라이버는 정상인데 컨테이너에 전달되지 않은 경우

---

# 2. NVIDIA 공식 문서와 대조

## 2.1 공식 구조에서 확인한 내용

NVIDIA Container Toolkit은 단순히 환경변수 하나를 넣는 도구가 아니다. 컨테이너 런타임과 연결되어 OCI 설정을 수정하거나 hook/CDI를 사용해 NVIDIA GPU 장치와 필요한 드라이버 구성요소를 컨테이너에 제공한다.

현재 공식 문서에서 설명하는 주요 구성요소는 다음과 같다.

```text
Docker / containerd / CRI-O / Podman
                │
                ▼
NVIDIA Container Runtime 또는 CDI 연동
                │
                ▼
NVIDIA Container Runtime Hook
                │
                ▼
nvidia-container-cli / libnvidia-container
                │
                ▼
GPU 장치, 드라이버 라이브러리, 실행 파일 등을 컨테이너에 주입
```

Docker의 `--gpus` 방식에서는 런타임 연동을 통해 필요한 GPU가 선택되고, Toolkit 구성요소가 컨테이너 시작 전에 장치 접근과 드라이버 라이브러리 마운트를 준비한다.

## 2.2 내가 맞게 이해한 부분

### 맞음 1 — 커널 드라이버는 호스트에 있다

일반 Linux 컨테이너는 별도의 Linux 커널을 부팅하지 않는다. 따라서 컨테이너가 NVIDIA 커널 모듈을 직접 로드해서 GPU를 소유하는 구조가 아니라 호스트 커널에 로드된 드라이버를 사용한다.

### 맞음 2 — CUDA 툴킷과 NVIDIA 드라이버는 같은 것이 아니다

CUDA Toolkit은 다음과 같은 개발 및 실행 구성요소를 제공한다.

- `nvcc` 컴파일러
- CUDA 헤더
- CUDA Runtime인 `libcudart`
- cuBLAS 등의 CUDA 라이브러리
- 디버거와 프로파일러 등의 개발 도구

반면 NVIDIA 드라이버는 GPU 하드웨어와 통신하고 CUDA Driver API를 제공하는 기반이다. 이미지 안에 CUDA Toolkit이 있어도 사용할 수 있는 드라이버와 GPU가 연결되지 않으면 CUDA 연산은 실행되지 않는다.

### 맞음 3 — 컨테이너는 GPU를 자동 상속하지 않는다

호스트에서 `nvidia-smi`가 성공한다고 해서 일반 `docker run` 컨테이너가 자동으로 GPU를 볼 수 있는 것은 아니다. 컨테이너를 GPU 지원 방식으로 시작하고 NVIDIA Container Toolkit이 런타임에 연결되어 있어야 한다.

---

# 3. 대조 후 수정한 부분

## 수정 1 — “경고 = 호스트 드라이버 미설치”라고 단정하면 안 된다

### 처음 생각

```text
NVIDIA Driver was not detected
→ 호스트에 NVIDIA 드라이버가 설치되지 않았다.
```

### 수정

```text
NVIDIA Driver was not detected
→ 컨테이너 내부에서 사용할 수 있는 NVIDIA 드라이버 인터페이스를
  감지하지 못했다.
```

이 현상의 원인은 여러 가지일 수 있다.

1. 호스트 NVIDIA 드라이버가 설치되지 않았거나 로드되지 않음
2. NVIDIA Container Toolkit이 설치되지 않음
3. Toolkit은 설치됐지만 Docker/containerd에 설정되지 않음
4. 컨테이너 실행 시 `--gpus all` 같은 GPU 요청을 하지 않음
5. 권한, cgroup, CDI 설정 등의 문제로 GPU 장치가 주입되지 않음
6. 드라이버 라이브러리나 `/dev/nvidia*` 장치가 컨테이너에서 보이지 않음

따라서 이 경고는 **증상**이고, 호스트 드라이버 부재는 가능한 원인 중 하나다.

## 수정 2 — “드라이버는 전부 호스트에만 있고 컨테이너에는 아무것도 안 들어온다”는 표현은 부정확하다

### 처음 생각

```text
드라이버는 호스트에만 존재한다.
컨테이너에는 CUDA 런타임만 존재한다.
```

### 수정

NVIDIA **커널 드라이버 모듈**은 호스트 커널에 남아 있다. 하지만 컨테이너의 애플리케이션이 드라이버를 호출하려면 사용자 공간 드라이버 라이브러리와 장치 파일이 필요하다.

NVIDIA Container Toolkit은 필요한 항목을 컨테이너에서 사용할 수 있게 구성한다.

```text
호스트에 남는 것
- NVIDIA 커널 모듈
- 실제 GPU 제어

컨테이너에 노출·마운트되는 것
- /dev/nvidia* GPU 장치
- libcuda.so 등 필요한 사용자 공간 드라이버 라이브러리
- 설정에 따라 nvidia-smi 등의 드라이버 유틸리티
```

따라서 “드라이버 전체를 컨테이너에 설치한다”도 틀리고, “드라이버 관련 요소는 컨테이너에 하나도 들어오지 않는다”도 틀리다.

## 수정 3 — NVIDIA Container Toolkit을 단순 장치 패스스루라고만 보면 부족하다

Toolkit은 요청된 GPU를 선택하고, 컨테이너 런타임과 연동하여 OCI 설정이나 hook/CDI 구성을 통해 다음 작업을 수행한다.

- GPU 장치 노출
- 장치 접근 권한 설정
- 드라이버 라이브러리와 바이너리 제공
- 요청된 driver capability 반영
- 컨테이너 실행 전에 GPU 사용 환경 구성

즉, Toolkit은 **호스트 드라이버와 컨테이너 애플리케이션 사이의 런타임 통합 계층**이다.

---

# 4. 경고가 발생한 정확한 층

## 한 문장 답

> `NVIDIA Driver was not detected` 경고는 CUDA Toolkit 계층의 부재를 말하는 것이 아니라, 컨테이너 내부에서 호스트 NVIDIA 드라이버가 제공해야 할 사용자 공간 인터페이스와 GPU 장치를 사용할 수 없다는 뜻이다.

## 스택에서 표시

```text
컨테이너 애플리케이션
PyTorch / CUDA 프로그램
        │
        ▼
CUDA Runtime / CUDA 라이브러리     ← 이미지에 이미 존재할 수 있음
        │
        ▼
libcuda.so / NVIDIA Driver API     ← 여기부터 접근 불가
        │
======== 컨테이너 경계 ==========================================
        │
NVIDIA Container Toolkit           ← 미설정·미사용 가능
        │
GPU 장치 /dev/nvidia*              ← 컨테이너에 미노출 가능
        │
NVIDIA 호스트 커널 드라이버         ← 없거나, 있어도 연결이 안 됐을 수 있음
        │
NVIDIA GPU
```

경고가 관찰되는 위치는 컨테이너 내부지만, 실제 원인은 컨테이너 경계 아래 여러 층에 있을 수 있다.

---

# 5. 진단 순서

## 5.1 호스트 드라이버 확인

```bash
nvidia-smi
```

### 해석

- 실패: 호스트 드라이버 설치, 로드, GPU 인식부터 점검한다.
- 성공: 호스트 GPU와 드라이버는 대체로 정상이며 다음 단계로 간다.

추가 확인:

```bash
lsmod | grep nvidia
ls -l /dev/nvidia*
```

## 5.2 NVIDIA Container Toolkit 확인

```bash
nvidia-ctk --version
```

Docker 런타임 설정 확인:

```bash
cat /etc/docker/daemon.json
```

필요할 경우 공식 설치 절차에 따라 Docker를 설정한다.

```bash
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker
```

## 5.3 GPU를 요청한 컨테이너로 검증

```bash
sudo docker run --rm --runtime=nvidia --gpus all ubuntu nvidia-smi
```

### 해석 표

| 호스트 `nvidia-smi` | GPU 컨테이너 | 판단 |
|---|---|---|
| 실패 | 실패 | 호스트 드라이버 또는 GPU 인식 문제 |
| 성공 | 실패 | Container Toolkit, 런타임 설정, GPU 요청 또는 권한 문제 |
| 성공 | 성공 | 호스트 드라이버와 컨테이너 GPU 연결 정상 |

## 5.4 일반 컨테이너와 비교

```bash
# GPU를 요청하지 않음
sudo docker run --rm <CUDA_IMAGE> <COMMAND>

# GPU를 요청함
sudo docker run --rm --gpus all <CUDA_IMAGE> <COMMAND>
```

첫 번째에서 경고가 발생하고 두 번째가 정상이라면 CUDA 이미지가 잘못된 것이 아니라 **GPU가 컨테이너에 주입되지 않은 것**이 원인이다.

---

# 6. CUDA Runtime, Toolkit, Driver 구분

| 구성요소 | 주 위치 | 역할 | 없을 때 나타나는 대표 현상 |
|---|---|---|---|
| NVIDIA 커널 드라이버 | 호스트 커널 | GPU 하드웨어 제어 | 호스트 `nvidia-smi` 실패, GPU 장치 생성 실패 |
| NVIDIA 사용자 공간 드라이버 | 호스트 기반, Toolkit이 컨테이너에 제공 | CUDA Driver API, NVML 제공 | `libcuda.so` 탐색 실패, driver initialization 실패 |
| NVIDIA Container Toolkit | 호스트 | GPU 장치와 드라이버 요소를 컨테이너에 연결 | 호스트는 정상인데 컨테이너만 GPU를 못 봄 |
| CUDA Runtime | 주로 컨테이너 이미지 | CUDA 프로그램 실행 지원 | `libcudart.so` 로딩 실패 |
| CUDA Toolkit | 개발 환경 또는 devel 이미지 | 컴파일러, 헤더, 개발 도구 | `nvcc: command not found`, CUDA 코드 컴파일 불가 |
| PyTorch/TensorFlow | 컨테이너 이미지 | 상위 ML 프레임워크 | 프레임워크 import 또는 연산 API 사용 불가 |

핵심은 `nvcc`, `libcudart`, `libcuda`가 서로 다른 층이라는 점이다.

```text
nvcc       = CUDA 코드를 빌드하는 컴파일러
libcudart  = CUDA Runtime API 구현
libcuda    = NVIDIA 드라이버가 제공하는 CUDA Driver API
```

---

# 7. 최종 스택 지도

```text
┌───────────────────────────────────────────────────────────────┐
│ 컨테이너 사용자 공간                                         │
│                                                               │
│  애플리케이션                                                 │
│  Python / PyTorch / TensorFlow / CUDA binary                  │
│                         │                                     │
│                         ▼                                     │
│  CUDA Runtime 및 라이브러리                                   │
│  libcudart / cuBLAS / cuDNN                                   │
│                         │                                     │
│                         ▼                                     │
│  NVIDIA 사용자 공간 드라이버 인터페이스                       │
│  libcuda / NVML / 필요 유틸리티                               │
│  ※ 호스트 드라이버와 Toolkit을 통해 사용 가능                │
│                         │                                     │
│  /dev/nvidia* 장치                                            │
└─────────────────────────┼─────────────────────────────────────┘
                          │ 컨테이너 경계
┌─────────────────────────▼─────────────────────────────────────┐
│ 호스트 사용자 공간                                            │
│                                                               │
│  Docker / containerd / CRI-O                                  │
│                         │                                     │
│  NVIDIA Container Toolkit                                     │
│  nvidia-ctk / runtime / hook / CDI / libnvidia-container      │
│                         │                                     │
└─────────────────────────┼─────────────────────────────────────┘
                          │
┌─────────────────────────▼─────────────────────────────────────┐
│ 호스트 커널                                                   │
│                                                               │
│  NVIDIA 커널 드라이버                                         │
│  nvidia / nvidia_uvm / nvidia_modeset                         │
└─────────────────────────┬─────────────────────────────────────┘
                          │
┌─────────────────────────▼─────────────────────────────────────┐
│ NVIDIA GPU                                                    │
└───────────────────────────────────────────────────────────────┘
```

---

# 8. 최종 정리

## 내가 이제 설명할 수 있는 내용

- 컨테이너는 호스트 Linux 커널과 NVIDIA 커널 드라이버를 공유한다.
- CUDA Toolkit과 NVIDIA GPU Driver는 서로 다른 소프트웨어 계층이다.
- CUDA 이미지가 존재한다고 해서 GPU 접근까지 자동으로 제공되지는 않는다.
- NVIDIA Container Toolkit은 GPU 장치와 필요한 드라이버 요소를 컨테이너에 연결한다.
- `NVIDIA Driver was not detected`는 컨테이너가 NVIDIA 드라이버 인터페이스를 감지하지 못했다는 의미다.
- 이 경고만으로 호스트 드라이버가 미설치됐다고 단정할 수 없다.
- 호스트 `nvidia-smi` 성공 여부를 먼저 확인하면 문제 층을 빠르게 분리할 수 있다.

## 최종 답안

```text
W2에서 본 경고는 CUDA 런타임이나 CUDA Toolkit이 없다는 뜻이 아니다.

컨테이너 안에는 CUDA 라이브러리가 존재할 수 있지만,
컨테이너가 호스트 NVIDIA 드라이버가 제공하는 libcuda 계층과
/dev/nvidia* GPU 장치를 사용하지 못하고 있다는 뜻이다.

원인은 호스트 드라이버 부재일 수도 있지만,
호스트 드라이버가 정상이어도 NVIDIA Container Toolkit 미설정,
Docker/containerd 연동 실패, --gpus 옵션 누락 때문에 같은 경고가 발생한다.
```

---

# 9. 공식 문서 대조 기록

- NVIDIA Container Toolkit — Architecture Overview  
  https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/arch-overview.html

- NVIDIA Container Toolkit — Installation Guide  
  https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html

- NVIDIA Container Toolkit — Running a Sample Workload  
  https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/sample-workload.html

- NVIDIA CUDA Compatibility  
  https://docs.nvidia.com/deploy/cuda-compatibility/index.html

## 대조 후 틀렸던 부분 요약

```text
[틀린 표현]
경고가 떴으므로 호스트 NVIDIA 드라이버가 설치되지 않았다.

[수정]
컨테이너에서 드라이버 인터페이스가 보이지 않는다는 뜻이며,
호스트 드라이버 부재와 컨테이너 런타임 연결 실패를 추가 진단해야 한다.

[틀린 표현]
NVIDIA 드라이버는 전부 호스트에만 있고 컨테이너에는 드라이버 요소가 없다.

[수정]
커널 모듈은 호스트에 있지만, 사용자 공간 드라이버 라이브러리와 장치 파일은
Toolkit을 통해 컨테이너에서 사용할 수 있게 제공된다.

[틀린 표현]
NVIDIA Container Toolkit은 GPU 장치 하나만 패스스루한다.

[수정]
Toolkit은 런타임 hook 또는 CDI와 libnvidia-container를 이용해
장치, 라이브러리, 권한 및 OCI 실행 구성을 함께 준비한다.
```