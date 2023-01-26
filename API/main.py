from typing import Union
from fastapi import FastAPI
from sklearn.tree import DecisionTreeRegressor
import dvc.api 
from pickle import load, dump
import numpy as np
import pandas as pd
from pydantic import BaseModel

app = FastAPI()

class Input(BaseModel):
    symboling : int
    wheelbase : float
    carlength : float
    carwidth : float
    carheight : float
    curbweight : int
    enginesize : int
    boreratio : float
    stroke : float 
    compressionratio : float
    horsepower : int
    peakrpm : int
    citympg : int
    highwaympg : int

    def to_dataframe(self):
        #print([self.dict()])
        #print()
        return pd.DataFrame([self.dict()])


regr = load(open("regressor.pickle", 'rb'))


@app.put("/")
async def read_root(inp: Input):
    inp_df = inp.to_dataframe() 
    return {"predicted_price" : regr.predict(inp_df)[0]}
