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
CLICKHOUSE_USER = "<Enter your CLICKHOUSE user name>"
CLICKHOUSE_PASSWORD = "<Enter your CLICKHOUSE user password>"
CLICKHOUSE_TABLE = "flights"
CLICKHOUSE_DB = "default"

# Postgres parameters:
POSTGRES_HOST = "localhost"
POSTGRES_PORT = 5432
POSTGRES_USER = "<Enter your POSTGRES user name>"
POSTGRES_PASSWORD = "<Enter your POSTGRES user password>"
POSTGRES_DBNAME = "flights"
POSTGRES_TABLE = "flights_migrated"
