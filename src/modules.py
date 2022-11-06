import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error


selected_cols = ["symboling", "wheelbase", "carlength", 
                 "carwidth", "carheight", "curbweight", 
                 "enginesize", "boreratio", "stroke", 
                 "compressionratio", "horsepower", "peakrpm", 
                 "citympg", "highwaympg", "price"]
predict = "price"


def read_data(path: str) -> pd.DataFrame:
    data = pd.read_csv(path)
    return data


def dataset_split(data: pd.DataFrame):
    data = data[selected_cols]
    x = np.array(data.drop([predict], 1))
    y = np.array(data[predict])
    xtrain, xtest, ytrain, ytest = train_test_split(x, y, test_size=0.2)
    return xtrain, xtest, ytrain, ytest


def train_model(model, xtrain, xtest, ytrain):
    model.fit(xtrain, ytrain)
    predictions = model.predict(xtest)
    return predictions


def score_model(model, xtest, predictions):
    return model.score(xtest, predictions)


if __name__ == "__main__":
    data = read_data("../data/CarPrice.csv")
    xtrain, xtest, ytrain, ytest = dataset_split(data)
    model = DecisionTreeRegressor()
    predictions = train_model(model, xtrain, xtest, ytrain)
    score = score_model(model, xtest, predictions)
    print(score)
