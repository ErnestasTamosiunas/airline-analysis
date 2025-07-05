import psycopg2
import io
from clickhouse_connect import get_client
from scripts.constants import (
    CLICKHOUSE_HOST,
    CLICKHOUSE_PASSWORD,
    CLICKHOUSE_PORT,
    CLICKHOUSE_DB,
    CLICKHOUSE_TABLE,
    CLICKHOUSE_USER,
    POSTGRES_HOST,
    POSTGRES_PORT,
    POSTGRES_USER,
    POSTGRES_PASSWORD,
    POSTGRES_DBNAME,
    POSTGRES_TABLE,
    REQUIRED_COLUMNS,
)

PG_CONN_INFO = {
    "host": POSTGRES_HOST,
    "port": POSTGRES_PORT,
    "user": POSTGRES_USER,
    "password": POSTGRES_PASSWORD,
    "dbname": POSTGRES_DBNAME,
}


def fetch_from_clickhouse():
    client = get_client(
        host=CLICKHOUSE_HOST,
        port=CLICKHOUSE_PORT,
        database=CLICKHOUSE_DB,
        password=CLICKHOUSE_PASSWORD,
        user=CLICKHOUSE_USER,
    )
    query = f"SELECT {', '.join(REQUIRED_COLUMNS)} FROM {CLICKHOUSE_TABLE}"
    return client.query_df(query)


def ensure_postgres_table(cursor):
    cursor.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {POSTGRES_TABLE} (
            FlightDate DATE,
            DayOfWeek SMALLINT,
            Year SMALLINT,
            Flights SMALLINT,
            DepDelayMinutes REAL,
            Reporting_Airline TEXT,
            Dest TEXT
        )
    """
    )


def insert_to_postgres(df, conn):
    print("🔁 Migrating to PostgreSQL with COPY...")

    # Convert DataFrame to CSV format in memory
    output = io.StringIO()
    df.to_csv(output, sep="\t", header=False, index=False, na_rep="\\N")
    output.seek(0)

    with conn.cursor() as cursor:
        cursor.execute(f"DROP TABLE IF EXISTS {POSTGRES_TABLE}")
        ensure_postgres_table(cursor)
        cursor.copy_expert(
            f"""
            COPY {POSTGRES_TABLE} FROM STDIN WITH (
                FORMAT CSV,
                DELIMITER E'\t',
                NULL '\\N'
            );
        """,
            output,
        )
        conn.commit()
        print(f"✅ Data migrated to PostgreSQL table '{POSTGRES_TABLE}' using COPY")


def main():
    print("📥 Fetching data from ClickHouse...")
    df = fetch_from_clickhouse()
    print(f"✅ Retrieved {len(df)} rows.")

    print("🔁 Migrating to PostgreSQL...")
    with psycopg2.connect(**PG_CONN_INFO) as conn:
        insert_to_postgres(df, conn)
    print("✅ Migration complete.")


if __name__ == "__main__":
    main()
