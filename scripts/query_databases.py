import pandas as pd
from sqlalchemy import create_engine
from clickhouse_connect import get_client
from scripts.constants import (
    CLICKHOUSE_HOST,
    CLICKHOUSE_USER,
    CLICKHOUSE_PASSWORD,
    CLICKHOUSE_DB,
    CLICKHOUSE_TABLE,
    POSTGRES_USER,
    POSTGRES_PASSWORD,
    POSTGRES_HOST,
    POSTGRES_PORT,
    POSTGRES_DBNAME,
    POSTGRES_TABLE,
)

# ClickHouse client
clickhouse_client = get_client(
    host=CLICKHOUSE_HOST,
    username=CLICKHOUSE_USER,
    password=CLICKHOUSE_PASSWORD,
    database=CLICKHOUSE_DB,
)

# PostgreSQL engine
postgres_engine = create_engine(
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DBNAME}"
)

# Queries
CLICKHOUSE_QUERIES = {
    "1. Day with the most flights": f"""
        SELECT FlightDate, SUM(Flights) AS TotalFlights
        FROM {CLICKHOUSE_TABLE}
        GROUP BY FlightDate
        ORDER BY TotalFlights DESC
        LIMIT 1
    """,
    "2. Day of the week with fewest flights in 1995": f"""
        SELECT DayOfWeek, SUM(Flights) AS TotalFlights
        FROM {CLICKHOUSE_TABLE}
        WHERE Year = 1995
        GROUP BY DayOfWeek
        ORDER BY TotalFlights ASC
        LIMIT 1
    """,
    "3. Number of flights delayed >10min by day of the week": f"""
        SELECT DayOfWeek, COUNT() AS DelayCount
        FROM {CLICKHOUSE_TABLE}
        WHERE DepDelayMinutes > 10
        GROUP BY DayOfWeek
        ORDER BY DelayCount DESC
    """,
    "4. Number of delays by carrier in 1997": f"""
        SELECT Reporting_Airline, COUNT() AS DelayedFlights
        FROM {CLICKHOUSE_TABLE}
        WHERE Year = 1997 AND DepDelayMinutes > 0
        GROUP BY Reporting_Airline
        ORDER BY DelayedFlights DESC
    """,
    "5. Percentage of delays by carrier in 1997": f"""
        SELECT
            Reporting_Airline,
            COUNTIf(DepDelayMinutes > 0) * 100.0 / COUNT() AS DelayPercentage
        FROM {CLICKHOUSE_TABLE}
        WHERE Year = 1997
        GROUP BY Reporting_Airline
        ORDER BY DelayPercentage DESC
    """,
    "6. Percentage delayed > 10 min. by year": f"""
        SELECT
            Year,
            COUNTIf(DepDelayMinutes > 10) * 100.0 / COUNT() AS DelayPercentage
        FROM {CLICKHOUSE_TABLE}
        GROUP BY Year
        ORDER BY Year ASC
    """,
    "7. Top 10 most popular destinations": f"""
        SELECT Dest, SUM(Flights) AS TotalFlights
        FROM {CLICKHOUSE_TABLE}
        GROUP BY Dest
        ORDER BY TotalFlights DESC
        LIMIT 10
    """,
}

POSTGRES_QUERIES = {
    key: query
    for key, query in {
        "1. Day with the most flights": f"""
            SELECT FlightDate, SUM(Flights) AS TotalFlights
            FROM {POSTGRES_TABLE}
            GROUP BY FlightDate
            ORDER BY TotalFlights DESC
            LIMIT 1
        """,
        "2. Day of the week with fewest flights in 1995": f"""
            SELECT DayOfWeek, SUM(Flights) AS TotalFlights
            FROM {POSTGRES_TABLE}
            WHERE Year = 1995
            GROUP BY DayOfWeek
            ORDER BY TotalFlights ASC
            LIMIT 1
        """,
        "3. Number of flights delayed >10min by day of the week": f"""
            SELECT DayOfWeek, COUNT(*) AS DelayCount
            FROM {POSTGRES_TABLE}
            WHERE DepDelayMinutes > 10
            GROUP BY DayOfWeek
            ORDER BY DelayCount DESC
        """,
        "4. Number of delays by carrier in 1997": f"""
            SELECT Reporting_Airline, COUNT(*) AS DelayedFlights
            FROM {POSTGRES_TABLE}
            WHERE Year = 1997 AND DepDelayMinutes > 0
            GROUP BY Reporting_Airline
            ORDER BY DelayedFlights DESC
        """,
        "5. Percentage of delays by carrier in 1997": f"""
            SELECT
                Reporting_Airline,
                COUNT(*) FILTER (WHERE DepDelayMinutes > 0) * 100.0 / COUNT(*) AS DelayPercentage
            FROM {POSTGRES_TABLE}
            WHERE Year = 1997
            GROUP BY Reporting_Airline
            ORDER BY DelayPercentage DESC
        """,
        "6. Percentage delayed > 10 min. by year": f"""
            SELECT
                Year,
                COUNT(*) FILTER (WHERE DepDelayMinutes > 10) * 100.0 / COUNT(*) AS DelayPercentage
            FROM {POSTGRES_TABLE}
            GROUP BY Year
            ORDER BY Year ASC
        """,
        "7. Top 10 most popular destinations": f"""
            SELECT Dest, SUM(Flights) AS TotalFlights
            FROM {POSTGRES_TABLE}
            GROUP BY Dest
            ORDER BY TotalFlights DESC
            LIMIT 10
        """,
    }.items()
}


def run_queries(title, queries, executor):
    print(f"\n📊 Running queries against {title}...\n")
    for name, sql in queries.items():
        print(f"\n{name}")
        try:
            result = executor(sql)
            print(result.to_string(index=False))
        except Exception as e:
            print(f"❌ {title} query failed: {e}")
        print("-" * 60)


def main():
    run_queries("ClickHouse", CLICKHOUSE_QUERIES, clickhouse_client.query_df)
    run_queries(
        "PostgreSQL", POSTGRES_QUERIES, lambda q: pd.read_sql(q, postgres_engine)
    )


if __name__ == "__main__":
    main()
