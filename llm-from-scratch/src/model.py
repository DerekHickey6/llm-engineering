import torch.nn as nn
import torch

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


class FeedForward(nn.Module):
    def __init__(self, embed_dim):
        """Initialize feedforward network with expand-and-compress MLP (4x hidden dim)."""
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(embed_dim, 4*embed_dim),
            nn.ReLU(),
            nn.Linear(4 * embed_dim, embed_dim)
        )

    def forward(self, x):
        """Pass x through the feedforward network and return the result."""
        return self.net(x)


class TransformerBlock(nn.Module):
    def __init__(self, embed_dim, num_heads, block_size):
        """Initialize transformer block with multi-head attention, feedforward, and layer norms."""
        super().__init__()
        head_size = embed_dim // num_heads
        self.attention = MultiHeadAttention(embed_dim, num_heads, head_size, block_size)
        self.ff = FeedForward(embed_dim)
        self.ln1 = nn.LayerNorm(embed_dim)
        self.ln2 = nn.LayerNorm(embed_dim)

    def forward(self, x):
        """Apply attention and feedforward sublayers with residual connections and layer norm."""
        x = x + self.attention(self.ln1(x))
        x = x + self.ff(self.ln2(x))
        return x
    

class GPT(nn.Module):
    def __init__(self, vocab_size, num_heads, num_layers, embed_dim, block_size):
        """Initializes model with vocab size, embed dims & block size"""
        super().__init__()
        self.token_embedding = nn.Embedding(vocab_size, embed_dim)
        self.position_embedding = nn.Embedding(block_size, embed_dim)

        self.blocks = nn.Sequential(
            *[TransformerBlock(embed_dim, num_heads, block_size) for _ in range(num_layers)]
        )
        self.ln_final = nn.LayerNorm(embed_dim)
        self.output_head = nn.Linear(embed_dim, vocab_size)

    def forward(self, x):
        """Forward pass -> looks up embeddings adds positional embeddings and returns combined representations"""
        T = x.shape[1]

        pos_ind = torch.arange(T)
        tok_embed = self.token_embedding(x)
        pos_embed = self.position_embedding(pos_ind)

        logits = self.output_head(self.ln_final(self.blocks(tok_embed + pos_embed)))

        return logits