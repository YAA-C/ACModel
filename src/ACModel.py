import pandas as pd
from .DTModel import dtModel


class ACModel:
    def __init__(self) -> None:
        pass


    def predict(self, fightDf: pd.DataFrame) -> bool:
        return dtModel.predict(fightDf)


model: ACModel = ACModel()