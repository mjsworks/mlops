## Definition
Airflow is an open-source platform used to programatically author, schedule and monitor workflows. This is also used in ETL.

## Key components of Apache Airflow
1. DAG(Directed Acyclic Graph) - collection of tasks that we want to schedule and run.
    a. Directed: Tasks must have a specific sequence.
    b. acyclic: it cannot be cyclic, meaning, it should not refer to itself. No task should depend on itself.
2. Tasks: individual unit of works in a DAG.
    a. python function
    b. querying database
    c. sending HTTP request
3. Dependencies: Tasks in DAG have dependencies, meaning one task might need to finish before another task can start. Airflow offers the processes to function like this.

## Why Airflow for MLOps
1. Orchestrating ML & ETL Pipelines
2. Tasks Automations
3. Monitoring and Alerts