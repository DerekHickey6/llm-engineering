import numpy as np
import torch
from tokenizer import encode

def get_batch(data: torch.Tensor, block_size: int, batch_size: int) -> tuple[torch.Tensor, torch.Tensor]:
    """Sample a random batch of input/target sequence pairs from the dataset."""

    if not torch.is_tensor(data) or not data.dim() == 1:
        raise ValueError("Data must be a 1D Tensor")

    ix = torch.randint(len(data) - block_size, (batch_size,))
    x = torch.stack([data[i:i+block_size] for i in ix])
    y = torch.stack([data[i+1:i+block_size+1] for i in ix])

    return x, y

def load_data(filepath: str) -> torch.Tensor:
    """Load a text file, encode it with the GPT-2 tokenizer, and return as a 1D tensor."""
    
    with open(filepath, "r", encoding="utf-8") as f:
        data = f.read()

    encoded_data = torch.tensor(encode(data), dtype=torch.long)
    return encoded_data

if __name__ == "__main__":
    data = load_data("data/input.txt")

    print(len(data))

    x, y = get_batch(data, batch_size=4, block_size=8)

    print(x.shape, y.shape)