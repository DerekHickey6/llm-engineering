import tiktoken

def encode(text) -> list[int]:
    enc = tiktoken.get_encoding("gpt2")
    token_integers = enc.encode(text)

    return token_integers

def decode(tokens: list[int]) -> str:
    dec = tiktoken.get_encoding("gpt2")
    decoded_string = dec.decode(tokens)

    return decoded_string



if __name__ == "__main__":
    with open("data/input.txt", 'r', encoding="utf-8") as f:
        lines = f.readlines()
        encoded = encode("\n".join(lines[0:2]))
        print(f"Encoded: {encoded}")
        print(f"Decoded: {decode(encoded)}")
