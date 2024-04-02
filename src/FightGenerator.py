import pandas as pd


class FightGenerator:
    def __init__(self) -> None:
        pass


    def fights(self, df: pd.DataFrame):
        indexes: list = [-1]
        indexes.extend(df[df.isnull().all(axis=1)].index.to_list())
        
        for i in range(1, len(indexes)):
            prevRowIndex: int = int(indexes[i - 1] + 1)
            curRowIndex: int = int(indexes[i])
            curDf: pd.DataFrame = df.iloc[prevRowIndex: curRowIndex, :].copy()
            curDf.reset_index(inplace = True)
            yield curDf


    def getFightData(self, df: pd.DataFrame) -> list[list]:
        x = df["X"]
        y = df["Y"]
        targetX = df["targetX"]
        targetY = df["targetY"]
        isHurt = ~df["targetId"].isna()
        data = [x for x in zip(x, y, targetX, targetY, isHurt)]
        return data