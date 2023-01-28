"""
This is a boilerplate pipeline 'serve_model'
generated using Kedro 0.18.3
"""


import os
from pathlib import Path
from pickle import load
from sklearn.tree import DecisionTreeRegressor
from pandas import DataFrame


def get_latest_model_path(index: int) -> str: 
    try:      
        models_storage_dir =  os.path.join(
            str(Path(__file__).resolve().parents[4]), "data", "06_models", "regressor.pickle"
            )
        all_model_dirs_paths = [x.name for x in os.scandir(models_storage_dir)]
        all_model_dirs_paths.sort(key=lambda x: x, reverse=True)
        latest_model_dir_path = all_model_dirs_paths[index]
        latest_model_path = os.path.join(
            models_storage_dir, latest_model_dir_path, "regressor.pickle"
            )
        return latest_model_path
    except Exception as e:
        print(latest_model_path)
    

def read_model(model_path: str) -> DecisionTreeRegressor:
    with open(model_path, 'rb') as o:
        model = load(o)
    return model


def predict(model: DecisionTreeRegressor, data_piece: DataFrame):
    return model.predict(data_piece)[0]

