from pathlib import Path

def prepare_data(directory_path: str) -> None:
    """Concatenate all .txt files in a directory into a single data/input.txt file."""
    
    directory_path = Path(directory_path)
    with open("data/input.txt", "a", encoding="utf-8") as output_file:

        for file in directory_path.glob("*.txt"):
            with open(file, "r", encoding="utf-8", errors="ignore") as f:
                data = f.read()

                output_file.write(data)


if __name__ == "__main__":
    prepare_data("data/SpongeBob_SquarePants_Transcripts")