from tokenizer import encode, decode
import torch

def generate(model, prompt, max_new_tokens=200):
    """Generates the response from model given the output length"""
    encoded_prompt = torch.tensor(encode(prompt)).unsqueeze(0)
    context = encoded_prompt

    for _ in range(max_new_tokens):
        # Crop to context to block size
        encoded_prompt = encoded_prompt[:, -model.block_size:]

        logits = model(encoded_prompt)

        # Extract last logits for next token in sequence
        last_pos_logits = logits[:, -1, :]

        probs = torch.softmax(last_pos_logits, dim=-1)

        token = torch.multinomial(probs, num_samples=1)

        context = torch.cat([context, token], dim=1)

    output = decode(context[0].tolist())

    return output


if __name__ == "__main__":
    from model import GPT
    import torch

    # Load the trained model
    model = GPT(vocab_size=50257, embed_dim=256, num_heads=4, num_layers=4, block_size=128)
    model.load_state_dict(torch.load("models/spongebob_gpt.pth", map_location=torch.device('cpu')))
    model.eval()

    output = generate(model, "SpongeBob:", max_new_tokens=200)
    print(output)
