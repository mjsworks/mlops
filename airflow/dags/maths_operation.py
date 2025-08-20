"""
We will define a DAG where the tasks will be:

1. start with an initial number
2. add 5 to it
3. multiply the result by 2
4. subtract 3 from the final result
5. print the final result
"""

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

## define the functions for each task

## task 1
def start_number(**context):
    # xcom is used to pass data between tasks
    # here we are starting with a number 10 and pushing it to xcom
    # so that it can be used in the next task
    # context is a dictionary that contains information about the task instance
    # we use context["task_instance"] to access the task instance
    # and then we use xcom_push to push data to xcom
    # key is the name of the data we are pushing and value is the data itself
    # in this case, we are pushing the number 10 with the key "current_val"
    
    context["task_instance"].xcom_push(
        key = "current_val",
        value = 10  # starting with number 10
    )
    print("Starting with number 10")

## task 2
def add_five(**context):
    current_val = context["task_instance"].xcom_pull(
        key = "current_val",
        task_ids = "add five"
    )
    new_value = current_val + 5 # adding 5 to the current value
    context["task_instance"].xcom_push(
        key = "current_val",
        value = new_value
    )

## task 3
def multiply_by_two(**context):
    current_val = context["task_instance"].xcom_pull(
        key= "current_val",
        task_ids="mul two"
    )
    new_value = current_val * 2  # multiplying the current value by 2
    context["task_instance"].xcom_push(
        key="current_val",
        value=new_value
    )

## task 4
def subtract_three(**context):
    current_val = context["task_instance"].xcom_pull(
        key = "current_val",
        task_ids = "sub three"
    )
    new_value = current_val -3

    context["task_instance"].xcom_push(
        key = "current_val",
        value = new_value
    )

## task 5
def print_final_result(**context):
    final_result = context["task_instance"].xcom_pull(
        key = "current_val",
        task_ids = "print result"
    )
    print(f"The final result is: {final_result}")

## Define the default arguments for the DAG
default_args = {
    'owner': 'protik',
    'start_date': datetime(2024,1,1),
    'schedule_interval': '@weekly'
}

## define the DAG
with DAG(
    dag_id = 'maths_operation',
    default_args = default_args,
    catchup=False # to stop backfilling of the DAG
) as dag:
    
    # define the tasks
    start = PythonOperator(
        task_id='start_number',
        python_callable = start_number
    )

    add_five_task = PythonOperator(
        task_id='add_five',
        python_callable=add_five
    )

    multiply_by_two_task = PythonOperator(
        task_id='mul_two',
        python_callable=multiply_by_two
    )

    subtract_three_task = PythonOperator(
        task_id = 'sub_three',
        python_callable=subtract_three
    )

    print_final_result_task = PythonOperator(
        task_id='print_result',
        python_callable=print_final_result
    )

    ## set task dependencies
    start >> add_five_task >> multiply_by_two_task >> subtract_three_task >> print_final_result_task