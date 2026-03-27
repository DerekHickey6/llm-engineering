# LLM from Scratch

A GPT-style language model built from scratch in PyTorch, trained on SpongeBob SquarePants transcripts. Every component is implemented by hand — tokenization, embeddings, self-attention, transformer blocks, training loop, and autoregressive text generation.

## What It Does

1. Preprocesses and concatenates SpongeBob episode transcripts into a single corpus
2. Tokenizes the corpus using GPT-2's BPE tokenizer (tiktoken)
3. Trains a GPT model from scratch on the corpus
4. Generates new SpongeBob-flavored dialogue autoregressively

## Architecture

```
Input tokens
    → Token Embedding + Positional Embedding
    → N × Transformer Block
        → LayerNorm
        → Multi-Head Self-Attention (causal mask)
        → Residual connection
        → LayerNorm
        → FeedForward (embed_dim → 4x → embed_dim, ReLU)
        → Residual connection
    → Final LayerNorm
    → Linear output head (embed_dim → vocab_size)
    → Logits over 50,257 tokens
```

## Tech Stack

- **PyTorch** — model definition, training loop, autograd
- **tiktoken** — GPT-2 BPE tokenizer (50,257 token vocabulary)
- **Google Colab (T4 GPU)** — used for full training runs

## Project Structure

```
llm-from-scratch/
├── src/
│   ├── prepare_data.py   # concatenates episode .txt files into input.txt
│   ├── tokenizer.py      # encode/decode wrappers around tiktoken
│   ├── dataset.py        # data loading, batching, get_batch()
│   ├── model.py          # GPT model: Head, MultiHeadAttention, FeedForward, TransformerBlock, GPT
│   ├── train.py          # training loop with AdamW optimizer
│   └── generate.py       # autoregressive text generation
├── data/
│   └── input.txt         # preprocessed SpongeBob corpus (~1.4M tokens)
├── models/
│   └── spongebob_gpt.pth # trained model weights
├── requirements.txt
└── README.md
```

## Setup

**1. Install dependencies**
```bash
pip install -r requirements.txt
```

**2. Prepare the data**
```bash
python src/prepare_data.py
```

**3. Train the model (GPU recommended)**
```bash
python src/train.py
```

**4. Generate text**
```bash
python src/generate.py
```

## Hyperparameters

| Parameter | Value |
|-----------|-------|
| vocab_size | 50,257 |
| embed_dim | 256 |
| num_heads | 4 |
| num_layers | 4 |
| block_size | 128 |
| batch_size | 32 |
| learning_rate | 3e-4 |
| epochs | 10,000 |

## Key Concepts

- **BPE Tokenization** — subword tokenization that handles any word by breaking it into known chunks
- **Token + Positional Embeddings** — combined into one vector; model learns to use both signals
- **Causal Self-Attention** — each token attends only to previous tokens via a lower-triangular mask
- **Scaled Dot-Product Attention** — scores scaled by √head_size to prevent softmax saturation
- **Multi-Head Attention** — multiple attention heads learn different relationships in parallel
- **Residual Connections** — `x = x + sublayer(x)` allows gradients to flow through deep networks
- **Layer Norm** — normalizes activations before each sublayer for stable training
- **Autoregressive Generation** — samples next token from predicted distribution, appends, repeats

## Sample Output

```
SpongeBob: Car Aw [ Hot Mother Well Honey Okay Patrick [ See Hey Okay
Sandy What What I We A Uh There How [ Wait All Means Yes Me No Again
Patrick Squid I Patrick [ Raw Squid My [ tomatoes With [ So Yeah ...
```

*Trained on CPU locally for 5,000 steps and on Colab T4 for 10,000 steps. A full 50,000 step run produces more coherent multi-sentence dialogue.*
