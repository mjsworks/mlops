from airflow import DAG
from airflow.operators.python import PythonOperator # enables us to run python functions as tasks
from datetime import datetime

## Define our task 1
def preprocess_data():
    print("Preprocessing data...")

## Define our task 2
def train_model():
    print("Training model...")

## Define our task 3
def evaluate_model():
    print("Evaluating model...")

## Define the default arguments for the DAG
default_args = {
    "owner": "airflow",
    "start_date": datetime(2024, 1, 1),
    "schedule_interval": "@weekly",
    "catchup": False
}

## Define the DAG
with DAG(
    dag_id='ml_pipeline',
    default_args=default_args
) as dag:

    # Define tasks
    preprocess = PythonOperator(
        task_id='preprocess_data',
        python_callable=preprocess_data # the function to run
    )

    train = PythonOperator(
        task_id='train_task',
        python_callable=train_model
    )

    evaluate = PythonOperator(
        task_id='evaluate_task',
        python_callable=evaluate_model
    )

    # set task dependencies
    preprocess >> train >> evaluate