import os
import zipfile
from pathlib import Path
from typing import List

from constants import DATA_DIR, CSV_EXTRACTED_DIR


def extract_csvs_from_zip(zip_path: Path, extract_to: Path) -> List[Path]:
    """Extract all .csv files from a ZIP archive to a target directory."""
    extracted_files = []
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        for member in zip_ref.namelist():
            if member.lower().endswith(".csv"):
                zip_ref.extract(member, path=extract_to)
                extracted_file = extract_to / Path(member).name
                extracted_files.append(extracted_file)
                print(f"📦 Extracted: {extracted_file.name}")
            else:
                print(f"⏭️ Skipped non-CSV: {member}")
    return extracted_files


def extract_all_zips():
    """Extract all CSV files from ZIPs in the data directory."""
    os.makedirs(CSV_EXTRACTED_DIR, exist_ok=True)
    zip_files = sorted(Path(DATA_DIR).glob("*.zip"))

    for zip_file in zip_files:
        try:
            extract_csvs_from_zip(zip_file, Path(CSV_EXTRACTED_DIR))
        except Exception as e:
            print(f"❌ Failed to extract {zip_file.name}: {e}")


if __name__ == "__main__":
    extract_all_zips()
