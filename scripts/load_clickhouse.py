import pandas as pd
from pathlib import Path
import traceback
from clickhouse_connect import get_client
from scripts.constants import (
    CLICKHOUSE_HOST,
    CLICKHOUSE_USER,
    CLICKHOUSE_PASSWORD,
    CLICKHOUSE_DB,
    CLICKHOUSE_TABLE,
    CSV_EXTRACTED_DIR,
)

REQUIRED_COLUMNS = [
    "FlightDate",
    "DayOfWeek",
    "Year",
    "Flights",
    "DepDelayMinutes",
    "Reporting_Airline",
    "Dest",
]


def ensure_table_exists(client):
    """Drop existing table and create new flights table."""
    drop_ddl = f"DROP TABLE IF EXISTS {CLICKHOUSE_TABLE}"
    print("🧸 Dropping existing flights table (if any)...")
    client.command(drop_ddl)

    create_ddl = f"""
    CREATE TABLE {CLICKHOUSE_TABLE} (
        FlightDate Date,
        DayOfWeek UInt8,
        Year UInt16,
        Flights UInt16,
        DepDelayMinutes Nullable(Float32),
        Reporting_Airline String,
        Dest String
    ) ENGINE = MergeTree
    ORDER BY (Year, FlightDate)
    """
    client.command(create_ddl)
    print("✅ flights table ready")


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Cleans and filters the dataframe to include only required columns with correct types."""
    for col in REQUIRED_COLUMNS:
        if col not in df.columns:
            df[col] = None  # add missing columns as nulls

    df = df[REQUIRED_COLUMNS].copy()  # Ensure we're working on a fresh copy

    # Type conversions with .loc to avoid SettingWithCopyWarning
    df.loc[:, "FlightDate"] = pd.to_datetime(df["FlightDate"], errors="coerce").dt.date
    df.loc[:, "DayOfWeek"] = (
        pd.to_numeric(df["DayOfWeek"], errors="coerce").fillna(0).astype("UInt8")
    )
    df.loc[:, "Year"] = (
        pd.to_numeric(df["Year"], errors="coerce").fillna(0).astype("UInt16")
    )
    df.loc[:, "Flights"] = (
        pd.to_numeric(df["Flights"], errors="coerce").fillna(0).astype("UInt16")
    )
    df.loc[:, "DepDelayMinutes"] = pd.to_numeric(df["DepDelayMinutes"], errors="coerce")
    df.loc[:, "Reporting_Airline"] = df["Reporting_Airline"].fillna("").astype(str)
    df.loc[:, "Dest"] = df["Dest"].fillna("").astype(str)

    return df


def load_all_csvs():
    loaded_files = 0
    failed_files = []

    client = get_client(
        host=CLICKHOUSE_HOST,
        username=CLICKHOUSE_USER,
        password=CLICKHOUSE_PASSWORD,
        database=CLICKHOUSE_DB,
    )

    ensure_table_exists(client)

    csv_files = sorted(Path(CSV_EXTRACTED_DIR).glob("*.csv"))
    for csv_path in csv_files:
        try:
            print(f"📦 Processing: {csv_path.name}")
            df = pd.read_csv(csv_path, dtype=str, low_memory=False)
            df = clean_dataframe(df)
            client.insert_df(CLICKHOUSE_TABLE, df)
            loaded_files += 1
            print(f"✅ Loaded: {csv_path.name} ({len(df)} rows)")
        except Exception as e:
            failed_files.append((csv_path.name, str(e)))
            print(f"❌ Failed to load {csv_path}: {e}")
            traceback.print_exc()

    print("\n📊 Summary:")

    print(f"✅ Loaded: {loaded_files} files out of {len(csv_files)}")
    if failed_files:
        print(f"❌ Failed files: {len(failed_files)}")
        for name, error in failed_files:
            print(f"   - {name}: {error}")


if __name__ == "__main__":
    load_all_csvs()
