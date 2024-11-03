from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import requests

def successful_request():
    response = requests.get('http://example.com')
    response.raise_for_status()  # This should not raise an error for a successful request
    print(response.text)  # Optionally print or log the response

with DAG(
    dag_id='successful_request_dag',
    schedule_interval='@once',
    start_date=datetime(2023, 11, 1),
    catchup=False,
) as dag:
    success_task = PythonOperator(
        task_id='make_successful_request',
        python_callable=successful_request,
    )