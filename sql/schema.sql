-- Create schemas
CREATE SCHEMA IF NOT EXISTS public;

CREATE TABLE IF NOT EXISTS dim_crime_type (
    crime_type_id SERIAL PRIMARY KEY,
    primary_type TEXT UNIQUE NOT NULL,
    fbi_code TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS dim_location (
    location_id SERIAL PRIMARY KEY,
    location_description TEXT,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    district INTEGER,
    ward INTEGER
);

CREATE TABLE IF NOT EXISTS dim_time (
    time_id SERIAL PRIMARY KEY,
    date TIMESTAMP NOT NULL,
    hour_of_day INTEGER,
    day_of_week TEXT,
    season TEXT
);

CREATE TABLE IF NOT EXISTS crime_incidents (
    id BIGINT PRIMARY KEY,
    crime_type_id INTEGER REFERENCES dim_crime_type(crime_type_id),
    location_id INTEGER REFERENCES dim_location(location_id),
    time_id INTEGER REFERENCES dim_time(time_id),
    arrest BOOLEAN,
    domestic BOOLEAN,
    is_violent BOOLEAN
);

CREATE TABLE IF NOT EXISTS bad_records (
    id SERIAL PRIMARY KEY,
    raw_data JSONB,
    error_reason TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS pipeline_runs (
    run_id SERIAL PRIMARY KEY,
    run_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    records_ingested INTEGER,
    records_failed INTEGER,
    status TEXT
);
