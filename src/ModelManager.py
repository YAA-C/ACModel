from .ACModel import ACModel
from .DTModel import DTModel
from .LSTMModel import LSTMModel


modelConfigurations = {
    "lstm": "./src/models/dataset4/stackedLSTMwithDenseNet/stackedLSTMwithDenseNet_LSTMModel_3.keras",
    "decision_tree": "./src/models/DTModel/DTmodel.pkl"
}


class ModelManager:
    def __init__(self) -> None:
        self.modelSet: bool = False
        self.model: ACModel


    def setModel(self, modelChoice) -> None:
        assert modelChoice in modelConfigurations.keys(), "Wrong model choice..."

        if modelChoice == "lstm":
            self.model = LSTMModel(modelConfigurations["lstm"])
        elif modelChoice == "decision_tree":
            self.model = DTModel(modelConfigurations["decision_tree"])


    def getModel(self) -> ACModel:
        return self.model


modelManager: ModelManager = ModelManager()