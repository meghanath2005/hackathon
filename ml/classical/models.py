from __future__ import annotations

import torch
from torch import nn


class GRUForecast(nn.Module):
    def __init__(self, input_size: int = 6, hidden_size: int = 24, output_size: int = 2):
        super().__init__()
        self.gru = nn.GRU(input_size=input_size, hidden_size=hidden_size, batch_first=True)
        self.head = nn.Sequential(nn.Linear(hidden_size, 32), nn.ReLU(), nn.Linear(32, output_size))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        _, h = self.gru(x)
        return self.head(h[-1])
