import numpy as np
import pandas as pd
from kedro.pipeline import node, pipeline
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error
from typing import Dict,Tuple

import logging

from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split

import wandb





def split_data(data: pd.DataFrame, parameters : Dict) -> Tuple:
    """Splits data into features and targets training and test sets.

    Args:
        data: Data containing features and target.
        parameters: Parameters defined in parameters/data_science.yml.
    Returns:
        Split data.
    """
    X = data[parameters["features"]]
    y = data["price"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=parameters["test_size"], random_state=parameters["random_state"]
    )
    return X_train, X_test, y_train, y_test

def train_model(X_train: pd.DataFrame, y_train: pd.Series, parameters : Dict) -> DecisionTreeRegressor:
    """Trains the linear regression model.

    Args:
        X_train: Training data of independent features.
        y_train: Training data for price.
        parmateres : parameters for the model
    Returns:
        Trained model.
    """

    wandb.init(project="random-team-project")
    wandb.config = {
        "max_depth": parameters['max_depth'],
        "min_samples_split": parameters['min_samples_split'],
        "min_samples_leaf": parameters['min_samples_leaf'],
    }
    print(parameters)
    regressor = DecisionTreeRegressor(max_depth= parameters['max_depth'], 
       min_samples_split = parameters['min_samples_split'] , min_samples_leaf  = parameters['min_samples_leaf'] )
    regressor.fit(X_train, y_train)
    return regressor


def evaluate_model(
    regressor: DecisionTreeRegressor, X_test: pd.DataFrame, y_test: pd.Series
):
    """Calculates and logs the coefficient of determination.

    Args:
        regressor: Trained model.
        X_test: Testing data of independent features.
        y_test: Testing data for price.
    """
    y_pred = regressor.predict(X_test)
    score = r2_score(y_test, y_pred)
    logger = logging.getLogger(__name__)
    logger.info("Model has a coefficient R^2 of %.3f on test data.", score)
    wandb.log({"R^2": score})

def log_regressor_visualisations( regressor: DecisionTreeRegressor, X_train: pd.DataFrame, y_train: pd.Series,
                                        X_test: pd.DataFrame, y_test: pd.Series, ):
        wandb.sklearn.plot_regressor(regressor, X_train, X_test, y_train, y_test,  model_name="Random_team")