# Download parameters:
BASE_URL = "https://transtats.bts.gov/PREZIP/On_Time_Reporting_Carrier_On_Time_Performance_1987_present_{year}_{month}.zip"

# Directories
DATA_DIR = "data"
CSV_EXTRACTED_DIR: str = "data/extracted"

START_YEAR = 1990
END_YEAR = 2000

MAX_RETRIES = 3
RETRY_DELAY = 5  # seconds

# Target columns:
REQUIRED_COLUMNS = [
    "FlightDate",
    "DayOfWeek",
    "Year",
    "Flights",
    "DepDelayMinutes",
    "Reporting_Airline",
    "Dest",
]

# Clickhouse parameters:
CLICKHOUSE_HOST = "localhost"
CLICKHOUSE_PORT = 8123
CLICKHOUSE_USER = "dev_user"
CLICKHOUSE_PASSWORD = "dev_pass"
CLICKHOUSE_TABLE = "flights"
CLICKHOUSE_DB = "default"

# Postgres parameters:
POSTGRES_HOST = "localhost"
POSTGRES_PORT = 5432
POSTGRES_USER = "ernestastamo"
POSTGRES_PASSWORD = "password"
POSTGRES_DBNAME = "flights"
POSTGRES_TABLE = "flights_migrated"
