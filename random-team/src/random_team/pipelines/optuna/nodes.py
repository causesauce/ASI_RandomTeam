import logging
from typing import Dict, Tuple, Callable

import optuna
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor


def split_data(data: pd.DataFrame, parameters: Dict) -> Tuple:
    X = data[parameters["features"]]
    y = data["price"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=parameters["test_size"], random_state=parameters["random_state"]
    )
    return X_train, X_test, y_train, y_test


def get_objective(X_train: pd.DataFrame, X_test: pd.DataFrame, y_train: pd.DataFrame):
    def dtree_objective(trial):
        max_depth = trial.suggest_int("max_depth", 2, 64)
        min_samples_leaf = trial.suggest_int("min_samples_leaf", 1, 32)

        classifier = DecisionTreeRegressor(max_depth=max_depth, min_samples_leaf=min_samples_leaf, random_state=1)
        classifier.fit(X_train, y_train)
        predictions = classifier.predict(X_test)
        score = classifier.score(X_test, predictions)

        return score

    return dtree_objective


def tune_hyperparams(objective: Callable):
    logger = logging.getLogger(__name__)

    logger.info("STARTING TUNING HYPERPARAMETERS")
    dtree_study = optuna.create_study(direction='maximize')
    dtree_study.optimize(objective, n_trials=30)
    logger.info("FINISHED TUNING HYPERPARAMETERS")
    best_params = dtree_study.best_params



    logger.info(f'best value: {dtree_study.best_value}')
    logger.info(best_params)

    return best_params['max_depth'], best_params['min_samples_leaf']