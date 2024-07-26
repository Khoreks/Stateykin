import requests
from telebot import TeleBot
from telebot.types import BotCommand, MenuButtonCommands, InlineKeyboardMarkup, InlineKeyboardButton, ChatPermissions

from tools import settings

bot = TeleBot(settings.BOT_TOKEN)

c_post = BotCommand(command='new_post', description='Создание контента')
c_help = BotCommand(command='help', description='Справочная информация')
c_sub_info = BotCommand(command='sub_info', description='Информация о текущей подписке')
c_sub_buy = BotCommand(command='sub_buy', description='Приобретение подписки')
bot.set_my_commands([c_post, c_help, c_sub_info, c_sub_buy])


@bot.message_handler(content_types=['text'])
def func(message):
    command = message.text.lower()
    bot.set_chat_menu_button(message.chat.id, MenuButtonCommands('commands'))

    if message.from_user.is_bot:
        bot.send_message(message.chat.id, settings.bot_detect_message, parse_mode='MarkdownV2')

    elif command == "/start":
        data = {
            "login": message.from_user.username,
            "chat_id": message.chat.id,
            "first_name": message.from_user.first_name,
            "last_name": message.from_user.last_name
        }
        response = requests.post(settings.BACKEND_URL + '/signup', json=data)
        if response.status_code == 201:
            print(200, response.text)
        elif response.status_code == 409:
            print(409, response.text)
        elif response.status_code == 500:
            print(500, response.text)

        bot.send_message(message.chat.id, settings.start_message, parse_mode='MarkdownV2')

    elif command == "/help":
        bot.send_message(message.chat.id, settings.help_message, parse_mode='MarkdownV2')
    elif command == "/sub_info":
        data = {
            "chat_id": message.chat.id,
        }
        response = requests.post(settings.BACKEND_URL + '/subscription/check', json=data).json()
        bot.send_message(message.chat.id, response.get("message", ""))  # , parse_mode='MarkdownV2')

    elif command == "/sub_buy":
        response = requests.get(settings.BACKEND_URL + '/subscription/list').json()
        msg = "Доступные подписки:"
        subscriptions = [sub for sub in response.get("value") if not sub.get("is_free")]
        for num, sub in enumerate(subscriptions):
            msg += f"\n{num + 1}. {sub.get('name')} - {sub.get('description')}"

        msg += "\n\ncoming soon\nК сожалению, на данный момент ЮKassa не подключена. "

        bot.send_message(message.chat.id, msg)  # , parse_mode='MarkdownV2')

    elif command == "/new_post":
        bot.send_message(message.chat.id, settings.new_post_message, parse_mode='MarkdownV2')
        bot.register_next_step_handler(message, post_generation)


def post_generation(message):
    if len(message.text.split()) < 3:
        bot.send_message(message.chat.id, settings.low_info_message)
        return None

    # restrict_user(message.chat.id, message.from_user.id, can_send_messages=False)
    bot.send_message(message.chat.id, settings.start_generate_message)

    data = {
        "chat_id": message.chat.id,
        "message": message.text
    }
    response = requests.post(settings.BACKEND_URL + '/post/create', json=data).json()
    if response["success"]:
        send_message_with_feedback(chat_id=message.chat.id, post=response.get("value", ""))
    else:
        bot.send_message(message.chat.id, settings.server_error_message)
    # restrict_user(message.chat.id, message.from_user.id, can_send_messages=True)


def send_message_with_feedback(chat_id, post):
    markup = InlineKeyboardMarkup()
    thumbs_up_button = InlineKeyboardButton("👍", callback_data="1")
    neutrality = InlineKeyboardButton("😐", callback_data="0")
    thumbs_down_button = InlineKeyboardButton("👎", callback_data="-1")
    markup.add(thumbs_up_button, neutrality, thumbs_down_button)
    bot.send_message(chat_id, post, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "1":
        bot.answer_callback_query(call.id, settings.thumbs_up_message)
    elif call.data == "0":
        bot.answer_callback_query(call.id, settings.neutrality_message)
    elif call.data == "-1":
        bot.answer_callback_query(call.id, settings.thumbs_down_message)

    data = {
        "chat_id": call.from_user.id,
        "post": call.message.text,
        "feedback": call.data
    }

    requests.post(settings.BACKEND_URL + '/post/feedback', json=data).json()


def restrict_user(chat_id, user_id, can_send_messages):
    permissions = ChatPermissions(can_send_messages=can_send_messages)
    bot.restrict_chat_member(chat_id, user_id, permissions)


if __name__ == "__main__":
    bot.polling()
