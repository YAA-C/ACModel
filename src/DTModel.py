import pickle
import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.compose import ColumnTransformer


class DTModel:
    def __init__(self) -> None:
        with open("./src/models/DTmodel.data", "rb") as f:
            modelData: bytes = f.read()

        self.model: DecisionTreeClassifier = pickle.loads(modelData)
        
        with open('./src/models/column_transformer.pkl', 'rb') as f:
            columnTransformerData: bytes = f.read()
        
        self.columnTransformer: ColumnTransformer = pickle.loads(columnTransformerData)


    def predict(self, data: pd.DataFrame) -> bool:
        data = data.drop(['currentTick','playerId','playerName','X','Y','Z','targetId','targetName','targetX','targetY','targetZ'], axis=1)
        data = data[(data['isHurt'] != False) & (~data['isHurt'].isna())]

        data.fillna(0, inplace=True)
        data = self.columnTransformer.transform(data)

        yPred = self.model.predict(data)
        counts = np.bincount(yPred)

        return bool(np.argmax(counts))


dtModel: DTModel = DTModel()