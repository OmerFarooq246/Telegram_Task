import telebot
from typing import Final
from configparser import ConfigParser
from Functions import *
print()

# mongo_pass = dotenv.dotenv_values(".env")["MONGO_PASS"]
# connetion_string = f"mongodb+srv://ofarooq:{mongo_pass}@telegramtestcluster.p6lge3o.mongodb.net/?retryWrites=true&w=majority"


config = ConfigParser()
config.read("./bot_info.ini")
BOT_TOKEN: Final = config.get("BOT_Info", "token")

Test_Bot = telebot.TeleBot(BOT_TOKEN)

Test_Bot.register_message_handler(start_command, pass_bot=True, commands=["start"])
Test_Bot.register_message_handler(help_command, pass_bot=True, commands=["help"])
Test_Bot.register_message_handler(list_members, pass_bot=True, commands=["list_members"])
Test_Bot.register_message_handler(register_group, pass_bot=True, commands=["register"])
Test_Bot.register_message_handler(insert_members, pass_bot=False, func=insert_member_filter)
Test_Bot.register_message_handler(delete_member, pass_bot=False, func=delete_member_filter)
# Test_Bot.register_message_handler(greet_new_or_left_members, pass_bot=True, func=new_or_left_members_filter)

print()
Test_Bot.infinity_polling()