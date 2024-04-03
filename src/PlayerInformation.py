import pandas as pd

class PlayerInformation:
    def __init__(self) -> None:
        self.players: dict = {}

    
    def loadPlayers(self, df: pd.DataFrame):
        self.allPlayers = df["playerName"].unique().tolist()
        self.allPlayers = sorted(self.allPlayers)

        for playerSteamId in self.allPlayers:
            tmp: pd.DataFrame = df.loc[df['steamid'] == playerSteamId]
            self.addplayer(playerSteamId, tmp.iloc[0, 2])
        
    
    def addplayer(self, playerSteamId: int, playerName: str) -> None:
        self.players[playerSteamId] = {
            "name": playerName,
            "cheatingCount": 0
        }
    
    
    def increasePlayerCheatingCount(self, playerSteamId: int) -> None:
        self.players[playerSteamId]["cheatingCount"] += 1


    def getPlayerName(self, playerSteamId: int) -> str:
        assert (playerSteamId in self.players), "No data available for player"
        
        return self.players[playerSteamId]["name"]

    
    def getPlayerData(self, playerSteamId: int) -> dict:
        assert (playerSteamId in self.players), "No data available for player"

        return {
            "steamid": playerSteamId,
            "playerName": self.players[playerSteamId]["name"],
            "isCheating": (self.players[playerSteamId]["cheatingCnt"] > 0)
        }