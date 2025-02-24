from datetime import datetime, timedelta
import random
import psycopg2
from airflow import DAG
from airflow.operators.python import PythonOperator

def extract():
    """Simulate data extraction."""
    data = [{'id': i, 'value': random.randint(1, 100)} for i in range(10)]
    print(f"Extracted data: {data}")
    return data

def transform(**kwargs):
    """Transform extracted data."""
    ti = kwargs['ti']
    data = ti.xcom_pull(task_ids='extract_task')
    for item in data:
        item['value'] *= 2  # Simple transformation
    print(f"Transformed data: {data}")
    return data

def load(**kwargs):
    """Load transformed data into PostgreSQL."""
    ti = kwargs['ti']
    data = ti.xcom_pull(task_ids='transform_task')
    connection = psycopg2.connect(
        dbname='postgres', user='postgres', password='postgres', host='db', port=5432
    )
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS etl_data (
            id SERIAL PRIMARY KEY,
            data_id INT,
            value INT
        )
    """
    )
    for item in data:
        cursor.execute("INSERT INTO etl_data (data_id, value) VALUES (%s, %s)", (item['id'], item['value']))
    connection.commit()
    cursor.close()
    connection.close()
    print("Data loaded into PostgreSQL")

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'simple_etl',
    default_args=default_args,
    description='A simple ETL data pipeline using Airflow',
    schedule_interval=timedelta(days=1),
)

extract_task = PythonOperator(
    task_id='extract_task',
    python_callable=extract,
    dag=dag,
)

transform_task = PythonOperator(
    task_id='transform_task',
    python_callable=transform,
    provide_context=True,
    dag=dag,
)

load_task = PythonOperator(
    task_id='load_task',
    python_callable=load,
    provide_context=True,
    dag=dag,
)

extract_task >> transform_task >> load_task
