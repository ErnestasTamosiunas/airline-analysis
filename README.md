## 📁 Project Structure

```
.
├── clickhouse-data/                # ClickHouse data volume
├── data/                           # Raw datasets (unzipped .csv)
├── docker-compose.yml             # Container orchestration
├── Makefile                        # Run project tasks
├── poetry.lock / pyproject.toml    # Python environment dependencies
├── requirements.txt                # Alternative dependency listing
├── results/                        # Output directory (if needed)
├── scripts/                        # All logic scripts
│   ├── analyze_columns.py
│   ├── constants.py
│   ├── extract_csvs.py
│   ├── load_clickhouse.py
│   ├── migrate_clickhouse_to_postgres.py
│   ├── migrate_to_postgres.py
│   ├── query_databases.py
│   └── retrieve_data.py
├── typescript/                     # (Optional UI or frontend stub)
└── venv/                           # Local Python virtual environment (ignored)
```

---

## 🚀 Setup Instructions

### 1. Install dependencies

```bash
make init
```

### 2. Start services (ClickHouse, Adminer)

```bash
make up
```

### 3. Retrieve flight dataset

```bash
make retrieve
```

### 4. Extract CSVs from raw ZIPs

```bash
make extract-csvs
```

### 5. Load data into ClickHouse

```bash
make load-clickhouse
```

### 6. Migrate from ClickHouse to PostgreSQL

```bash
make migrate-clickhouse-to-postgres
```

### 7. Run analytical queries on both databases

```bash
make query-databases
```

### 8. Tear down services (optional)

```bash
make down
```

---

## 🧪 Query Comparison Results

### 1. Day with the most flights

```
FlightDate  TotalFlights
2000-12-18         16218
```

### 2. Day of the week with fewest flights in 1995

```
DayOfWeek  TotalFlights
6          695286
```

### 3. Number of flights delayed >10min by day of the week

```
DayOfWeek  DelayCount
5          1898026
4          1744321
7          1530053
3          1504265
1          1419299
2          1349905
6          1293669
```

### 4. Number of delays by carrier in 1997

```
Reporting_Airline  DelayedFlights
DL                 481009
UA                 412867
US                 317819
WN                 290235
AA                 246490
NW                 212544
CO                 169227
TW                  82727
HP                  64982
AS                  49442
```

### 5. Percentage of delays by carrier in 1997

```
Reporting_Airline  DelayPercentage
UA                 55.504291
DL                 52.178662
US                 44.218234
CO                 41.955478
NW                 39.568688
AA                 37.124560
WN                 36.514483
AS                 33.463283
HP                 31.498177
TW                 30.188259
```

### 6. Percentage delayed > 10 min. by year

```
Year  DelayPercentage
1990        16.645130
1991        14.721628
1992        14.675431
1993        15.424985
1994        16.568032
1995        19.393442
1996        22.182806
1997        19.165135
1998        19.356379
1999        20.087415
2000        23.171672
```

### 7. Top 10 most popular destinations

```
Dest  TotalFlights
ORD       3179174
DFW       2781284
ATL       2610247
LAX       1926312
PHX       1715468
STL       1712218
DTW       1558308
DEN       1540166
SFO       1422341
MSP       1418363
```

---

## ✅ Validation

All queries yield identical results in ClickHouse and PostgreSQL, validating successful data migration and schema compatibility.

---

## 🛑 .gitignore Recommendations

Ensure the following files/folders are ignored in `.gitignore`:

```
venv/
__pycache__/
clickhouse-data/
data/
pg-data/
results/
*.pyc
*.pyo
.DS_Store
```