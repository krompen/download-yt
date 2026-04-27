import telebot
from telebot import types
from fake_useragent import UserAgent
import requests
import random
import string
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

API_TOKEN = '8440617021:AAHjnHWe6-FeITwpuMlTyeXTY3XCd0tl-mE'

bot = telebot.TeleBot(API_TOKEN)

def generate_random_email():
    domains = ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "mail.ru"]
    username = ''.join(random.choice(string.ascii_lowercase) for _ in range(8))
    domain = random.choice(domains)
    email = f"{username}@{domain}"
    return email

def generate_phone_number():
    country_codes = ['+7', '+380', '+375']
    country_code = random.choice(country_codes)
    phone_number = ''.join(random.choices('0123456789', k=10))
    formatted_phone_number = f'{country_code}{phone_number}'
    return formatted_phone_number

def send_complaint(chat_id, message, repeats):
    url = 'https://telegram.org/support'
    user_agent = UserAgent().random
    headers = {'User-Agent': user_agent}
    complaints_sent = 0
    for _ in range(repeats):
        email = generate_random_email()
        phone = generate_phone_number()
        response = requests.post(url, headers=headers, data={'message': message})
        if response.status_code == 200:
            complaints_sent += 1
            status = "✅Успешно"
        else:
            status = "❌Неуспешно"
        logging.info(f'Sent complaint: {message}, Email: {email}, Phone: {phone}, Status: {status}')
        bot.send_message(chat_id, f"✉️Сообщение: {message}\n📪Email: {email}\n📞Телефон: {phone}\n▶️Статус: {status}")
    return complaints_sent

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup()
    button_channel = types.InlineKeyboardButton("🔰 Канал", callback_data="channel")
    button_send = types.InlineKeyboardButton("🔥 Снос", callback_data="input_text")
    markup.add(button_channel, button_send)
    bot.reply_to(message, "Привет! Я бот сносер. Нажмите кнопку для начала.", reply_markup=markup)
    logging.info(f'User {message.chat.id} started the bot.')

@bot.callback_query_handler(func=lambda call: call.data == "channel")
def callback_channel(call):
    bot.send_message(call.message.chat.id, "**Channel - @exploitwizard**", parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: call.data == "input_text")
def callback_input_text(call):
    msg = bot.send_message(call.message.chat.id, "Введите текст сообщения:")
    bot.register_next_step_handler(msg, input_repeats)
    logging.info(f'User {call.message.chat.id} is entering text.')

def input_repeats(message):
    text = message.text
    msg = bot.send_message(message.chat.id, "Введите количество сообщений для отправки:")
    bot.register_next_step_handler(msg, lambda m: send_messages(m, text))
    logging.info(f'User {message.chat.id} entered text: {text}')

def send_messages(message, text):
    try:
        repeats = int(message.text)
        complaints_sent = send_complaint(message.chat.id, text, repeats)
        bot.send_message(message.chat.id, f"Успешно отправлено {complaints_sent} сообщений.")
        logging.info(f'User {message.chat.id} sent {repeats} messages.')
    except ValueError:
        bot.send_message(message.chat.id, "Ошибка: введите корректное число.")
        logging.error(f'User {message.chat.id} entered an invalid number: {message.text}')

bot.polling()
