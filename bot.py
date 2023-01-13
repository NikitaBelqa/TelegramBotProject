import telebot
from telebot import *
import config
import PIL
from PIL import Image

bot = telebot.TeleBot(config.TOKEN)

#Клавиатура
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
start_call = types.KeyboardButton("/start")
reply_markup=markup
markup.add(start_call)


@bot.message_handler(commands = ['start']) #Ответ на команду /start 
def Welcome(message):
    welcome_text = "Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>, бот созданный, чтобы подготовить любую Вашу фоторграфию для стикеров. \nПросто пришлите мне НЕ СЖАТОЕ фото (в виде файла), и я верну вам его в нужном формате и размерах для стикера. "
    bot.send_message(message.chat.id, welcome_text.format(message.from_user, bot.get_me()), parse_mode='html')


@bot.message_handler(content_types=['photo']) #присылается ЛЮБОЕ фото
def Photo(message):
    file_name = message.photo.file_name
    file_info = bot.get_file(message.photo.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(file_name, 'wb') as new_file:
        new_file.write(downloaded_file)

    img = Image.open(new_file)
    width, height = img.size
    print("Начальные размеры картинки -", img.size)

    k = float(width/512)
    new_width = int(width/k)
    new_height = int(height/k)

    new_image = img.resize((new_width, new_height))
    print("Конечные размеры картинки -", new_image.size)
    bot.send_photo(message.chat.id, new_image)
    



bot.infinity_polling()

