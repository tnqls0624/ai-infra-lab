# monitoring/ — Block 6: 관측성 & 운영 + 캡스톤

> 로드맵: [`ROADMAP.md` § Block 6](../ROADMAP.md)

## 여기에 채울 것
- W1: **DCGM Exporter** + Prometheus scrape → **Grafana GPU 대시보드** (사용률·온도·전력·ECC·XID, NVIDIA 레퍼런스 대시보드 활용)
- W2: 알림 규칙(OOM·XID·온도 임계) + **장애 플레이북** — 드라이버 크래시, "GPU fallen off the bus"(XID 79), ECC 에러의 의미와 대응
  + 패치 위생: Security Bulletin 구독, 변경 전 스냅샷·롤백 개념, 드라이버 브랜치 EOL 추적
- W3: 백업 개념(체크포인트·웨이트 — `models/`는 git 미추적), GPU 유휴율 추적, (선택) Terraform/Ansible

## 🎓 캡스톤 — ops 노트 종합 (`../docs/`)
Block 2~6 노트를 **"GPU 인프라 운영 핸드북"** 하나로 종합 — 버전 호환성 매트릭스, 장애 플레이북, 검증 명령 모음. 학습의 총정리이자 실무 투입 시 바로 쓸 자산.

## 완료 기준
Grafana 대시보드 1개 + 장애 플레이북 + 캡스톤 핸드북.
