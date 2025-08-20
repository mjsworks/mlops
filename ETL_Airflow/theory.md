## What is ETL pipeline?

Extract > Transform > Load

### why do we need to run these 3 componenets as a form of a pipeline?

In a lifecycle of a data science project, the first step is requirement gathering. Here, the product owner and business analysts will speak and come up with the details. specifically, they follow a AGILE process. In an Agile process, all the stories are divided into sprints. So, a continuous integration and continuous development will take place.

Once the specifications are clear, this will go to the team of data scientists where they will also speak with the product owner. the task will be first to identify how they will be accessing the data. once they sort out the source of the data, it goes to the DATA ENGINEERING team.

the DE team will create a data pipeline.

The team will follow a ETL pipeline process. This ETL pipeline is a part of the entire data pipeline.

First the source is identified. if there are more than 1 source, the data engineer will first integrate all the sources together.
Then some transformation bit is done. Normally then transform into a JSON format to get all the data in one place.

then the task is to load the data in some place. it can be sql server/mongodb server/posgres etc.

The data scientists will then be dependent on this one source.

This pipeline is necessary to ease the process.

Best part is, we can run ETL using Airflow

## we will be using Airflow hooks
when we will be pushing our data to the postgres, these hooks will be useful then.