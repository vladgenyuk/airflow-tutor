from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests
import time

# Function to request example.com and print the status code
def request_example():
    for _ in range(2):  # Loop twice for a 30-second interval
        response = requests.get('https://example.com')
        print(f'Status Code: {response.status_code}')
        time.sleep(30)  # Wait for 30 seconds before the next request

# Define default arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 11, 1),
    'retries': 1,
    'retry_delay': timedelta(seconds=5),
}

# Define the DAG
dag = DAG(
    'request_example_dag',
    default_args=default_args,
    description='Request example.com every 30 seconds',
    schedule_interval='*/1 * * * *',  # Runs every minute
    catchup=False,
)

# Define the task
request_task = PythonOperator(
    task_id='request_example_task',
    python_callable=request_example,
    dag=dag,
)

# Set up the task dependencies
request_task