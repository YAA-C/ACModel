import pandas as pd


class FightGenerator:
    def __init__(self) -> None:
        pass


    def fights(df: pd.DataFrame):
        indexes: list = [-1]
        indexes.extend(df[df.isnull().all(axis=1)].index.to_list())
        
        for i in range(1, len(indexes)):
            prevRowIndex: int = int(indexes[i - 1] + 1)
            curRowIndex: int = int(indexes[i])
            curDf: pd.DataFrame = df.iloc[prevRowIndex: curRowIndex, :].copy()
            curDf.reset_index(inplace = True)
            yield curDf