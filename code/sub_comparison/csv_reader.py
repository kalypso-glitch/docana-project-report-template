
import csv

def read_csv(file_path: str) -> list[dict]:
    with open(file_path, newline="") as f:
        data = list(csv.DictReader(f))
    return data