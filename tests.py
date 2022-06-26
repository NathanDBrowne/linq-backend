import sys
from pprint import pprint

import pandas as pd
import requests
from loguru import logger


def get_user(uname):
    return requests.get("http://127.0.0.1:5000/login", params={"username": uname}).json()


def get_chats(user_detail):
    return pd.DataFrame(requests.get("http://127.0.0.1:5000/events", params=user_detail).json())


@logger.catch
def main():

    username = sys.argv[1]

    if "account" in sys.argv:
        account = get_user(username)
        pprint(account)

    if "chats" in sys.argv:
        account = get_user(username)
        chats = get_chats(account)
        pprint(chats)


if __name__ == "__main__":
    main()
