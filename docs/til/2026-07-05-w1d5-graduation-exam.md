# [W1 D5] 졸업 시험 — 예외는 목격해야 안다

일요일 저녁부터 밤까지 train_mnist.py로 졸업 시험 세 문제를 풀었다. 코드를 읽어서 아는 것과 실행해서 보는 것의 차이가 컸던 하루였다.

첫 문제는 네트워크를 끊고 실행하는 거였다. load_data가 MNIST를 다운로드하다 실패하면 어떻게 죽는지 보라는 조건. Wi-Fi를 끄고 돌렸더니 torchvision 내부에서 socket.gaierror가 urllib.error.URLError로 올라가고, 그게 결국 RuntimeError로 다시 포장돼 튀어나왔다. 문제는 main()의 except가 NotImplementedError, OSError 두 개뿐이었다는 것. RuntimeError는 둘 다 아니라서 그대로 unhandled로 터졌다. torchvision이 네트워크 예외를 RuntimeError로 감싼다는 사실은 문서로 읽은 게 아니라 트레이스백을 직접 보고서야 알았다.

두 번째 문제는 models/ 디렉토리 권한을 없애고 torch.save를 실행하는 거였다. EACCES가 나면서 이번에도 RuntimeError로 재포장됐는데, 여기서 진짜 버그를 발견했다. main()의 except OSError 브랜치는

```python
except OSError as e:
    logger.error("파일/네트워크 I/O 실패: %s", e);
    return
```

bare return이었다. return은 None을 반환하고, sys.exit(main())은 곧 sys.exit(None) — exit 0. I/O가 실패했는데 프로그램은 성공했다고 보고한 것이다. 이걸 고쳐 커밋한 게 8761381이다.

```python
except (OSError, RuntimeError) as e:
    logger.error("파일/네트워크 I/O 실패: %s", e);
    return 1
```

except 대상도 RuntimeError까지 넓혔다. 두 실험에서 목격한 재포장 사실을 그대로 코드에 반영한 것.

세 번째는 --device 플래그였는데 두 번 실패했다. 1차는 cuda가 없는 환경에서 --device cuda를 줘도 검사 없이 조용히 cpu로 넘어가는 구조였다. 2차는 pick_device 쪽 argparse 오타로 실행 자체가 죽었는데, 이번엔 내가 직접 돌려보지 않고 리뷰만 요청했다가 그대로 걸렸다. 교훈은 명확했다. 셀프 실행 없이 리뷰 요청하지 말 것. 결국 코치가 준 코드로 마감했다.

```python
if requested == "cuda" and not torch.cuda.is_available():
    raise ValueError("cuda 요청됐지만 이 환경엔 CUDA 없음")
```

조용한 폴백을 없애고 fail-fast로 바꿔서 --device auto/cpu/cuda 인수 매트릭스를 다 통과시켰다.

라이브러리가 예외를 어떻게 재포장하는지는 문서를 읽어서 아는 게 아니라 직접 끊어보고 traceback으로 확인해야 안다는 게 이번 시험이 남긴 결론이다.
