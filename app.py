#!/usr/bin/env python3

import pandas as pd
from flask import Flask, jsonify, request
from loguru import logger

from db.mongo import DataBase as Mongo
from db.sql import SQLInterface

app = Flask(__name__)
app.config["DEBUG"] = True


@app.route("/login", methods=["GET"])
def get_user():
    query_params = request.args
    logger.info(query_params)

    mongo = Mongo("LINQ")
    sql = SQLInterface()

    user = pd.read_sql(
        "SELECT * FROM users where tgUsername = '{}';".format(query_params["username"]), sql.conn
    ).to_dict("records")[0]

    user_chats = [x for x in mongo.users.find({"userID": user["userID"]}, projection={"_id": 0})][
        0
    ]
    return jsonify({**user, **user_chats})


@app.route("/events", methods=["GET"])
def get_events():
    user_info = request.args.to_dict(flat=False)

    sql = SQLInterface()

    query = "SELECT * FROM events WHERE eventID IN {};".format(
        tuple(int(x) for x in (user_info["memberEvents"] + user_info["adminEvents"]))
    )

    return jsonify(pd.read_sql(query, sql.conn).to_dict("records"))


@logger.catch
def main():
    app.run()


if __name__ == "__main__":
    main()
