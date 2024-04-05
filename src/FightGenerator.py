import pandas as pd
import numpy as np


class FightGenerator:
    def __init__(self, filePath: str) -> None:
        self.df: pd.DataFrame = pd.read_csv(filePath)
    

    def getFights(self):
        indexes: list = [-1]
        indexes.extend(self.df[self.df.isnull().all(axis=1)].index.to_list())
        
        for i in range(1, len(indexes)):
            prevRowIndex: int = int(indexes[i - 1] + 1)
            curRowIndex: int = int(indexes[i])
            curDf: pd.DataFrame = self.df.iloc[prevRowIndex: curRowIndex, :].copy()
            curDf.reset_index(inplace = True)            
            curDf["playerId"] = curDf["playerId"].astype(np.int64)
            curDf["targetId"] = curDf["targetId"].astype(np.int64)

            yield curDf


    def getFightPlayerId(self, df: pd.DataFrame) -> int:
        return int(df["playerId"].iloc[0])


    def getFightTargetId(self, df: pd.DataFrame) -> int:
        return int(df["targetId"].iloc[0])
    

    def getFightData(self, df: pd.DataFrame) -> list[list]:
        x = df["X"]
        y = df["Y"]
        targetX = df["targetX"]
        targetY = df["targetY"]
        isHurt = df["isHurt"]
        data = [x for x in zip(x, y, targetX, targetY, isHurt)]
        return data