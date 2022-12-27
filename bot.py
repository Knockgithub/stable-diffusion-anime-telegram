import telebot
import requests
import base64
from stablediff import get_ai_image

from config import token

bot = telebot.TeleBot(token)


@bot.message_handler(content_types=["photo"])
def start(message):

    bot.send_message(message.from_user.id, "🤖Нейросеть конвертирует фото")

    # Получаем ID фоторгафии
    fileID = message.photo[-1].file_id
    filepath = bot.get_file(fileID).file_path

    # Скачиваем фотографию
    r = requests.get(
        "https://api.telegram.org/file/bot" + token + "/" + filepath,
        timeout=None,
        stream=True,
    )

    # Преобразовываем картинку в base64
    base64_image_string = base64.b64encode(r.content).decode("utf-8")

    # Получаем ссылку на обработанное изображение
    ai_image = get_ai_image(base64_image_string)["media_info_list"][0]["media_data"]

    bot.send_photo(message.from_user.id, ai_image)


bot.polling(none_stop=True, interval=0)
