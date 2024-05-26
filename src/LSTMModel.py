import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.python.keras.models import load_model
from tensorflow.python.keras.models import Sequential
from typing import List
from .ACModel import ACModel
from .utils.Logger import log


class LSTMModel(ACModel):
    def __init__(self, modelPath) -> None:
        super(LSTMModel, self).__init__()
        self.model: Sequential = load_model(modelPath)
        self.threshold = 0.5


    def predict(self, fightDf: pd.DataFrame) -> bool:
        X = self.formatData(fightDf)
        ypred: np.ndarray = self.model.predict(X)
        ypred = ypred.reshape(ypred.shape[0])
        ypred = (ypred > self.threshold).astype(bool)
        return self.calculateVerdict(ypred)

    
    def formatData(self, df: pd.DataFrame) -> np.ndarray:
        df: pd.DataFrame = self.dropUselessColumns(df)
        
        df = self.normalize(df)
            
        max_rows = 32
        num_samples = len(df)
        num_columns = df.shape[1]

        Xarray = np.zeros((num_samples, max_rows, num_columns))

        Xarray[0, :df.shape[0], :] = df.values

        return Xarray