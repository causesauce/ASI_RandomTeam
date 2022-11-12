import numpy as np
import pandas as pd
from kedro.pipeline import node, pipeline
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


#kedro wrapper nodes
read_data_node = node(func=read_data, inputs="file path", outputs="data")
dataset_split_node = node(func=dataset_split, inputs="data frame", outputs="test and train data")
train_model_node = node(func=train_model, inputs="model and data", outputs="predictions")
score_model_node = node(func=score_model, inputs="model and predictions", outputs="model score")

#assemble nodes into pipeline
modules_pipeline = pipeline([read_data_node, dataset_split_node, train_model_node, score_model_node])