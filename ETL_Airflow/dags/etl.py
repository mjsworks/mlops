from airflow import DAG
from airflow.providers.http.operators.http import HttpOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook #https://registry.astronomer.io/modules/?types=hooks%2CHooks&page=2
from airflow.decorators import task
from datetime import datetime

## define the default arguments for the DAG
default_args = {'owner': 'Protik'}

## define the DAG
with DAG(
    dag_id='nasa_apod_etl',
    default_args=default_args,
    start_date=datetime(2024, 1, 1),
    schedule='@once', 
    catchup=False # dont want to run past dates
) as dag:
    ## step 1: create the table if that does not exist
    @task
    def create_table():
        ## initialize the Postgres hook
        pg_hook = PostgresHook(postgres_conn_id='my_postgres_conn')

        ## SQL query to create the table
        create_table_query = """
        CREATE TABLE IF NOT EXISTS public.apod_data(
            id SERIAL PRIMARY KEY,
            title VARCHAR(255),
            explanation TEXT,
            url TEXT,
            date DATE,
            media_type VARCHAR(50)
        );
        """

        ## execute the query
        pg_hook.run(create_table_query, autocommit=True)

    ## step 2: extract the NASA API DATA(APOD) [extract pipeline]
    extract_apod = HttpOperator(
        task_id='extract_apod',
        http_conn_id='nasa_apod_api',  ## connection ID defined in Airflow for NASA API
        endpoint='planetary/apod?api_key={{ conn.nasa_apod_api.extra_dejson.api_key }}',  ## API key via connection extras
        method='GET',
        response_filter=lambda response: response.json(),  # convert response to JSON
        log_response=True,
    )

    ## step 3: transform the data (Pick the information to save)
    @task
    def transform_apod_data(response):
        apod_data = {
            'title': response.get('title', ''),
            'explanation': response.get('explanation', ''),
            'url': response.get('url', ''),
            'date': response.get('date', ''),
            'media_type': response.get('media_type', '')
        }
        return apod_data

    ## step 4: load the data to Postgres [load pipeline]
    @task
    def load_data_to_postgres(apod_data):
        ## initialize the Postgres hook
        pg_hook = PostgresHook(postgres_conn_id='my_postgres_conn')

        ## define SQL insert query
        insert_query = """
        INSERT INTO public.apod_data (title, explanation, url, date, media_type)
        VALUES (%s, %s, %s, %s, %s);
        """

        ## execute the query
        pg_hook.run(
            insert_query,
            parameters=(
                apod_data['title'],
                apod_data['explanation'],
                apod_data['url'],
                apod_data['date'],
                apod_data['media_type']
            ),
            autocommit=True
        )

    ## step 5: define the task dependencies
    ## extraction
    create_table() >> extract_apod
    api_response = extract_apod.output          # get the output of the API call
    ## transform
    transformed = transform_apod_data(api_response)  # transform the data
    ## load
    load_data_to_postgres(transformed)          # load the data to Postgres
