from datasets import load_dataset
from transformers import AutoTokenizer

def load_train_test_data(dataset: str):
    """Return: Train, Test splits"""
    dataset = load_dataset(dataset)

    tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")

    def tokenize(examples):
        return tokenizer(examples["text"], truncation=True, padding=True)

    train_data = dataset["train"].map(tokenize, batched=True)
    test_data = dataset["test"].map(tokenize, batched=True)

    return train_data, test_data


if __name__ == "__main__":
    train, test = load_train_test_data("imdb")
    print(train)
    print(test)