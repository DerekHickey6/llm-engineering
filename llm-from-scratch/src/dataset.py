import numpy as np
import torch

def get_batch(data, block_size, batch_size):
    if not torch.is_tensor(data) or not data.dim() == 1:
        raise ValueError("Data must be a 1D Tensor")

    ix = torch.randint(len(data) - block_size, (batch_size,))
    x = torch.stack([data[i:i+block_size] for i in ix])
    y = torch.stack([data[i+1:i+block_size+1] for i in ix])

    return x, y

def load_data(filepath):
    pass