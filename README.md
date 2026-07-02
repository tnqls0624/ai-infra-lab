# ai-infra-lab

백엔드 개발자 → **AI 인프라 엔지니어** 전환을 위한 단계적 실습 저장소.
GPU 서버 위에서 모델이 학습·서빙되는 전체 스택을 기초부터 직접 다루는 것이 목표다.

> **📍 학습 순서 정본은 [`ROADMAP.md`](ROADMAP.md) — 7블록, 19주+버퍼. 학습 우선.**
> Block 0 파이썬/PyTorch 기초 → 1 컨테이너&GPU → 2 GPU/CUDA → 3 서버·OS·네트워크 → 4 K8s+GPU → 5 서빙&학습 → 6 관측성&운영
> 블랙웰 특화 내용·서버 브링업 체크리스트는 ROADMAP 부록 A/B (참고용).

**현재**: Block 0 (파이썬 + PyTorch 감잡기). GPU가 필요한 Block 2부터는 클라우드 GPU 실습 환경(Block 1 게이트)이 전제.

## 디렉토리 구조

각 디렉토리는 [`ROADMAP.md`](ROADMAP.md)의 블록과 매핑된다. 착수한 디렉토리에는 블록별 `README.md` 스텁이 있다.

| 디렉토리 | 용도 | 블록 |
|---|---|---|
| `python/` | 파이썬 기초 실습 (`train_mnist.py`) | Block 0 |
| `docker/` | Dockerfile · GPU 컨테이너 | Block 1 |
| `docs/notes/` | **채점용 학습 노트** (명령 출력 포함 커밋) — gpu-access-decision, block2/3 노트 | Block 1~3 |
| `training/` | DDP 토이 학습 + 체크포인트 재개 | Block 5B |
| `serving/` | vLLM 서빙 + 벤치마크 (TRT-LLM은 프리빌트만) | Block 5A |
| `gateway/` | 서빙 인증/게이트웨이 (vLLM은 기본 무인증) | Block 5A |
| `mlflow/` | 실험 추적 (1런) | Block 5B |
| `kubernetes/` | K8s 매니페스트 · GPU Operator | Block 4 |
| `monitoring/` | DCGM · Prometheus/Grafana · 장애 플레이북 | Block 6 |
| `terraform/` | 인프라 코드화 (선택 — 컷 1순위) | Block 6 |
| `notebooks/` | 실험 노트북 | 공용 |
| `workflows/` | 워크플로우 오케스트레이션 (후순위) | 확장 |
| `models/` | 모델 산출물 (`.gitignore`, git 추적 안 함 — 백업 정책은 Block 6) | — |
| `docs/` | 학습 로그(`log.md`) · ops 핸드북 캡스톤 | — |

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
