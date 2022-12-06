"""
This is a boilerplate pipeline 'pycaret'
generated using Kedro 0.18.3
"""

from kedro.pipeline import Pipeline, node, pipeline
from.nodes import split_unseen_data, find_best_model, create_and_tune_model, evaluate_and_finalize_model

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
    [
        node(
            func=split_unseen_data,
            inputs=["car_price"],
            outputs=["data", "data_unseen"],
            name="split_unseen_data_node"
        ),
        node(
            func=find_best_model,
            inputs=["data", "params:model_options"],
            outputs="best_model",
            name="find_best_model_node",
        ),
        node(
            func=create_and_tune_model,
            inputs="best_model",
            outputs="tuned_model",
            name="create_and_tune_model_node",
        ),
        node(
            evaluate_and_finalize_model,
            inputs=["tuned_model", "data_unseen"],
            outputs=None,
            name="evaluate_and_finalize_model_node",
        )
    ]
)
