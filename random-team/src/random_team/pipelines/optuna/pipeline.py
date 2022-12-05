from kedro.pipeline import Pipeline, node, pipeline
from .nodes import split_data, tune_hyperparams, get_objective


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=split_data,
                inputs=["car_price", "params:model_options"],
                outputs=["X_train", "X_test", "y_train", "y_test"],
                name="split_data_node",
            ),
            node(
                func=get_objective,
                inputs=["X_train", "X_test", "y_train"],
                outputs="dtree_objective",
                name="get_objective_node"
            ),
            node(
                func=tune_hyperparams,
                inputs="dtree_objective",
                outputs=None,
                name="tune_hyperparams_node"
            )
        ]
    )
