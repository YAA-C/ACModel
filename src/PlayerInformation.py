import pandas as pd
import numpy as np

class PlayerInformation:
    def __init__(self) -> None:
        self.players: dict = {}

    
    def loadPlayers(self, filePath: str):
        df: pd.DataFrame = pd.read_csv(filePath)
        
        notNullDf: pd.DataFrame = df[df["playerId"].notnull()].copy()
        notNullDf["playerId"] = notNullDf["playerId"].astype(np.int64)
        notNullDf["targetId"] = notNullDf["targetId"].astype(np.int64)

        attackerPlayerId: list = notNullDf["playerId"].unique().tolist()
        attackerPlayerId = sorted(attackerPlayerId)

        for playerSteamId in attackerPlayerId:
            tmp: pd.DataFrame = df.loc[df["playerId"] == playerSteamId]
            self.addPlayer(playerSteamId, tmp.iloc[0, 2])
        
        defenderPlayerId = notNullDf["targetId"].unique().tolist()

        for playerSteamId in defenderPlayerId:
            tmp: pd.DataFrame = df.loc[df["targetId"] == playerSteamId]
            self.addPlayer(playerSteamId, tmp.iloc[0, 22])
        
        self.allPlayerId = attackerPlayerId + defenderPlayerId
        
    
    def addPlayer(self, playerSteamId: int, playerName: str) -> None:
        self.players[playerSteamId] = {
            "name": playerName,
            "cheatingCount": 0
        }
    
    
    def increasePlayerCheatingCount(self, playerSteamId: int) -> None:
        self.players[playerSteamId]["cheatingCount"] += 1


    def getPlayerName(self, playerSteamId: int) -> str:
        assert (playerSteamId in self.players), "No data available for player"
        
        return self.players[playerSteamId]["name"]

    
    def getAllPlayerData(self) -> list[dict]:
        return [
            self.getPlayerData(playerSteamId) for playerSteamId in self.players.keys()
        ]


    def getPlayerData(self, playerSteamId: int) -> dict:
        assert (playerSteamId in self.players), "No data available for player"

        return {
            "steamid": playerSteamId,
            "playerName": self.players[playerSteamId]["name"],
            "isCheating": (self.players[playerSteamId]["cheatingCount"] > 2)
        }