from uuid import uuid4
from sys import maxsize
from hashlib import sha256
from random import randint
from datetime import datetime
import json

from database.mongo import MongoDBSingleton


class BlockchainSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Blockchain(metaclass=BlockchainSingleton):

    
    def __init__(self, difficulty: int = 4):
        self.__difficulty = difficulty
        mongo = MongoDBSingleton()
        self.__chain = mongo.get_collection(collection_name="blocks")
        self.__pow_prefix = "0"

        self.__create_genesis_block()


    def __create_genesis_block(self):
        payload = {
            "sequency": 0,
            "timestamp": datetime.now().timestamp(),
            "data": "Genesis Block",
            "previous_hash": "",
        }

        header = {
            "nonce": 0,
            "hash": self.__create_hash(json.dumps(payload)),
        }

        block = {
            "id": str(uuid4()),
            "header": header,
            "payload": payload,
        }

        self.__chain.insert_one(block)

        return block


    def create_block(self, data: dict[str, any] ) -> dict[str, any]:

        payload = {
            "sequency": self.__get_last_block()["payload"]["sequency"] + 1,
            "data": data,
            "previous_hash": self.__get_hash_last_block(),
            "timestamp": datetime.now().timestamp(),
        }

        print(f"Block #{payload}")

        return payload
    

    def block_miner(self, payload_block: dict[str, any]) -> dict[str, any]:
        
        nonce = randint(0, maxsize)
        start_at = datetime.now()

        while (True):
            data_to_hash = json.dumps(payload_block) + str(nonce)

            pow_hash = self.__create_hash(data_to_hash)
            
            if (self.__validate_hash_prefix(pow_hash)):
                stop_at = datetime.now()

                mining_time = stop_at - start_at

                sequency = payload_block["sequency"]

                print(f"Mined block #{sequency} in {mining_time.seconds} seconds")
                print(f"#{pow_hash} | nonce={nonce} attempts")

                header = {
                    "nonce": nonce,
                    "hash": pow_hash,
                }

                return {                
                    "id": str(uuid4()),
                    "header": header,
                    "payload": payload_block,
                }
            
            nonce = randint(0, maxsize)

    
    def __verify_block(self, data: dict[str, any]) -> bool:

        previous_hash = data.get("payload").get("previous_hash")
        last_hash = self.__get_hash_last_block()

        if (previous_hash != last_hash):
            print(f"Error: {previous_hash[0:12]} differs from {last_hash[0:12]}")
            return False
        
        hash_test = self.__create_hash(json.dumps(data.get("payload")) + str(data.get("header").get("nonce")))

        if not (self.__validate_hash_prefix(hash_test)):
            print(f"Error: {data} is invalid, nonce is invalid")
            return False
        
        return True

    def send_block(self, data: dict[str, any]) -> list[dict[str, any]]:
        if (self.__verify_block(data)):
            self.__chain.insert_one(data)
            print(f"Block #{data} added")
        else:
            print(f"Block #{data} error")

        return self.get_chain()
    
    def get_chain(self,) -> list[dict[str, any]]:
        return list(self.__chain.find())
    
    def __get_last_block(self) -> dict[str, any]:
        return self.__chain.find_one(sort=[("payload.sequency", -1)])
    
    def __get_hash_last_block(self) -> str:
        return self.__get_last_block()["header"]["hash"]
        
    def __create_hash(self, data) -> str:
        hasher = sha256()
        hasher.update(data.encode('utf-8'))
        return hasher.hexdigest().upper()
    
    def __validate_hash_prefix(self, pow_hash: str) -> bool:
        return pow_hash.startswith(self.__pow_prefix * self.__difficulty)
    
    
    