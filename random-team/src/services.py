from .random_team.pipelines.serve_model.pipeline import create_pipeline
from kedro.runner import SequentialRunner
from kedro.io import DataCatalog
import pandas as pd

def run_pipeline(df: pd.DataFrame):
    catalog = DataCatalog(feed_dict={"data_piece": df, "index":0})
    pipeline = create_pipeline()
    return SequentialRunner().run(pipeline=pipeline, catalog=catalog)
    