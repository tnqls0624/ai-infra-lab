"""MNIST 학습 CLI — Block 0 통합 산출물.

이 파일 하나에 Block 0의 파이썬 주제를 전부 녹인다:
타입힌트 · argparse · logging · 클래스(nn.Module) · 예외처리 · 파일 저장/로드

세션 진행 (TODO를 위에서부터 하나씩 채운다 — 채울 때마다 커밋):
  [x] S1: 뼈대 — argparse + logging + device 선택  (완성된 예시: 읽고 이해할 것)
  [ ] S2: load_data()  구현  → W1 완료
  [ ] S3: SimpleNet    구현
  [ ] S4: train()      구현
  [ ] S5: 모델 저장/로드 + 예외처리 마무리  → Block 0 완료

실행 (repo 루트에서):
  python python/train_mnist.py --epochs 1
  python python/train_mnist.py --help

지금 상태로도 실행된다 — 미구현 TODO에 도달하면 어떤 세션을 채울 차례인지
알려주고 종료한다. (빨간불 → 하나씩 초록불로 만드는 방식)
"""
from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

import torch
from torch import nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

logger = logging.getLogger("train_mnist")


# ── S1. 뼈대 (완성된 예시 — 이 세 함수가 "인프라 도구의 기본 골격"이다) ──────


def setup_logging(verbose: bool) -> None:
    """print 대신 logging을 쓰는 이유:
    레벨(INFO/DEBUG)로 출력량 제어, 타임스탬프 자동 기록,
    서버에서는 파일·수집기(예: journald)로 그대로 전환 가능.
    """
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """CLI 인자 정의. nvidia-smi, kubectl 등 인프라 도구는 전부 이 인터페이스다.

    타입힌트 읽는 법: `argv: list[str] | None` = "str 리스트 또는 None".
    """
    p = argparse.ArgumentParser(description="MNIST 학습 CLI (Block 0 통합 산출물)")
    p.add_argument("--epochs", type=int, default=1, help="학습 epoch 수")
    p.add_argument("--batch-size", type=int, default=64, help="미니배치 크기")
    p.add_argument("--lr", type=float, default=1e-3, help="learning rate")
    p.add_argument("--data-dir", type=Path, default=Path("data"),
                   help="MNIST 다운로드 경로 (.gitignore 대상)")
    p.add_argument("--model-out", type=Path, default=Path("models/mnist.pt"),
                   help="학습된 모델 저장 경로 (models/는 git 미추적)")
    p.add_argument("--verbose", action="store_true", help="DEBUG 로그 출력")
    return p.parse_args(argv)


def pick_device() -> torch.device:
    """GPU가 있으면 cuda, 없으면 cpu.

    주의: is_available()=True여도 연산이 죽을 수 있다(휠에 해당 GPU 커널 부재)
    — Block 2 W2 함정 재현 랩에서 직접 겪어본다.
    """
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    logger.info("device=%s (cuda available: %s)", device, torch.cuda.is_available())
    return device


# ── S2. TODO(나): 데이터 로드 — 이걸 채우면 W1 완료 ─────────────────────────


def load_data(data_dir: Path, batch_size: int) -> tuple[DataLoader, DataLoader]:
    """MNIST를 내려받아 (train_loader, test_loader)를 돌려준다.

    힌트 (3단계):
      1) from torchvision import datasets, transforms  (파일 상단 import에 추가)
      2) tf = transforms.ToTensor()  # 이미지(PIL) → 텐서(0~1 float)
         train_ds = datasets.MNIST(root=data_dir, train=True,  download=True, transform=tf)
         test_ds  = datasets.MNIST(root=data_dir, train=False, download=True, transform=tf)
      3) DataLoader(train_ds, batch_size=batch_size, shuffle=True) / test는 shuffle=False
    확인: 구현 후 실행하면 data/ 밑에 파일이 내려오고, 다음 TODO(S3) 메시지가 떠야 한다.
    """
    tf = transforms.ToTensor();
    train_ds = datasets.MNIST(root=data_dir, train=True, download=True, transform=tf);
    test_ds = datasets.MNIST(root=data_dir, train=False, download=True, transform=tf);
    DataLoader(train_ds, batch_size=batch_size, shuffle=True);
    # raise NotImplementedError("S2: load_data()를 구현하세요 (docstring 힌트 참고)")
    return tuple(train_ds, test_ds);


# ── S3. TODO(나): 모델 — 28x28 흑백 이미지를 0~9로 분류하는 최소 신경망 ────


class SimpleNet(nn.Module):
    """힌트: __init__에서 nn.Sequential(
             nn.Flatten(),            # 28x28 → 784
             nn.Linear(784, 128), nn.ReLU(),
             nn.Linear(128, 10),      # 클래스 10개
           )를 self.net에 담고, forward(self, x)는 self.net(x)를 반환.
    super().__init__() 호출은 필수 — nn.Module 초기화가 먼저다.
    """

    def __init__(self) -> None:
        super().__init__()
        raise NotImplementedError("S3: SimpleNet 레이어를 정의하세요")

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        raise NotImplementedError("S3: forward를 구현하세요")


# ── S4. TODO(나): 학습 루프 ─────────────────────────────────────────────────


def train(model: nn.Module, loader: DataLoader, device: torch.device,
          epochs: int, lr: float) -> None:
    """힌트 (학습 루프의 5박자 — 어떤 프레임워크든 이 구조다):
      loss_fn = nn.CrossEntropyLoss(); opt = torch.optim.Adam(model.parameters(), lr=lr)
      for epoch in range(epochs):
          for x, y in loader:
              x, y = x.to(device), y.to(device)   # ← 데이터도 GPU로 (모델만 옮기면 에러!)
              opt.zero_grad()                      # ① 기울기 초기화
              loss = loss_fn(model(x), y)          # ② forward + 손실
              loss.backward()                      # ③ backward
              opt.step()                           # ④ 가중치 갱신
          logger.info("epoch %d done, loss=%.4f", epoch, loss.item())  # ⑤ 기록
    """
    raise NotImplementedError("S4: train() 학습 루프를 구현하세요")


# ── 실행 흐름 (S5에서 저장/로드를 여기에 추가) ──────────────────────────────


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    setup_logging(args.verbose)
    logger.info("hyperparams: epochs=%d batch_size=%d lr=%g",
                args.epochs, args.batch_size, args.lr)
    device = pick_device()

    try:
        train_loader, _test_loader = load_data(args.data_dir, args.batch_size)
        model = SimpleNet().to(device)  # 모델을 device로 — GPU 학습의 첫 줄
        train(model, train_loader, device, epochs=args.epochs, lr=args.lr)

        # TODO(나) S5: 학습된 모델 저장/재로드 검증
        #   힌트: args.model_out.parent.mkdir(parents=True, exist_ok=True)
        #         torch.save(model.state_dict(), args.model_out)
        #         재로드: m2 = SimpleNet(); m2.load_state_dict(torch.load(args.model_out))
        #   + load_data의 다운로드 실패(네트워크) 같은 예외를 try/except로 구분해
        #     "무엇이 왜 실패했는지" 로그로 남기기 — 인프라 코드의 기본기.
        logger.info("완료: 모델 저장은 S5에서 구현")

    except NotImplementedError as e:
        logger.error("다음 세션 과제 → %s", e)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
