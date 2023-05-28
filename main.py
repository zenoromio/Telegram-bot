import gspread
import messages
from oauth2client.service_account import ServiceAccountCredentials
import random
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


API_TOKEN = '5838704651:AAGhIUuPpDzt059feiakFYhjlO5Qw1NPc5o'
bot = telebot.TeleBot(API_TOKEN)

# Connect to Google Sheets
scope = ['https://www.googleapis.com/auth/spreadsheets', "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name("botzeno.json", scope)
client = gspread.authorize(credentials)
sheet = client.open("NewDatabase").sheet1


# find first cell empty in a column
def next_available_row(worksheet, col):
    str_list = list(filter(None, worksheet.col_values(col)))
    return str(len(str_list)+1)


# handles /start command
@bot.message_handler(commands=['start'])
def welcome_message(message):
    bot.send_message(message.chat.id, messages.start_message, parse_mode="MarkdownV2")

    #update the sheet with the username and the command used
    sheet.update("A" + next_available_row(sheet, 4), [[message.from_user.first_name, message.from_user.last_name, message.from_user.username, message.text]])


# handles /stats command
@bot.message_handler(commands=['stats'])
def send_stats(message):
    bot.send_message(message.chat.id, messages.stats_message, parse_mode="MarkdownV2")

    #update the sheet with the username and the command used
    sheet.update("A" + next_available_row(sheet, 4), [[message.from_user.first_name, message.from_user.last_name, message.from_user.username, message.text]])


# handles /zodiac command
@bot.message_handler(commands=['zodiac'])
def send_profiles(message):
    bot.send_message(message.chat.id, messages.zodiac_message, parse_mode="MarkdownV2")

    #update the sheet with the username and the command used
    sheet.update("A" + next_available_row(sheet, 4), [[message.from_user.first_name, message.from_user.last_name, message.from_user.username, message.text]])


# handles /social command
@bot.message_handler(commands=['socials'])
def send_profiles(message):
    bot.send_message(message.chat.id, messages.social_message, parse_mode="MarkdownV2")

    #update the sheet with the username and the command used
    sheet.update("A" + next_available_row(sheet, 4), [[message.from_user.first_name, message.from_user.last_name, message.from_user.username, message.text]])


def closet():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Sferaebbasta", callback_data="Sfera"), InlineKeyboardButton("PallacanestroVicenza", callback_data="Basket"))
    markup.add(InlineKeyboardButton("PaoloLioy", callback_data="Lioy"), InlineKeyboardButton("FootballUSA", callback_data="America"))
    return markup

@bot.message_handler(commands=['hoodies'])
def show_shop(message):
    bot.send_message(message.chat.id,"Benvenuto nell'armadio delle felpe di Zeno. Cosa vuoi vedere?",reply_markup=closet())

    #update the sheet with the username and the command used
    sheet.update("A" + next_available_row(sheet, 4), [[message.from_user.first_name, message.from_user.last_name, message.from_user.username, message.text]])

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    bot.answer_callback_query(call.id, "Felpa in arrivo")
    if call.data == "Sfera":
        bot.send_photo(call.message.chat.id, open("zenos_hoodies/felpa1.jpeg", "rb"))
        bot.send_message(call.message.chat.id, "Sferaebbasta $€ Purple x Zeno")
    elif call.data == "Basket":
        bot.send_photo(call.message.chat.id, open("zenos_hoodies/felpa2.jpeg", "rb"))
        bot.send_message(call.message.chat.id, "Pallacanestro Vicenza 2012 x Zeno")
    elif call.data == "Lioy":
        bot.send_photo(call.message.chat.id, open("zenos_hoodies/felpa3.jpeg", "rb"))
        bot.send_message(call.message.chat.id, "Lioy Beta Midnight Blue x Zeno")
    elif call.data == "America":
        bot.send_photo(call.message.chat.id, open("zenos_hoodies/felpa4.jpeg", "rb"))
        bot.send_message(call.message.chat.id, "UME Eagle Football x ZenoMVP")
    else:
        bot.answer_callback_query(call.id, "Nigga")

@bot.message_handler(commands=['cameraroll'])
def send_pic(message):
    #generate random number for pic
    rad_num = random.randint(1, 32)
    bot.send_photo(message.chat.id, open("zenos_pics/" + str(rad_num) + ".jpeg", "rb"))
    bot.send_message(message.chat.id, messages.captions[str(rad_num)])
    bot.send_message(message.chat.id, "Molto bello vero? Premi /cameraroll per vedere un'altra foto random")
    #update the sheet with the username and the command used
    sheet.update("A" + next_available_row(sheet, 4), [[message.from_user.first_name, message.from_user.last_name, message.from_user.username, message.text]])


@bot.message_handler(commands=['message'])
def send_profiles(message):
    bot.send_message(message.chat.id, "Scrivi un messaggio e firmati così so che sei passato/a⬇️⬇️⬇️")

    bot.register_next_step_handler(message, handle_message)

def handle_message(message):
    bot.send_message(message.chat.id, "Grazie il tuo messaggio è stato ricevuto!")

    sheet.update("F" + next_available_row(sheet, 9), [[message.from_user.first_name, message.from_user.last_name, message.from_user.username, message.text]])



@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, "Scusa non so ancora come rispondere a questo messaggio")


bot.infinity_polling()