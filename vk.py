import requests
import random
import time
from datetime import datetime
import os

# Твой токен VK API (https://vkhost.github.io/)  
CONFIG_FILE = "config.txt"
# Группы для публикацииhttps://t.me/work_cach_bot
GROUPS_1 = ["mihilson2090", "inetwoorking", "club76701772", "biz_obyava2", "zarabotok_mdk", "club131157242", "work_on_the_internet_2024", "piar_ot_karpycheva"]
GROUPS_2 = ["club130591079", "club79067401", "club119131616", "rabota_zarabotok_v_internet3", 'club80110611', "joinmygroup", "club83077374", "club146463949"]

# Сообщения для публикации
POST_MESSAGES = [
    "Ищем людей для заработка! Разово оформите офер наших продуктов и получите до 5000 ₽. Также платим 500 ₽ за каждого приведённого клиента. Подробности в боте!\n Заработок: http://t.me/Road_to_Cashbot",
    "Нужны люди для разового заработка – до 5000 ₽! Платим 500 ₽ за клиента. Инфо в боте!\nhttp://t.me/Road_to_Cashbot",
    "Быстрый доход! Разовый офер – до 5000 ₽. Платим 500 ₽ за каждого клиента. Подробнее в боте.\nhttp://t.me/Road_to_Cashbot",
    "Ищем партнёров для заработка! До 5000 ₽ + 500 ₽ за каждого клиента. Подробности в боте!\nhttp://t.me/Road_to_Cashbot",
    "Готовы заработать 5000 ₽? Оформите офер разово или приводите клиентов (500 ₽ за каждого). Инфо в боте!\nhttp://t.me/Road_to_Cashbot",
    "Лёгкий заработок! 5000 ₽ или 500 ₽ за клиента. Всё честно! Подробности тут:\nhttp://t.me/Road_to_Cashbot",
    "Работа без вложений! 5000 ₽ или 500 ₽ за каждого клиента. Готов? Пиши в бот:\nhttp://t.me/Road_to_Cashbot",
    "Заработок до 5000 ₽! Оформите офер разово или приводите клиентов за 500 ₽. Все детали тут:\nhttp://t.me/Road_to_Cashbot",
    "Хотите заработать? Оформите офер (до 5000 ₽) или приводите клиентов (500 ₽). Пиши в бот:\nhttp://t.me/Road_to_Cashbot",
    "Лёгкий способ заработать! Разовый доход до 5000 ₽ или 500 ₽ за клиента. Информация здесь:\nhttp://t.me/Road_to_Cashbot",
    "Заработай без вложений! 5000 ₽ + 500 ₽ за каждого приведённого клиента. Подробности в боте!\nhttp://t.me/Road_to_Cashbot",
    "Работа на неделю – 5000 ₽! Или приводи клиентов за 500 ₽ каждого. Всё честно! Подробности тут:\nhttp://t.me/Road_to_Cashbot",
    "Нужны деньги? Оформите офер – 5000 ₽! Или приводите клиентов (500 ₽ за каждого). Пишите:\nhttp://t.me/Road_to_Cashbot",
    "Быстрый доход – 5000 ₽! Разово оформите офер или приводи клиентов за 500 ₽. Подробнее:\nhttp://t.me/Road_to_Cashbot",
    "Заработай с нами! 5000 ₽ или 500 ₽ за каждого приведённого клиента. Инфо тут:\nhttp://t.me/Road_to_Cashbot",
    "Хочешь 5000 ₽? Оформите офер! Или приводи клиентов за 500 ₽. Все детали тут:\nhttp://t.me/Road_to_Cashbot",
    "Работа с доходом 5000 ₽! Или приведи друзей – 500 ₽ за каждого. Всё честно! Подробности тут:\nhttp://t.me/Road_to_Cashbot",
    "Есть способ заработать! 5000 ₽ разово или 500 ₽ за клиента. Всё честно! Пиши в бот:\nhttp://t.me/Road_to_Cashbot",
    "Простой способ заработать! 5000 ₽ разово или 500 ₽ за друга. Инфо в боте:\nhttp://t.me/Road_to_Cashbot",
    "Хочешь 5000 ₽? Разово оформите офер! Или приводи клиентов – 500 ₽ за каждого. Все детали тут:\nhttp://t.me/Road_to_Cashbot"
]


# Чтение пути изображения из файла
def read_banner_path():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as file:
            return file.read().strip()
    return None

# Запись пути изображения в файл
def write_banner_path(path):
    with open(CONFIG_FILE, "w") as file:
        file.write(path)

def get_group_id(group_name):
    url = "https://api.vk.com/method/groups.getById"
    params = {"access_token": ACCESS_TOKEN, "v": "5.131", "group_id": group_name}
    response = requests.get(url, params=params).json()
    return response.get("response", [{}])[0].get("id")

# Функция загрузки фото в группу
def upload_photo(group_id, image_path):
    server_url = "https://api.vk.com/method/photos.getWallUploadServer"
    params = {"access_token": ACCESS_TOKEN, "v": "5.131", "group_id": group_id}
    server_response = requests.get(server_url, params=params).json()
    upload_url = server_response["response"]["upload_url"]
    
    with open(image_path, "rb") as image_file:
        files = {"photo": ("banner.jpg", image_file, "image/jpeg")}
        upload_response = requests.post(upload_url, files=files).json()
    
    save_url = "https://api.vk.com/method/photos.saveWallPhoto"
    save_params = {
        "access_token": ACCESS_TOKEN,
        "v": "5.131",
        "group_id": group_id,
        "photo": upload_response["photo"],
        "server": upload_response["server"],
        "hash": upload_response["hash"]
    }
    save_response = requests.get(save_url, params=save_params).json()
    photo = save_response["response"][0]
    return f"photo{photo['owner_id']}_{photo['id']}"

# Функция публикации поста
def post_to_vk(group_id):
    attachment = upload_photo(group_id, BANNER_PATH)
    url = "https://api.vk.com/method/wall.post"
    params = {
        "access_token": ACCESS_TOKEN,
        "v": "5.131",
        "owner_id": f"-{group_id}",
        "message": random.choice(POST_MESSAGES),
        "from_group": 0,
        "attachments": attachment,
        "publish_date": 0  # Публикация сразу"
    }
    response = requests.post(url, params=params).json()


# Запуск публикации
# Запуск публикации
def main():
    # Проверим, есть ли сохранённый путь к изображению
    banner_path = read_banner_path()
    if not banner_path:
        banner_path = input('Введите путь к баннеру для поста: ')
        write_banner_path(banner_path)  # Сохраняем путь в файл

    now = datetime.now()
    if now.day % 2 == 0:
        GROUPS = GROUPS_1
    else:
        GROUPS = GROUPS_2
    for group in GROUPS:
        group_id = get_group_id(group)
        if group_id:
            post_to_vk(group_id)
            print(f'Сообщение отправлено в группу: {group}')
            time.sleep(300)

BANNER_PATH = read_banner_path()  # Пытаемся прочитать путь из файла

if __name__ == "__main__":
    print('Твой токен VK API (https://vkhost.github.io/)')
    BANNER_PATH = read_banner_path()  # Пытаемся прочитать путь из файла
    ACCESS_TOKEN = str(input('Введите VK token: '))
    status_shutdown = str(input('Выключить компьютер после завершения рассылки? да/нет: '))
    main()
    print('Рассылка завершена')
    if status_shutdown.lower() == 'да':
        #os.system("shutdown /s /f /t 0")
        os.system("shutdown now")