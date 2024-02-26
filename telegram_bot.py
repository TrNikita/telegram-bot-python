import os
import requests
from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("TOKEN")  

CRYPTO_NAME_TO_TICKER = {
    "Bitcoin":  "BTCUSDT",
    "Ethereum": "ETHUSDT",
    "Doge":     "DOGEUSDT"
}

bot = TeleBot(token)

@bot.message_handler(commands=['start'])
def send_welcome(message):
  markup = ReplyKeyboardMarkup(row_width=3)
  for crypto_name in CRYPTO_NAME_TO_TICKER:
    item_button = KeyboardButton(crypto_name)
    markup.add(item_button)
  bot.send_message(message.chat.id, 'Choose a crypto', reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in CRYPTO_NAME_TO_TICKER.keys())
def send_price(message): 
  crypto_name = message.text
  print(crypto_name)
  print(message)
  ticker = CRYPTO_NAME_TO_TICKER[crypto_name]
  price = get_price_by_ticker(ticker=ticker)
  bot.send_message(message.chat.id, f'Price of {crypto_name} to USDT is {price}')

def get_price_by_ticker(*, ticker: str) -> float:
  url = 'https://api.binance.com/api/v3/ticker/price'
  params = {
    'symbol': ticker 
  }
  response = requests.get(url, params=params)
  data = response.json()
  price = round(float(data['price']), 2)
  return price

bot.infinity_polling()