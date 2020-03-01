import requests
import bot_setup
from coin import get_btc, get_usd_private
import time
import json








TOKEN = bot_setup.token
URL = f'https://api.telegram.org/bot{TOKEN}/'
GLOB_UPDATE_ID = None


def get_updates():
    url = URL + 'getupdates'
    request = requests.get(url)
    return request.json()


def get_message():
    data = get_updates()
    last_obj = data['result'][-1]
    update_id = last_obj['update_id']
    chat_id = last_obj['message']['chat']['id']
    message_text = last_obj['message']['text']

    global GLOB_UPDATE_ID
    if GLOB_UPDATE_ID != update_id:
        GLOB_UPDATE_ID = update_id
        message = {'chat_id': chat_id, 'text': message_text}
        return message
    else:
        return {}


def send_message(chat_id, text='Wait a second, please ..'):
    url = f"{URL}sendmessage?chat_id={chat_id}&text={text}"
    requests.get(url)


def main():
    # request = get_updates()
    # with open('bot.json', 'w') as file:
    #     json.dump(request, file, indent=2, ensure_ascii=False)
    while True:
        answear = get_message()
        if answear.get('text') == '/btc':
            send_message(answear['chat_id'], get_btc())
        elif answear.get('text') == '/usd':
            send_message(answear['chat_id'], get_usd_private())
        elif answear.get('chat_id'):
            send_message(answear['chat_id'], "может купишь биток")
        else:
            continue
        time.sleep(1)


if __name__ == '__main__':
    main()
