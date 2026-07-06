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
- 발생한 문제: 없음
- 해결하거나 확인한 내용: 없음
- 다음에 할 것: 너가 적어줘
