# GPU 실습 환경 결정 (Block 1 종료 게이트)

> 이 문서가 커밋되어야 Block 2 진입 가능. ROADMAP.md "GPU 실습 환경" 참고.
> ⚠️ RunPod/Vast 컨테이너 대여 불가(root VM 필요) · V100/Pascal 불가(CUDA 13.x 미지원, Turing 이상) · EKS는 Block 4에서만.

## 메인 — root 단일 GPU VM (Block 2~3, 5~6 대부분)
- 프로바이더:
- 인스턴스 타입:
- 시간당 비용:
- 예상 사용량: 15~25h (≈ $50~100)

## 선택 — 멀티 GPU(NVLink) VM (Block 3 W3 실측용, 여유 시)
- 프로바이더/인스턴스:
- 계획: 2~3h 세션 (없으면 공개 topo 출력 주석으로 대체)

## 비용
- 예상 총액: $
- 결제/승인 방식:
