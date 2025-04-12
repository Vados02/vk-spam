import requests
import random
import time
from datetime import datetime
import os

# Твой токен VK API (https://vkhost.github.io/)  
CONFIG_FILE = "config.txt"
# Группы для публикацииhttps://t.me/work_cach_bot
GROUPS = []

# Сообщения для публикации
POST_MESSAGES = []


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
        os.system("shutdown now")
