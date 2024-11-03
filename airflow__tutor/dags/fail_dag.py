from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import requests

def failing_request():
    response = requests.get('http://nonexistent.example.com')
    response.raise_for_status()  # This will raise an HTTPError for bad responses

with DAG(
    dag_id='failing_request_dag',
    schedule_interval='@once',
    start_date=datetime(2023, 11, 1),
    catchup=False,
) as dag:
    fail_task = PythonOperator(
        task_id='make_failing_request',
        python_callable=failing_request,
    )