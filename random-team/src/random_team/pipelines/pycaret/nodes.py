import logging
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pycaret.regression import *

from typing import Dict,Tuple

def split_unseen_data(dataset: pd.DataFrame) -> Tuple:
    #reserves 10% of data separate from the test and train set
    data = dataset.sample(frac=0.9)
    data_unseen = dataset.drop(data.index)
    data.reset_index(drop=True, inplace=True)
    data_unseen.reset_index(drop=True, inplace=True)
    return data, data_unseen
    
def find_best_model(data: pd.DataFrame, parameters:Dict) -> Tuple:
    regress = setup(data=data, target="price", session_id=parameters["random_state"], use_gpu=True, train_size=1-parameters["test_size"])
    best_model = compare_models(fold=10, sort="MAE")
    return best_model

def create_and_tune_model(best_model):
    model = create_model(best_model, fold=10)
    tuned_model = tune_model(model, optimize="MAE", n_iter=100, fold=10)
    return tuned_model
    
def evaluate_and_finalize_model(tuned_model, data_unseen: pd.DataFrame):
    evaluate_model(tuned_model)
    final_model = finalize_model(tuned_model)
    predict_model(final_model)
    unseen_predictions = predict_model(final_model, data=data_unseen)
    unseen_predictions.head()