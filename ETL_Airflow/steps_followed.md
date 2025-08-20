## Here I am putting the step by step guideline to complete this project

1. we need to install Astro `https://www.astronomer.io/docs/astro/cli/get-started-cli`
2. We need docker desktop as well
3. we need the folder structure. so we run `astro dev init`
4. we need to update the README.md file(optional) for defining the description of the project.
5. we can also remove dags/exampledag.py
6. since we are running this in a docker container, we will be calling multiple images. to do that we need a `docker-compose.yml`

## Into the project
1. create the dag in the dags folder - `etl.py` <br>
    1.1 We have defined postgres in the `etl.py`. so the postgres should run somewhere.
        it can be our local system, cloud or docker.
        We will be using docker to run our postgres serve. 
        here, our astroner is running in docker. postgres will run as a seperate container. But, they need to interact with each other. so, to enable that, we need `docker-compose.yml` to configure this.<br>
2. after we ran the DAG properly, we go to `admin> connection`. then we add connection we put the connection name as `nasa_apod_api`. we took it from the HttpOperator bit. we then set the connection type as `http`. we provide the host, which is `http://api.nasa.gov/`. we also put api_key in the extra section as a dict.<br>
3. we also need to add the postgres connection. we put the connection name as `my_postgres_conn` from the `create_table()'s postgres hook`. we put the connection type to be `postgres`. for host -> we go to the docker desktop>containers>postgres>click> we get the name. right now, the name is `etl-airflow_ca385f-postgres-1`. we put this as the host name. we have already defined the login and password bit in the `docker-compose.yml`. we also have our port in there. 
4. after we have done that we can connect our postgres to the Dbeaver and we can query our data!


### currently the pipeline runs in my local machine. but we can host it to AWS
we can essentially change the host in the connection to the aws and that should work.

### steps to do that
1. go to astronomer.io
2. sign in
3. terminal> `astro login`
4. terminal> `astro deploy`

we will now go to the AWS console. because astronomer only manages airflow. it does not provide any database like postgres.
1. search RDS > aurora & rds> db instances > create database > standard create > select the engine version > template(free tier) > we will define the login and password as my `docker-compose.yml` > enable public access
2. once the database is creates> get into that> VPC security groups > security group id > edit inbound rule > add rule > type (postgres), cidr block (0.0.0.0/0) means anybody
3. back to RDS > db instances> database> endpoint - copy

back to astronomer.io<br>
1. go to deployment > open airflow ui
2. host name should be the one we copied from endpoint.
3. we save the postgres connection and nasa api connection like before


We can also see this from the Dbeaver with just the connection to AWS EC2's RDS.


if we ever need to delete the persistant data from the volume
```
docker volume ls
docker volume inspect postgres_data
docker system df -v
docker volume rm postgres_data        # DANGER: deletes the data

```