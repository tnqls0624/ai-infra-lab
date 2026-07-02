# serving/ — Block 5A: 추론/서빙 트랙 (산출물 2개로 한정)

> 로드맵: [`ROADMAP.md` § Block 5](../ROADMAP.md)

## 산출물 (이게 전부 — 더 파지 않는다)
1. **vLLM**으로 오픈소스 LLM 1개 서빙(OpenAI 호환 API) + **처리량/지연 벤치마크 1회** (1.5주)
2. **TensorRT-LLM/NIM은 NGC 프리빌트 컨테이너 실행만** — 엔진 빌드 금지, 블랙웰 FP4 경로 존재 확인까지 (0.5주)

## 필수 — 서빙 보안
- vLLM OpenAI 서버는 **기본 무인증** → 사내망 노출 전 API key/게이트웨이(`../gateway/`) 최소 1겹
- 모델 웨이트는 **safetensors만** (pickle `.bin`은 로드 시 임의 코드 실행 위험)
- 오픈 모델 **상용 라이선스**(Llama 커뮤니티 라이선스 등) 확인

## 핵심 개념
PagedAttention · continuous batching · FP4/FP8 양자화와 처리량-지연 트레이드오프 (부록 A-7)
