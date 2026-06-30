# ai-infra-lab

백엔드 개발자 → **AI Infrastructure / MLOps 엔지니어** 전환을 위한 단계적 실습 저장소.
하나의 repo를 단계적으로 키우며 다음 파이프라인을 직접 만든다:

> **PyTorch 모델 학습 → 저장 → FastAPI 추론 API → Docker → Kubernetes(GPU) → vLLM 서빙 → 사내 LLM 플랫폼**

K8s/GPU/분산학습/vLLM은 블록2(13~24주)에서 합류. 지금은 **블록1: Python/ML → PyTorch → FastAPI → Docker**.

## 디렉토리 구조

| 디렉토리 | 용도 |
|---|---|
| `training/` | PyTorch 학습 코드 |
| `serving/` | FastAPI 추론 API |
| `gateway/` | NestJS API Gateway (블록2) |
| `docker/` | Dockerfile |
| `kubernetes/` | K8s 매니페스트 (블록2) |
| `mlflow/` | 실험 관리 (블록2) |
| `workflows/` | Argo Workflows (블록2) |
| `monitoring/` | Prometheus/Grafana (블록2) |
| `terraform/` | EKS IaC (블록2) |
| `notebooks/` | 실험 노트북 |
| `models/` | 모델 산출물 (`.gitignore`, git 추적 안 함) |
| `docs/` | 학습 로그(`log.md`) 등 |

---

## 학습 운영 — study-coach

이 repo의 학습은 별도 vault(`obsidian_sync`)의 **study-coach** 시스템으로 관리된다.
- **진도 정본**: `obsidian_sync/.claude/runtime/study-state.md` (git 공유 → 회사/집 두 Mac 동기화)
- **오늘 항목**: 매일 아침 cron(또는 `/study-coach brief`)이 `study-today.md`에 생성
- **검토·채점**: `/study-coach review`가 이 repo의 커밋·`docs/log.md`를 **읽기 전용**으로 보고 진도를 체크

### 매일 사용 순서 (4단계)

```
①  시작   →  ②  공부      →  ③  회고        →  ④  저장
 review      (이 repo)       docs/log.md      git push
```

| 단계 | 무엇을 | 어떻게 | 어디서 |
|---|---|---|---|
| **① 시작** | 어제 채점 + 오늘 항목 받기 | `/study-coach review` (아침 cron이 자동으로도 함) | obsidian_sync |
| **② 공부** | 가이드대로 학습·코딩 | 브리핑의 🎯개념·✅완료 기준 보고 진행 | ai-infra-lab |
| **③ 회고** | 4줄 일지 작성 | `docs/log.md`에 직접 작성 | ai-infra-lab |
| **④ 저장** | 커밋·푸시 | `git add → commit → push` | ai-infra-lab |

> `review`가 "어제 채점 + 오늘 브리핑"을 한 번에 한다 → **하루 시작에 review 1번**. 다음 날 review가 어제의 ②③④(커밋된 산출물)를 검토한다.

### 회고(`docs/log.md`) 형식

학습 끝에 아래 4줄을 직접 적는다 (이게 review 피드백과 면접 회고의 원천):

```markdown
## 2026-XX-XX (요일) — W1 Dx
- 오늘 한 것:
- 발생한 문제:
- 해결하거나 확인한 내용:
- 다음에 할 것:
```

### 꼭 지킬 규칙 2개

1. **자리 뜨기 전 `git push`** (회사 퇴근 전 / 집에서 자기 전) — 검토는 *커밋된 것만* 본다.
2. **다른 Mac으로 옮기면 먼저 `git pull`** — vault와 이 repo 둘 다.
   ```bash
   git -C ~/Desktop/Project/obsidian_sync pull   # 진도
   git -C ~/Desktop/Project/ai-infra-lab pull     # 학습 코드
   ```

### 누가 무엇을 쓰나

| 파일 | 작성 주체 |
|---|---|
| `study-today.md` (오늘 항목) | 🤖 시스템 자동 |
| `study-state.md` (진도·채점) | 🤖 review 자동 |
| **`docs/log.md` (학습 일지)** | **🙋 본인이 직접** |

---

## 환경 재현

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -c "import torch; print(torch.__version__, torch.cuda.is_available())"
```
