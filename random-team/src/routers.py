from fastapi import APIRouter
from .models import Input
from .services import run_pipeline

predictions_router = APIRouter()

@predictions_router.put("/")
def read_root(inp: Input):
    try:
        inp_df = inp.to_dataframe()
        print(inp_df)
        ret = run_pipeline(inp_df)
        return ret
    except Exception as e:
        print(e)
        return None
