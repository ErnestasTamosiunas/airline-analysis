# Airline Analysis

This project performs large-scale airline data analysis using ClickHouse and PostgreSQL. It involves:

* Retrieving raw flight data
* Loading it into ClickHouse for high-performance analytics
* Migrating the data to PostgreSQL
* Validating consistency of analytical queries across both databases

---

## 🚀 Project Structure

```bash
.
├── clickhouse-data/         # ClickHouse persistent volume
├── data/                    # Raw CSVs and intermediate files
├── docker-compose.yml       # Services for ClickHouse and Adminer
├── Makefile                 # Task automation
├── poetry.lock              # Dependency lockfile
├── pyproject.toml           # Project dependencies
├── requirements.txt         # Optional dependencies list
├── results/                 # Output of analysis/queries
├── scripts/                 # Data processing and migration scripts
│   ├── analyze_columns.py
│   ├── constants.py
│   ├── extract_csvs.py
│   ├── load_clickhouse.py
│   ├── migrate_clickhouse_to_postgres.py
│   ├── migrate_to_postgres.py
│   ├── query_databases.py
│   └── retrieve_data.py
├── typescript/              # Placeholder (if using a frontend)
├── venv/                    # Local virtual environment (if created)
└── README.md
```

---

## ⚙️ Setup Instructions

### 1. Install Dependencies

```bash
make init
```

### 2. Start Services

```bash
make up
```

This will spin up ClickHouse and Adminer. PostgreSQL is assumed to run locally.

### 3. Retrieve and Prepare Data

```bash
make retrieve
make extract-csvs
make analyze-columns
```

### 4. Load into ClickHouse

```bash
make load-clickhouse
```

### 5. Migrate to PostgreSQL

```bash
make migrate-clickhouse-to-postgres
```

---

## 🔍 Validate Results

```bash
make query-databases
```

This script runs a series of analytical SQL queries against both ClickHouse and PostgreSQL. Matching outputs confirm successful migration.

### ✅ Sample Output (Matching ClickHouse & PostgreSQL)

```text
1. Day with the most flights
FlightDate  TotalFlights
2000-12-18         16218

...

7. Top 10 most popular destinations
Dest  TotalFlights
ORD       3179174
DFW       2781284
...
```

---

## 🧹 .gitignore Suggestions

To prevent clutter and accidental versioning:

```gitignore
/venv
/data
/results
/clickhouse-data
/pg-data
__pycache__/
*.pyc
```

---

## 📝 Notes

* You can view the databases using Adminer at [http://localhost:8080](http://localhost:8080)
* Make sure PostgreSQL is running locally and accessible at `localhost:5432`
* If ClickHouse fails to respond, check that port `8123` is free and the container is up

---

## 🧪 Make Targets

```makefile
init                 # Install dependencies via Poetry
up                   # Start docker containers (ClickHouse, Adminer)
down                 # Stop containers
docker-compose down -v # (if needed) remove all volumes
retrieve             # Fetch raw data
extract-csvs         # Parse raw data
analyze-columns      # Inspect column metadata
load-clickhouse      # Insert data into ClickHouse
migrate-clickhouse-to-postgres # Migrate ClickHouse data to PostgreSQL
query-databases      # Run validation queries
reset                # Full teardown
```

---

## 📬 Contact

For questions or improvements, open an issue or ping the maintainer.
