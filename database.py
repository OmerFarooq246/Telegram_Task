import dotenv
import telebot
from pymongo import MongoClient
import urllib.parse

mongo_pass = dotenv.dotenv_values(".env")["MONGO_PASS"]
connetion_string = f"mongodb+srv://ofarooq:{mongo_pass}@telegramtestcluster.p6lge3o.mongodb.net/?retryWrites=true&w=majority"

try:
    client = MongoClient(connetion_string)
except Exception as e:
    print(e)