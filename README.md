# Urban Crime ETL Pipeline

End-to-end ETL pipeline that ingests public crime data from the Chicago Open Data API, transforms it, and loads it into a PostgreSQL data warehouse using Apache Airflow.

---

## Stack

* Python (Pandas, Requests)
* PostgreSQL
* Apache Airflow
* Docker

---

## Structure

```
etl/        # Extract, transform, load logic
dags/       # Airflow pipeline
sql/        # Database schema
tests/      # Unit tests
```

---

## Run

```bash
cp .env.example .env
docker-compose up
```

Airflow UI: http://localhost:8080
DAG: `crime_pipeline`

---

## Notes

* Handles API pagination and retries
* Cleans and validates data before loading
* Uses upsert to avoid duplicates
* Logs pipeline runs and bad records


