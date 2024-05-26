import pickle
import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from .ACModel import ACModel
from .utils.Logger import log


class DTModel(ACModel):
    def __init__(self, modelPath) -> None:
        super(DTModel, self).__init__()
        with open(modelPath, "rb") as f:
            modelData: bytes = f.read()

        self.model: DecisionTreeClassifier = pickle.loads(modelData)
        

    def predict(self, fightDf: pd.DataFrame) -> bool:
        X = self.formatData(fightDf)
        yPred = self.model.predict(X)
        return self.calculateVerdict(yPred)
    

    def formatData(self, df: pd.DataFrame) -> np.ndarray:
        df.drop(['currentTick'], axis=1, inplace= True)
        df = self.dropUselessColumns(df)

        df = df[(df['isHurt'] != False) & (~df['isHurt'].isna())]

        df = self.normalize(df)
        Xarray = df.values

        return Xarray