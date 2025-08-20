"""
Apache Airflow introduced the TaskFlow API which allows us to create tasks
using Pyhton Decorators like @tasks. This is a cleaner and more intuitive way
of writing tasks without needing to manually use operators like PythonOperator.
The example below demonstrates how to use the TaskFlow API's @task decorator
to create a simple DAG.
"""

from airflow import DAG
from airflow.decorators import task
from datetime import datetime

## define the default arguments for the DAG
default_args = {
    'owner': 'protik',
    'start_date': datetime(2023, 10, 1),
    'schedule_interval': '@once',
    'catchup': False,
}

## define the DAG
with DAG(
    dag_id = 'taskflow_api_example',
    default_args=default_args
) as dag:
    
    ## task 1: start witht the initial number
    @task
    def start_number():
        initial_number = 10
        print(f"Starting with number: {initial_number}")
        return initial_number
    
    @task
    def add_five(number):
        new_value = number + 5
        print(f"Adding 5 + {number} = {new_value}")
        return new_value
    
    @task
    def multiply_by_two(number):
        new_value = number * 2
        print(f"Multiplying by 2: {number} * 2 = {new_value}")
        return new_value
    
    @task
    def subtract_three(number):
        new_value = number - 3
        print(f"Subtracting 3: {number} - 3 = {new_value}")
        return new_value
    
    @task
    def print_final_value(number):
        print(f"The final value is: {number}")

    ## define the task dependencies
    start_value = start_number()
    added_value = add_five(start_value)
    multiplied_value = multiply_by_two(added_value)
    subtract_three_value = subtract_three(multiplied_value)
    print_final_value(subtract_three_value)