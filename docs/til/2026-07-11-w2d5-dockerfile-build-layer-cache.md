# 학습 스크립트를 도커 이미지로 만들기 — 빌드 에러 4개와 레이어 캐시 실측

지난 글에서 컨테이너 안에 들어가 리눅스 기본기를 익혔다면, 이번엔 반대로 내 코드를 컨테이너에 실어 보낼 차례다. 목표는 단순했다. 앞서 만든 MNIST 학습 스크립트(train_mnist.py)를 CUDA 베이스 이미지에 탑재해서 `docker build`와 `docker run`이 통과하게 만드는 것. 지금 쓰는 맥에는 NVIDIA GPU가 없으니 일단 CPU로 빌드·실행을 검증하고, GPU 실행은 다음 단계로 미뤘다. 15줄짜리 Dockerfile 하나 쓰는 데 빌드 에러를 4번 만났고, 그 덕에 빌드 컨텍스트·레이어 캐시가 어떻게 동작하는지 눈으로 확인할 수 있었다. 이번 글에서는 그 에러 4개의 원인과, 소스 한 줄을 바꿔가며 실측한 레이어 캐시 동작을 정리한다.

## 이미지, 컨테이너, 레이어

Dockerfile을 쓰기 전에 개념부터 내 말로 정리했다.

- **이미지**: 애플리케이션과 그 실행에 필요한 종속성을 통째로 담은 스냅샷. 여러 개의 **레이어**가 겹겹이 쌓인 구조이고, 각 레이어는 한 번 만들어지면 변하지 않는다(불변).
- **컨테이너**: 이미지를 실행한 것. 이때 이미지 전체를 복사하는 게 아니라, 읽기 전용 레이어들 위에 **쓰기 가능한 레이어 한 장**을 얹는다(Copy-on-Write). 컨테이너 안에서 파일을 바꾸면 이 쓰기 레이어에만 기록되고, 원본 이미지는 그대로다.
- **볼륨**: 컨테이너가 삭제되면 쓰기 레이어도 함께 사라지므로, 남겨야 할 데이터는 호스트 쪽에 분리해서 마운트한다.

레이어 구조가 왜 중요한지는 실무에서 먼저 체감한 적이 있다. 예전에 금융권 온프레미스 프로젝트에서 배포를 하는데, 외부 파일 반입 절차가 엄격해서 용량이 큰 파일은 물리 매체로 서버실에 직접 반입해야 했고 작은 파일만 메일로 전달할 수 있었다. 수 GB짜리 이미지를 매번 통째로 반입하는 건 불가능에 가까웠는데, 베이스 이미지를 현장 레지스트리에 미리 넣어두고 이전 버전과 달라진 레이어만 뽑아 보내는 방식으로 바꾸자 배포물이 메일로 보낼 수 있는 크기까지 줄었다. 레이어가 불변이고 재사용된다는 성질이 그대로 배포 전략이 된 경우다.

## 베이스 이미지 고르기 — nvidia/cuda vs NGC PyTorch

GPU 학습용 이미지의 베이스는 크게 두 갈래다.

- **`nvidia/cuda:*-runtime`**: CUDA 런타임만 들어 있다. 파이썬도 PyTorch도 직접 설치해야 하지만, 그만큼 구성을 내가 통제하고 용량도 상대적으로 작다.
- **NGC PyTorch (`nvcr.io/nvidia/pytorch`)**: PyTorch, CUDA, 각종 최적화 라이브러리가 검증된 조합으로 다 들어 있다. 대신 8GB를 넘어가는 크기다.

이번엔 `nvidia/cuda:12.4.1-runtime-ubuntu22.04`를 골랐다. 직접 조립해봐야 레이어 구조가 몸에 익을 것 같았고, 위의 반입 경험 때문에 이미지 크기에 예민하기도 하다.

## 빌드 에러 4개

첫 시도에서 쓴 Dockerfile은 첫 `RUN`에서 바로 죽었고, 고치면 다음 명령이 죽는 식으로 4개의 에러를 순서대로 만났다.

**① `RUN apt install && pip install`** — 세 가지가 한 줄에 겹쳐 있었다. 컨테이너 이미지는 패키지 목록이 비어 있어서 `apt-get update` 없이는 아무것도 설치할 수 없고, 설치할 패키지 이름도 안 썼고, pip은 아직 설치 전이라 `command not found`였다. 고친 버전:

```dockerfile
RUN apt-get update && apt-get install -y python3 python3-pip && rm -rf /var/lib/apt/lists/*
```

마지막 `rm`은 apt가 받아둔 패키지 목록 캐시를 지워 레이어 용량을 줄이는 관례다. 스크립트에서는 `apt` 대신 `apt-get`을 쓴다 — `apt`는 대화형 용도라 "unstable CLI" 경고를 낸다.

**② `COPY requirements.txt .` → file not found** — 파일은 분명 리포 루트에 있는데 COPY가 못 찾았다. 원인은 **빌드 컨텍스트**. `docker build ./docker`처럼 빌드하면 도커는 `docker/` 디렉토리만 데몬으로 전송하고, COPY는 그 바깥을 절대 볼 수 없다. 해결은 컨텍스트를 리포 루트로 주고 Dockerfile 위치는 `-f`로 분리 지정하는 것:

```bash
docker build -f docker/Dockerfile -t mnist-train .
```

**③ pip이 scikit-learn을 못 찾음** — PyTorch CPU 휠을 받으려고 `--index-url https://download.pytorch.org/whl/cpu`를 붙였는데, 이 인덱스에는 torch 계열 패키지**만** 있다. requirements.txt에 있던 scikit-learn, jupyterlab은 여기 없으니 `No matching distribution found`. 그런데 애초에 train_mnist.py의 import는 torch와 torchvision뿐이었다. **로컬 개발 의존성(주피터 등)과 컨테이너 실행 의존성은 다르다** — 이미지에는 실행에 필요한 최소만 넣는다.

```dockerfile
RUN pip3 install --no-cache-dir torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

CPU 휠을 고른 이유: 기본 `pip install torch`는 CUDA용 휠(~2.5GB)을 받는다. 어차피 CPU 검증 단계이니 200MB짜리 CPU 휠로 빌드를 가볍게 유지했다.

**④ `CMD "echo start!"` → not found** — 빌드는 통과했는데 실행에서 죽었다. CMD를 이렇게 쓰면 셸이 따옴표 포함 문자열 전체를 명령어 이름 하나로 해석한다. 올바른 형태는 exec form(JSON 배열)이다:

```dockerfile
CMD ["python3", "train_mnist.py", "--epochs", "1"]
```

shell form은 `/bin/sh -c`를 거쳐 PID 1이 셸이 되고, exec form은 python이 직접 PID 1이 된다. 지난 글에서 "컨테이너의 PID 1은 내가 띄운 프로세스"라는 걸 확인했는데, CMD 형식이 바로 그 PID 1을 결정하는 자리였다.

## .dockerignore — 1GB가 136B가 되다

컨텍스트를 리포 루트로 바꾸자 새 문제가 생겼다. 리포에는 `.venv/`(991MB)와 데이터셋(63MB)이 있어서, 매 빌드마다 약 1GB를 데몬으로 전송하게 된 것이다. `.dockerignore`에 `.venv/`, `data/`, `models/`, `.git/` 등을 넣고 다시 빌드하니:

```
 => => transferring context: 136B
```

1GB급 전송이 136바이트로 줄었다. `.gitignore`가 커밋을 지키는 파일이라면 `.dockerignore`는 빌드 컨텍스트를 지키는 파일이다.

## 실행 — 드라이버 경고와 사라진 모델

`docker run --rm mnist-train`을 돌리자 CUDA 배너와 함께 경고가 떴다.

```
WARNING: The NVIDIA Driver was not detected.  GPU functionality will not be available.
...
INFO train_mnist: device=cpu (cuda available: False)
INFO train_mnist: epoch 0 done, loss=0.0898
INFO train_mnist: 모델 저장/재로드 검증 완료: models/mnist.pt
```

경고의 의미가 오늘 배운 것 중 가장 중요했다. 이미지에는 CUDA **런타임**만 들어 있고, **드라이버**는 호스트 것을 빌려 쓴다. GPU가 있는 호스트에서 `--gpus all`을 붙이면 NVIDIA Container Toolkit이 호스트 드라이버를 컨테이너에 주입해주는 구조다. 맥에는 NVIDIA 드라이버가 없으니 경고가 뜨는 게 정상이고, 스크립트는 의도대로 CPU로 학습을 완주했다.

한 가지 더 눈에 들어온 것: MNIST 데이터 다운로드도, 학습된 모델(models/mnist.pt)도 전부 컨테이너 **안에서** 일어났고, `--rm`으로 컨테이너가 종료되는 순간 함께 사라졌다. 같은 명령을 다시 돌리면 다운로드부터 다시 시작한다. 글 앞머리에 정리한 "볼륨으로 분리해야 하는 이유"를 몸으로 확인한 셈이다.

## 레이어 캐시 실측 — 주석 한 줄의 파장

마지막으로 캐시 동작을 실험했다. 아무것도 안 바꾸고 재빌드하면 5개 레이어 전부 `CACHED`, 빌드는 1.5초. 그다음 train_mnist.py에 주석 한 줄만 추가하고 재빌드했다:

```
 => CACHED [3/5] RUN apt-get update && apt-get install -y python3 python3-pip ...
 => CACHED [4/5] RUN pip3 install --no-cache-dir torch torchvision ...
 => [5/5] COPY python/W1/D5/train_mnist.py .
```

apt와 pip 레이어는 그대로 캐시를 탔고, COPY 레이어만 재실행됐다. 도커는 COPY 대상을 파일 내용 체크섬으로 비교하기 때문에 주석 한 줄이라도 바뀌면 그 레이어부터 무효화된다. 이미지 해시도 바뀌었다 — 레이어는 불변이고, 바뀐 레이어를 얹은 "새 이미지"가 만들어진 것이다.

반대 방향이 진짜 교훈이다. 만약 위쪽의 apt 줄을 수정하면 그 **아래에 있는** pip 레이어(제일 무겁고 느린 것)까지 전부 재실행된다. 캐시는 바뀐 명령부터 아래로 전부 깨진다. 그래서 Dockerfile은 **비싸고 안 바뀌는 명령을 위에, 싸고 자주 바뀌는 것(소스 코드)을 아래에** 쓴다. 완성된 Dockerfile:

```dockerfile
FROM nvidia/cuda:12.4.1-runtime-ubuntu22.04

WORKDIR /app

RUN apt-get update && apt-get install -y python3 python3-pip && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir torch torchvision --index-url https://download.pytorch.org/whl/cpu

COPY python/W1/D5/train_mnist.py .

CMD ["python3", "train_mnist.py", "--epochs", "1"]
```

## 정리

이번 실습에서 새로 안 것 네 가지.

1. COPY는 빌드 컨텍스트 바깥을 절대 볼 수 없다 — 컨텍스트는 루트로, Dockerfile 위치는 `-f`로 분리 지정하고, `.dockerignore`로 전송량을 지킨다(1GB → 136B).
2. 이미지에는 CUDA 런타임만 있고 드라이버는 호스트 것을 빌려 쓴다 — "Driver was not detected" 경고는 이 구조를 그대로 보여준다.
3. 레이어 캐시는 바뀐 명령부터 아래로 전부 무효화된다 — 비싸고 안 바뀌는 명령은 위에, 자주 바뀌는 소스는 아래에.
4. 컨테이너 안에서 만들어진 데이터는 컨테이너와 함께 사라진다 — 로컬 개발 의존성과 컨테이너 실행 의존성을 구분하듯, 코드(이미지)와 데이터(볼륨)도 분리해야 한다.

다음은 이 컨테이너에 볼륨을 붙여 데이터셋과 모델을 호스트에 남기고, named volume과 bind mount의 차이, 그리고 컨테이너의 쓰기 레이어(Copy-on-Write)를 `docker diff`로 직접 확인할 차례다.
