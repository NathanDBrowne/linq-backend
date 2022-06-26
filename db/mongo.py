import os
import sys

import pymongo
from dotenv import load_dotenv
from loguru import logger

load_dotenv()


class DataBase(pymongo.database.Database):

    mongo_user = os.environ.get("MONGO_USER", None)
    mongo_pwd = os.environ.get("MONGO_PWD", None)

    if not (isinstance(mongo_pwd, str) and isinstance(mongo_user, str)):
        logger.warning("Missing Mongo auth. Please define MONGO_USER and MONGO_PWD in .env")

    def __init__(self, database_name) -> None:
        client = pymongo.MongoClient(
            "mongodb+srv://{}:{}@linq.aybjjlo.mongodb.net/?retryWrites=true&w=majority".format(
                self.mongo_user, self.mongo_pwd
            )
        )

        try:
            client.server_info()
            super().__init__(client, database_name)
            logger.success("Initialised connection to MongoDB database {}".format(database_name))

        except Exception as e:
            logger.error("INVALID MONGO CONNECTION: {}".format(e))
            sys.exit()

    def get_user_info(self, **kwargs):
        if ("tgID" not in kwargs) or ("tgUsername" not in kwargs):
            raise KeyError("The user query will return more than one user.")

        else:
            return self.users.find(kwargs)


@logger.catch
def main():
    db = DataBase("LINQ")


if __name__ == "__main__":
    main()
