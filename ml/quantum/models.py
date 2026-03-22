from __future__ import annotations

import pennylane as qml
import torch
from pennylane import numpy as np
from torch import nn


class HybridQuantumForecaster(nn.Module):
    def __init__(self, input_size: int = 6, hidden_size: int = 16, n_qubits: int = 4):
        super().__init__()
        self.encoder = nn.GRU(input_size=input_size, hidden_size=hidden_size, batch_first=True)
        self.pre_q = nn.Linear(hidden_size, n_qubits)
        self.n_qubits = n_qubits

        dev = qml.device("default.qubit", wires=n_qubits)

        @qml.qnode(dev, interface="torch")
        def circuit(inputs, weights):
            qml.AngleEmbedding(inputs, wires=range(n_qubits), rotation="Y")
            qml.BasicEntanglerLayers(weights, wires=range(n_qubits))
            return [qml.expval(qml.PauliZ(i)) for i in range(n_qubits)]

        weight_shapes = {"weights": (2, n_qubits)}
        self.q_layer = qml.qnn.TorchLayer(circuit, weight_shapes)
        self.head = nn.Sequential(nn.Linear(n_qubits, 16), nn.ReLU(), nn.Linear(16, 2))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        _, h = self.encoder(x)
        q_in = torch.tanh(self.pre_q(h[-1])) * (np.pi / 2)
        q_out = self.q_layer(q_in)
        return self.head(q_out)
