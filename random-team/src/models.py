from pydantic import BaseModel
import pandas as pd

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
        return pd.DataFrame([self.dict()])