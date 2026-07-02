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
- **다음에 할 것**: 너가 정해줘