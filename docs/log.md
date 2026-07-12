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
