import os
import pandas as pd
from collections import Counter
from typing import List, Set

EXTRACTED_DIR = "data/extracted"


def get_all_csv_paths(directory: str) -> List[str]:
    return [
        os.path.join(directory, file)
        for file in os.listdir(directory)
        if file.endswith(".csv")
    ]


def gather_all_columns(csv_paths: List[str]) -> Set[str]:
    unique_columns = set()
    column_counter = Counter()

    for path in csv_paths:
        try:
            df = pd.read_csv(path, nrows=0, on_bad_lines="skip")
            cols = list(df.columns)
            column_counter.update(cols)
            unique_columns.update(cols)
        except Exception as e:
            print(f"⚠️ Skipped {path}: {e}")

    return unique_columns, column_counter


if __name__ == "__main__":
    paths = get_all_csv_paths(EXTRACTED_DIR)
    all_columns, counter = gather_all_columns(paths)

    print("\n📋 All unique columns found across CSVs:")
    for col in sorted(all_columns):
        print(f"- {col}")

    print("\n📊 Column frequency (how many files each appeared in):")
    for col, count in counter.most_common():
        print(f"{col:40} : {count}")
