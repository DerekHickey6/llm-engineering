import torch.nn.functional as F
from tqdm import tqdm

from dataset import load_data, get_batch
from model import GPT


import torch

# HYPERPARAMS
VOCAB_SIZE = 50257
EMBED_DIM = 128
NUM_HEADS = 4
NUM_LAYERS = 3
BLOCK_SIZE = 64
BATCH_SIZE = 16
LEARNING_RATE = 3e-4
EPOCHS = 5000

data = load_data("data/input.txt")

model = GPT(vocab_size=VOCAB_SIZE,
            num_heads=NUM_HEADS,
            num_layers=NUM_LAYERS,
            embed_dim=EMBED_DIM,
            block_size=BLOCK_SIZE)

optimizer = torch.optim.AdamW(model.parameters(), lr=LEARNING_RATE)

# Training Loops
for epoch in tqdm(range(EPOCHS)):
    x, y = get_batch(data, block_size=BLOCK_SIZE, batch_size=BATCH_SIZE)

    logits = model(x)

    loss = F.cross_entropy(logits.view(-1, VOCAB_SIZE), y.view(-1))

    optimizer.zero_grad()

    loss.backward()

    optimizer.step()

    # Visualize
    if epoch % 500 == 0:
        print(f"Step {epoch} | Loss: {loss.item():.4f}")

torch.save(model.state_dict(), "models/model.pth")
