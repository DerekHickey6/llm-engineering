import torch.nn as nn
import torch

class GPT(nn.Module):
    def __init__(self, vocab_size, embed_dim, block_size):
        """Initializes model with vocab size, embed dims & block size"""
        super().__init__()
        self.token_embedding = nn.Embedding(vocab_size, embed_dim)
        self.position_embedding = nn.Embedding(block_size, embed_dim)

    def forward(self, x):
        """Forward pass -> looks up embeddings adds positional embeddings and returns combined representations"""
        T = x.shape[1]

        pos_ind = torch.arange(T)
        tok_embed = self.token_embedding(x)
        pos_embed = self.position_embedding(pos_ind)

        return tok_embed + pos_embed

class Head(nn.Module):
    def __init__(self, embed_dim, head_size, block_size):
        """Initizalizes attention head with embed_dim, head_Size and block size"""

        super().__init__()
        self.head_size = head_size
        self.query = nn.Linear(embed_dim, head_size, bias=False)
        self.key = nn.Linear(embed_dim, head_size, bias=False)
        self.value = nn.Linear(embed_dim, head_size, bias=False)
        self.register_buffer('tril', torch.tril(torch.ones(block_size, block_size)))    # Causal Mask

    def forward(self, x):
        """Calculates q,k,v and scores. Returns: Scores @ v"""
        q = self.query(x)
        k = self.key(x)
        v = self.value(x)

        # Attention Scores
        scores = q @ k.transpose(-2, -1) * self.head_size**-0.5

        # Apply Causal mask
        T = x.shape[1]
        scores = scores.masked_fill(self.tril[:T, :T] == 0, float('-inf'))
        scores = torch.softmax(scores, dim=-1)

        return scores @ v

class MultiHeadAttention(nn.Module):
    def __init__(self, embed_dim, num_heads, head_size, block_size):
        """creates a ModuleList of attention heads"""
        super().__init__()

        self.heads = nn.ModuleList([Head(embed_dim, head_size, block_size) for _ in range(num_heads)])
        self.proj = nn.Linear(embed_dim, embed_dim)

    def forward(self, x):
        """Feeds x through attention heads and concatenates them along last dim"""
        output = [head(x) for head in self.heads]

        concat_output = torch.cat(output, dim = -1)

        return self.proj(concat_output)




