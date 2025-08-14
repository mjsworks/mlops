## we are running a regression problem here
import os
import sys

import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.linear_model import ElasticNet

from urllib.parse import urlparse

import mlflow
from mlflow.models import infer_signature
import mlflow.sklearn

import logging

# initialize the logging
logging.basicConfig(level=logging.WARN)
logger = logging.getLogger(__name__)

# get a evaluation function
def eval_metrics(actual, prediction):
    rmse = np.sqrt(mean_squared_error(actual, prediction))
    mae = mean_absolute_error(actual, prediction)
    r2 = r2_score(actual, prediction)
    return rmse, mae, r2

if __name__ == "__main__":
    ### putting the steps
    # reading the dataset - wine quality
    csv_url = "https://raw.githubusercontent.com/mlflow/mlflow/master/tests/datasets/winequality-red.csv"
    try:
        data = pd.read_csv(csv_url,sep=";")
    except Exception as e:
        print(f"Something came up: {e}")
    finally:
        print("data reading complete")
    # Get the dependent and independent bit
    X, y = data.drop(columns=["quality"]), data.quality
    # split the dataset
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        random_state=42,
        test_size=0.2,
        stratify=y
    )
    # init mlflow for the remote server
    remote_server_uri = "http://ec2-13-211-45-210.ap-southeast-2.compute.amazonaws.com:5000"
    mlflow.set_tracking_uri(remote_server_uri)
    mlflow.set_experiment("WINE_Q_AWS_MLFLOW")

    # set the val
    alpha=0.5
    l1_ratio=0.5
    random_state=42

    # train the model
    lr = ElasticNet(
        alpha=alpha,
        l1_ratio=l1_ratio,
        random_state=random_state
    )
    model = lr.fit(X_train, y_train)

    predictions = model.predict(X_test)
    # infer signature after the model is trained
    signature = infer_signature(X_train, predictions)
    # call the evaluate function
    (rmse,mae,r2) = eval_metrics(y_test, predictions)
    # track the experiment-log
    with mlflow.start_run():
        mlflow.log_params({
        "alpha": alpha,
        "l1_ratio": l1_ratio,
        "random_state": random_state
        })

        mlflow.log_metrics({
            "rmse": rmse,
            "mae": mae,
            "r2_score": r2
        })

        mlflow.sklearn.log_model(
            model,
            name = "wine_q_AWS_MLFLOW",
            signature=signature,
            registered_model_name="ElasticNet WineQ"
        )