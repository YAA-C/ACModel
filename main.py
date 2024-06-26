import argparse
import json
import traceback
import pika
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic
from src.utils.LoadFile import LoadFile
from src.FightGenerator import FightGenerator
from src.ACModel import ACModel
from src.ModelManager import modelManager, modelConfigurations
from src.PlayerInformation import PlayerInformation
from src.utils.Logger import log, logp, compileLogs


class CharterWorker:
    def __init__(self) -> None:
        self.queueName: str = "to_model"
        self.connection: pika.BlockingConnection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost", port=5672))
        self.channel: BlockingChannel = self.connection.channel()


    def setupRabbit(self) -> None:
        self.channel.exchange_declare(exchange= "work_exchange", exchange_type= "fanout")
        self.channel.queue_declare(queue= "to_charter")
        self.channel.queue_declare(queue= "to_model")
        self.channel.queue_bind(queue= "to_charter", exchange= "work_exchange")
        self.channel.queue_bind(queue= "to_model", exchange= "work_exchange")

        self.channel.exchange_declare(exchange= "upload_exchange", exchange_type= "direct")
        self.channel.queue_declare(queue= "to_uploader")
        self.channel.queue_bind(queue= "to_uploader", exchange= "upload_exchange")


    def rejectMessage(self, channel: BlockingChannel, method: Basic.Deliver) -> None:
        if(method.redelivered):
            log("Discarding message from queue...")
            channel.basic_reject(delivery_tag= method.delivery_tag, requeue= False)
        else:
            log("Requeuing message...")
            channel.basic_reject(delivery_tag= method.delivery_tag, requeue= True)


    def makeUploadJSON(self, match_id: int, allPlayersData: list, allFightsData: list) -> str:
        data = [
            {
                "metadata": {
                    "type": "FIGHT",
                    "match_id": match_id
                },
                "data": allFightsData
            },
            {
                "metadata": {
                    "type": "MODEL_RESULT",
                    "match_id": match_id
                },
                "data": allPlayersData
            }
        ]

        return json.dumps(data)


    def handleData(self, channel: BlockingChannel, method: Basic.Deliver, body: bytes) -> None:
        log("Job Received.")
        try:
            workObject: dict = json.loads(str(body, encoding= "utf-8"))
            loadFile: LoadFile = LoadFile(workObject["url"])
            matchId: str = str(workObject["match_id"])
            filePath: str = loadFile.startLoading()
            # matchId: str = "660daf2f15e62d9d25cbdde8"
            # filePath: str = "./download/testing-large-unclasssified.csv"
            log("Loaded file:", filePath)

            log("Fetching player information...")
            playerInformation: PlayerInformation = PlayerInformation()
            playerInformation.loadPlayers(filePath)
            log("Successfully fetched player information.")
            
            allFightsData: list = []

            model: ACModel = modelManager.getModel()
            
            log("Starting Fight Analysis...")

            fightGenerator: FightGenerator = FightGenerator(filePath)

            for fightDf in fightGenerator.getFights():
                # get classification from model
                modelLabel: bool = model.predict(fightDf)
                
                # not processing non cheating players
                if modelLabel == False:
                    continue

                # update player information
                playerSteamId: int = fightGenerator.getFightPlayerId(fightDf)
                targetSteamId: int = fightGenerator.getFightTargetId(fightDf)

                playerInformation.increasePlayerCheatingCount(playerSteamId)
                
                # get fightChart data
                fightData: list[list] = fightGenerator.getFightData(fightDf)

                fightInformation = {
                    "match_id": matchId,
                    "playerSteamId": playerSteamId,
                    "targetSteamId": targetSteamId,
                    "isCheating": modelLabel,
                    "playerName": playerInformation.getPlayerName(playerSteamId),
                    "targetName": playerInformation.getPlayerName(targetSteamId),
                    "data": fightData
                }

                allFightsData.append(fightInformation)
            
            allPlayersData: list[dict] = playerInformation.getAllPlayerData()
            
            uploadJSON: str = self.makeUploadJSON(matchId, allPlayersData, allFightsData)
            
            log("Finished Fight Analysis.")
            self.channel.basic_publish(
                exchange= "upload_exchange", 
                routing_key="to_uploader", 
                body= uploadJSON
            )
            log("Sent Data to RabbitMQ.")
        except Exception:
            log(traceback.format_exc())
            self.rejectMessage(channel, method)
        else:
            channel.basic_ack(delivery_tag= method.delivery_tag)
        finally:
            log("Job Completed.")


    def work(self) -> None:
        self.setupRabbit()
        self.channel.basic_consume(
            queue= "to_model", 
            on_message_callback= lambda channel, method, _, body: self.handleData(channel, method, body)
        )
        log("Listening on:", self.queueName)
        self.channel.start_consuming()


def main() -> None:
    parser = argparse.ArgumentParser(description='Example script with required parameter.')

    parser.add_argument(
        "model",
        type=str,
        choices= modelConfigurations.keys(), 
        help= f"Model to use: {', '.join(modelConfigurations.keys())}"
    )

    args = parser.parse_args()
    modelManager.setModel(args.model)

    try:
        log("Starting Worker...")
        charterWorker: CharterWorker = CharterWorker()
    except Exception:
        log("Could not connect to RabbitMQ...")
        log(traceback.format_exc())
    else:
        charterWorker.work()
    finally:
        log("Exitting Worker...")
        compileLogs(["MW"])


if __name__ == "__main__":
    main()