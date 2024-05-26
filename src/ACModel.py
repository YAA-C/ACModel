import pandas as pd
import numpy as np
import pickle
from typing import List, Tuple
from sklearn.preprocessing import LabelEncoder


transformerConfigurations = {
    "weaponUsedTransformer": "./src/models/dataset4/data/weaponUsedTransformer.pkl",
    "weaponCategoryTransformer": "./src/models/dataset4/data/weaponCategoryTransformer.pkl",
}


class ACModel:
    def __init__(self) -> None:
        with open(transformerConfigurations["weaponUsedTransformer"], "rb") as f:
            self.weaponUsedTransformer: LabelEncoder = pickle.loads(f.read())
        with open(transformerConfigurations["weaponCategoryTransformer"], "rb") as f:
            self.weaponCategoryTransformer: LabelEncoder = pickle.loads(f.read())


    def predict(self, *args, **kwargs) -> bool:
        raise NotImplementedError("This method should be overrided")


    def calculateVerdict(self, verdicts: np.ndarray) -> bool:
        counts = np.bincount(verdicts)
        return bool(np.argmax(counts))


    def dropUselessColumns(self, df: pd.DataFrame) -> pd.DataFrame:
        return df.drop(['index', 'playerId','playerName','X','Y','Z', 'yaw', 'pitch', 'targetId','targetName','targetX','targetY','targetZ'], axis=1)


    def normalize(self, df: pd.DataFrame) -> pd.DataFrame:        
        df = df.infer_objects(copy=False).fillna(-1)
        
        df['isInAir'] = df['isInAir'].astype(int).values
        df['isFiring'] = df['isFiring'].astype(int).values
        df['isHurt'] = df['isHurt'].astype(int).values
        df['isScoping'] = df['isScoping'].astype(int).values
        df['shotTargetThroughSmoke'] = df['shotTargetThroughSmoke'].astype(int).values
        
        df["deltaX"] = df["deltaX"].astype(float).values / 64
        df["deltaY"] = df["deltaY"].astype(float).values / 64
        df["deltaZ"] = df["deltaZ"].astype(float).values / 64
        df["deltaYaw"] = df["deltaYaw"].astype(float).values / 64
        df["deltaPitch"] = df["deltaPitch"].astype(float).values / 64
        df["deltaAimArc"] = df["deltaAimArc"].astype(float).values / 64
        df["utilityDmgDone"] = df["utilityDmgDone"].astype(float).values / 64
        df["targetDeltaX"] = df["targetDeltaX"].astype(float).values / 64
        df["targetDeltaY"] = df["targetDeltaY"].astype(float).values / 64
        df["targetDeltaZ"] = df["targetDeltaZ"].astype(float).values / 64
        df["dmgDone"] = df["dmgDone"].astype(float).values / 64
        df["distToTarget"] = df["distToTarget"].astype(float).values / 128
        df["targetReturnedDmg"] = df["targetReturnedDmg"].astype(float).values / 64
        
        df['weaponUsed'] = df['weaponUsed'].replace(-1, "none")
        df['weaponCategory'] = df['weaponCategory'].replace(-1, "none")
            
        df['weaponUsed'] = self.weaponUsedTransformer.transform(df['weaponUsed'])
        df['weaponCategory'] = self.weaponCategoryTransformer.transform(df['weaponCategory'])

        return df