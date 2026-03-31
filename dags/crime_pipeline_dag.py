from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from etl.extract import fetch_crime_data
from etl.transform import transform_data
from etl.load import load_data
import pandas as pd

def extract_task(**c):
    c['ti'].xcom_push(key='raw', value=fetch_crime_data())

def transform_task(**c):
    df, bad = transform_data(c['ti'].xcom_pull(key='raw'))
    c['ti'].xcom_push(key='clean', value=df.to_dict())
    c['ti'].xcom_push(key='bad', value=bad)

def load_task(**c):
    load_data(pd.DataFrame(c['ti'].xcom_pull(key='clean')),
              c['ti'].xcom_pull(key='bad'))

with DAG("crime_pipeline", start_date=datetime(2024,1,1),
         schedule_interval="@daily", catchup=False,
         default_args={"retries":3,"retry_delay":timedelta(minutes=5)}) as dag:

    extract = PythonOperator(task_id="extract", python_callable=extract_task)
    transform = PythonOperator(task_id="transform", python_callable=transform_task)
    load = PythonOperator(task_id="load", python_callable=load_task)

    extract >> transform >> load
