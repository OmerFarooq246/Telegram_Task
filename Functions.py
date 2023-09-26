import telebot
from typing import Final
from pymongo import collection
from database import client
from configparser import ConfigParser
from bson.objectid import ObjectId

config = ConfigParser()
config.read("./bot_info.ini")
bot_username: str = config.get("BOT_Info", "username")


def start_command(message: telebot.types.Message, bot: telebot.TeleBot):
    text1 = f'Hello {message.from_user.first_name}, I am a Test bot.'
    text2 = "\nType /help to list all my commands."
    if message.chat.type == "supergroup":
        bot.send_message(message.chat.id, text1 + text2)
    elif message.chat.type == "private":
        bot.send_message(message.from_user.id, text1 + text2)


def help_command(message: telebot.types.Message, bot: telebot.TeleBot):
    text = "Here is the list of my commands:\n"
    commands = """
/start: To start the Bot
/help: To list all the bot commands
/register: To register a group
/list_members: To list all the users of a group
    """
    if message.chat.type == "supergroup":
        bot.send_message(message.chat.id, text+commands)
    elif message.chat.type == "private":
        bot.send_message(message.from_user.id, text+commands)


def list_members(message: telebot.types.Message, bot: telebot.TeleBot):
    if message.chat.type == "private":
        bot.reply_to(message, "Use this command in a group")
    else:
        db = client.Telegram_Test_Database
        members = list(get_documents(db.Members, message.chat.id, "group_id"))
        if len(list(members)) != 0:
            text = "Members in " + message.chat.title + ": \n"
            for i in members:
                text = text + "\n" + i["fname"] + " " + i["lname"]
            bot.send_message(message.chat.id, text)
        else:
            bot.reply_to(message, "No members found, I can only display those members that were added/joined after I was added")


def register_group(message: telebot.types.Message, bot: telebot.TeleBot):
    db = client.Telegram_Test_Database
    if message.chat.type == "private":
        bot.reply_to(message, "This command can only be used for groups")
        return
    else:
        group = get_document_single(db.Groups, message.chat.id, "_id")
        if group != None:
            bot.reply_to(message, "Group is already registered")
            return
        else:
            try:
                db.Groups.insert_one({
                    "_id": message.chat.id,
                    "name": message.chat.title,
                    "owner": message.from_user.id,
                    "owner_username": message.from_user.username
                })
                bot.reply_to(message, "Your group has been registered")
            except Exception as e:
                bot.reply_to(message, "Failed to register group, try using the command again, if error persists, reach out to the bot organizers")
                print(f"Group insert error - {e}")


# def new_or_left_members_filter(message: telebot.types.Message):
#     return message.new_chat_members != None or message.left_chat_member != None

# def greet_new_or_left_members(message: telebot.types.Message, bot: telebot.TeleBot):
#     if message.new_chat_members != None:
#         for i in range(len(message.new_chat_members)):
#             text = f"Greetings {message.new_chat_members[i].first_name}, welcome to {message.chat.title}"
#             bot.send_message(message.chat.id, text)
#             print(text)

#     if message.left_chat_member != None:
#         text = f"Goodbye {message.left_chat_member.first_name}"
#         bot.send_message(message.chat.id, text)


# _______________ Database Functions _______________

def get_document_single(collection: collection.Collection, id: ObjectId, attribute: str):
    try:
        doc = collection.find_one({attribute: id})
        return doc
    except Exception as e:
        print(f"Document find error - {e}")

def get_documents(collection: collection.Collection, id: ObjectId, attribute: str):
    try:
        doc = collection.find({attribute: id})
        return doc
    except Exception as e:
        print(f"Document find error - {e}")


def insert_member_filter(message: telebot.types.Message):
    return message.new_chat_members != None

def insert_members(message: telebot.types.Message):
    db = client.Telegram_Test_Database
    members = []
    names = []
    for i in message.new_chat_members:
        members.append({
            "_id": i.id,
            "fname": i.first_name,
            "lname": i.last_name,
            "is_bot": i.is_bot,
            "group_id": message.chat.id
        })
        names.append(i.full_name)
    try:
        db.Members.insert_many(members)
        print(f"{names} addded to group {message.chat.title}")
    except Exception as e:
        print(f"Members insert error - {e}")


def delete_member_filter(message: telebot.types.Message):
    return message.left_chat_member != None

def delete_member(message: telebot.types.Message):
    db = client.Telegram_Test_Database
    try:
        db.Members.delete_one({"_id": message.left_chat_member.id})
        print(f"{message.left_chat_member.full_name} successfully deleted")
    except Exception as e:
        print(f"Member delete error - {e}")
