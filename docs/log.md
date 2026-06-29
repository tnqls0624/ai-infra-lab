# AI Infra 학습 로그 (ai-infra-lab)

## 2026-06-29 (월) — W1 D1
- **오늘 한 것**: ai-infra-lab repo 생성, 디렉토리 골격(training/serving/gateway/docker/kubernetes/mlflow/workflows/monitoring/terraform/docs/notebooks/models) 커밋, GitHub(private) push
- **발생한 문제**: git remote URL에 PAT가 평문으로 박혀 노출됨
- **해결하거나 확인한 내용**: `git remote set-url`로 토큰 제거, gh keyring 인증으로 전환. (노출된 토큰은 GitHub에서 폐기·재발급 예정.) models/는 .gitignore 처리, origin 연결 확인
- **다음에 할 것**: W1 D2 — venv + PyTorch(CPU) 설치, requirements.txt 커밋
