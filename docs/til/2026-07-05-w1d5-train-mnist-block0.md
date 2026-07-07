# [W1 D5] train_mnist.py S2~S5 완주 — load_data 버그와 batch size가 loss에 미치는 영향

2026-07-05, ai-infra-lab Block 0을 끝냈다. `python/W1/D5/train_mnist.py`의 S2(load_data)만 하려던 날이었는데, 하루에 S5(모델 저장/재로드)까지 갔다.

## load_data가 Dataset을 그대로 돌려주고 있었다

S2를 처음 채운 코드는 이랬다.

```python
tf = transforms.ToTensor()
train_ds = datasets.MNIST(root=data_dir, train=True, download=True, transform=tf)
test_ds = datasets.MNIST(root=data_dir, train=False, download=True, transform=tf)
DataLoader(train_ds, batch_size=batch_size, shuffle=True)
return tuple(train_ds, test_ds)
```

두 가지가 틀렸다. `tuple()`은 인자를 하나(iterable)만 받는데 두 개를 넘겼다 — 사용법 혼동. 그리고 `DataLoader(...)`를 호출은 했지만 변수에 담지도, return에 넣지도 않았다. 함수 시그니처는 `tuple[DataLoader, DataLoader]`인데 실제로는 raw Dataset을 반환하려던 상태였다. 고쳐서:

```python
train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True)
test_loader = DataLoader(test_ds, batch_size=batch_size, shuffle=False)
return train_loader, test_loader
```

Dataset은 인덱싱 가능한 원본 데이터 묶음이고, DataLoader가 그걸 배치로 잘라 셔플까지 해주는 반복자다. 이 버그를 스스로 발견하고 고치면서 그 차이를 몸으로 확인했다.

## 학습 루프 5박자

S4의 train() 안쪽 루프는 어떤 프레임워크든 같은 구조였다.

```python
opt.zero_grad()              # ① 기울기 초기화
loss = loss_fn(model(x), y)  # ② forward + 손실
loss.backward()               # ③ backward
opt.step()                    # ④ 가중치 갱신
logger.info(...)              # ⑤ 기록
```

## y = wx + b, 그리고 batch size가 왜 loss를 바꾸나

병행해서 1차 방정식 y=ax+b를 그래프로 복습했다. 텐서에서는 이게 y = w(가중치)x(데이터) + b(바이어스)로 그대로 대응한다는 걸 확인했다.

batch_size를 64와 256으로 바꿔서 돌려봤다. 데이터는 60,000장으로 고정이라 총 연산량은 같다. 그런데 파라미터 업데이트 횟수는 60000/64=938회, 60000/256=235회로 4배 차이가 났다. 시간에는 영향이 미미했지만(총 연산량 동일) loss에는 영향이 컸다. batch size는 "속도" 파라미터가 아니라 "한 epoch 안에서 가중치를 몇 번 조정하는가"를 정하는 파라미터라는 걸 숫자로 확인한 실험이었다.

## state_dict 저장/재로드

S5에서 저장/재로드 검증까지 붙였다.

```python
args.model_out.parent.mkdir(parents=True, exist_ok=True)
torch.save(model.state_dict(), args.model_out)
m2 = SimpleNet()
m2.load_state_dict(torch.load(args.model_out))
```

모델 객체 전체를 pickle하는 게 아니라 파라미터(state_dict)만 저장하고, 같은 구조의 새 인스턴스에 얹어 검증하는 방식이다.

## 다음

Block 0은 여기서 끝. W2부터는 코드보다 Linux 기본기(`docker run -it ubuntu`에서 top/권한/journalctl 감각)와 수학(함수/이차함수/지수로그)을 병행한다.
