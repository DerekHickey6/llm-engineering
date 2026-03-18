import datetime
import json
import os
from pathlib import Path

def log_interaction(question: str, context: str, answer: str, latency: float, scores: dict):
    interaction_dict = {"question": question,
                        "context": context,
                        "answer": answer,
                        "latency": latency,
                        "score": scores,
                        "Time": datetime.datetime.now().isoformat()}

    file_path = Path("log/interactions.jsonl")

    os.makedirs("log", exist_ok=True)

    with open(file_path, "a", encoding="utf-8") as json_file:
        json.dump(interaction_dict, json_file)
        json_file.write(os.linesep)

if __name__ == "__main__":
    log_interaction("Who", "When", "Me", 3.14, {"score1": 1})