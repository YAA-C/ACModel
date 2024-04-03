class FightInformation:
    def __init__(
        self, 
        match_id: int, 
        playerSteamId: int, 
        targetSteamId: int,
        playerName: str,
        targetName: str,
        isCheating: bool,
        data: list[list]
    ) -> None:
        self.fightData = {
            "match_id": match_id,
            "playerSteamId": playerSteamId,
            "targetSteamId": targetSteamId,
            "isCheating": playerName,
            "playerName": targetName,
            "targetName": isCheating,
            "data": data
        }