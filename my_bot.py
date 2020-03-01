import requests
import bot_setup
import time


class MyBot:

    def __init__(self, token):
        self._TOKEN = token
        self._URL = f'https://api.telegram.org/bot{self._TOKEN}/'
        self._UPDATE_ID = None

    def get_updates(self):
        url = self._URL + 'getupdates'
        request = requests.get(url)
        return request.json()

    def get_message(self):
        data = self.get_updates()
        last_obj = data['result'][-1]
        update_id = last_obj['update_id']
        chat_id = last_obj['message']['chat']['id']
        message_text = last_obj['message']['text']

        if self._UPDATE_ID != update_id:
            self._UPDATE_ID = update_id
            message = {'chat_id': chat_id, 'text': message_text}
            return message
        else:
            return {}

    def send_message(self, chat_id, text='Wait a second, please ..'):
        url = f"{self._URL}sendmessage?chat_id={chat_id}&text={text}"
        requests.get(url)

    def run(self):
        while True:
            answear = self.get_message()
            if answear.get('text') == '/btc':
                self.send_message(answear['chat_id'], MyBot.get_btc())
            elif answear.get('text') == '/usd':
                self.send_message(answear['chat_id'], MyBot.get_usd_private())
            elif answear.get('chat_id'):
                self.send_message(answear['chat_id'], "может купишь биток")
            time.sleep(1)

    @staticmethod
    def get_btc():
        url = 'https://api.exmo.com/v1/ticker/'
        price = requests.get(url).json()['BTC_USD']['sell_price']
        return f'{round(float(price))} usd'

    @staticmethod
    def get_usd_private():
        url = 'https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5'
        price = requests.get(url).json()[0]['buy']
        return f'{float(price)} uah'


if __name__ == '__main__':
    bot = MyBot(bot_setup.token)
    bot.run()
