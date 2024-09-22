from dotenv import load_dotenv
import os
import sys

load_dotenv()
work_dir = os.getenv('WORK_DIR')
sys.path.append(work_dir)

print(os.getenv('PYTHONASYNCIODEBUG'))

from datetime import timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.models.baseoperator import chain
from datetime import datetime
from dags.etl import *



default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 12, 1),  # Update the start date to today or an appropriate date
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=10)
}

with DAG(
    'Workshop-2',
    default_args=default_args,
    description='workflow spotify stadistics',
    schedule_interval='@daily',  # Set the schedule interval as per your requirements
) as dag:

    read_db = PythonOperator(
        task_id='read_db',
        python_callable=extract_grammy,

    )

    transform_db = PythonOperator(
        task_id='transform_db',
        python_callable=transform_grammy,

        )

    read_csv = PythonOperator(
        task_id='read_csv',
        python_callable=read_spotify,


        )

    transform_csv = PythonOperator(
        task_id='transform_csv',
        python_callable=tranform_spotify,

        )

    merge = PythonOperator(
        task_id='merge',
        python_callable=merge_df,


        )

    load = PythonOperator(
        task_id='load',
        python_callable=load_merge,

        )

    Store = PythonOperator(
        task_id='Store',
        python_callable=store,

        )



    read_db >> transform_db >> merge >> load >> Store
    read_csv >> transform_csv >> merge
