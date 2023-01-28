"""
This is a boilerplate pipeline 'serve_model'
generated using Kedro 0.18.3
"""

from kedro.pipeline import Pipeline, node, pipeline
from .nodes import get_latest_model_path, read_model, predict

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=get_latest_model_path,
            inputs="index",
            outputs="model_path",
            name="get_model_path"
        ),
        node(
            func=read_model,
            inputs="model_path",
            outputs="model",
            name="read_model"
        ),
        node(
            func=predict,
            inputs=["model", "data_piece"],
            outputs="prediction",
            name="predict"
        )
    ])
