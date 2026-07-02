# kubernetes/ — Block 4: 쿠버네티스 + GPU (코어 2주 + 조건부 2주)

> 로드맵: [`ROADMAP.md` § Block 4](../ROADMAP.md)
> **단일 노드 서버 1대는 Docker+systemd+DCGM만으로 운영 시작 가능** — K8s는 서버 가동의 전제조건이 아니다.

## 코어 (2주)
- W1: `kind` 클러스터 — Deployment/Service/namespace + Helm 기본 (CPU 로컬, 매니페스트 커밋)
- W2: 클라우드 GPU 노드에 **GPU Operator** 배포 → GPU Pod 1개 (`resources.limits."nvidia.com/gpu"`), `kubectl describe` 출력 커밋

## 조건부 (+2주, 필요해지면)
- **MIG**: 여러 팀이 GPU를 나눠 쓰는 수요가 생기면
- 스케줄러(Kueue/Volcano/Slurm) 비교는 **1페이지 결정 노트**로 한정 — 용도 '학습' 확정 시 Slurm 실습 추가

## 완료 기준
kind 매니페스트 + GPU Operator 배포 기록 + GPU Pod 스케줄링 증적.
