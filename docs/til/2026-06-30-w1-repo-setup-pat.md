# [W1 D1~D3] 코드 한 줄 쓰기 전에 정리해야 했던 것들 — repo 골격, PAT 노출, venv

ai-infra-lab repo를 만들었다. training/serving/gateway/docker/kubernetes/mlflow/workflows/monitoring/terraform/docs/notebooks/models, 이렇게 12개 디렉토리 골격을 잡고 GitHub에 private로 push했다. 커밋 로그엔 "디렉토리 골격"이라고 적었는데, 나중에 다시 보니 실제로 바뀐 파일은 `.gitignore` 한 줄, `README.md` 한 줄뿐이었다. git은 빈 디렉토리를 추적하지 않아서, 실제 폴더는 안에 파일이 생겨야 트리에 따라온다는 걸 이때 알았다.

push하고 나서 remote를 다시 보니 origin URL에 PAT가 그대로 박혀 있었다. 토큰 값을 여기 적을 순 없지만 문제는 명확했다 — HTTPS remote URL에 인증정보를 그대로 넣어두면, 그 URL을 보는 모든 곳(터미널 히스토리, 로그, 스크롤백)에 그대로 노출된다. 바로 정리했다.

```
git remote set-url origin https://github.com/<user>/ai-infra-lab.git
```

URL에서 토큰을 빼고, 이후 인증은 gh CLI가 macOS Keychain에 저장하는 방식으로 바꿨다. 노출된 토큰은 GitHub에서 폐기하고 재발급할 예정이다. models/는 용량 큰 산출물이 들어갈 자리라 처음부터 .gitignore에 넣어뒀다.

다음 날은 venv + PyTorch 설치였다.

```
python -m venv .venv
pip install torch torchvision
```

torch 2.12.1, torchvision 0.27.1이 설치됐다. numpy·scikit-learn·jupyter까지 넣고 `pip freeze > requirements.txt`로 버전을 고정했다 — 113줄. 근데 커밋 전에 `git status`를 보니 `.venv/`가 통째로 untracked 상태로 잡혀 있었다. 그대로 add했으면 가상환경 전체가 git에 올라갈 뻔했다. .gitignore에 세 줄을 더 추가해서 막았다.

```
.venv/
__pycache__/
*.pyc
```

requirements.txt만 있으면 어디서든 pip install -r로 같은 환경을 재현할 수 있으니, .venv 자체가 git에 있을 이유는 없다.

`import torch`는 에러 없이 됐고, `torch.cuda.is_available()`은 False였다. 처음엔 뭔가 잘못됐나 싶었는데, 생각해보면 당연한 결과였다 — 지금 쓰는 건 CPU 빌드고 이 맥에는 CUDA GPU가 없다. False가 오히려 정상이다. 나중에 GPU 노드를 붙이는 블록으로 넘어가면 그때는 True로 바뀔 거다.

3일 동안 배운 걸 한 줄로 정리하면 이거다 — repo 하나 만드는 것도 결국 뭘 커밋하고 뭘 gitignore에 넣을지, 인증정보를 URL에 남기지 않는지부터 챙겨야 하는 문제였다. 코드 한 줄 쓰기 전에 먼저 정리해야 할 게 이만큼 있었다.
