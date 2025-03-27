import requests
import random
from parameters import ACCESS_TOKEN, BANNER_URL, POST_MESSAGES, GROUPS

# Функция получения ID группы
def get_group_id(group_name):
    url = "https://api.vk.com/method/groups.getById"
    params = {"access_token": ACCESS_TOKEN, 
              "v": "5.131", 
              "group_id": group_name}
    response = requests.get(url, params=params).json()
    return response.get("response", [{}])[0].get("id")

# Функция загрузки фото в группу
def upload_photo(group_id, image_url):
  
    server_url = "https://api.vk.com/method/photos.getWallUploadServer"
    params = {"access_token": ACCESS_TOKEN, 
              "v": "5.131", 
              "group_id": group_id}
    server_response = requests.get(server_url, params=params).json()
    upload_url = server_response["response"]["upload_url"] # Загрузка на сервер
    
    image_data = requests.get(image_url).content
    files = {"photo": ("image.jpg", image_data, "image/jpeg")}
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
def post_to_vk(group_id, status):
    if status == 1:
        attachment = upload_photo(group_id, BANNER_URL)
        url = "https://api.vk.com/method/wall.post"

        params = {
            "access_token": ACCESS_TOKEN,
            "v": "5.131",
            "owner_id": f"-{group_id}", # ID группы с минусом
            "message": random.choice(POST_MESSAGES), # Случайное сообщение
            "from_group": 0, # Чтобы пост выложился от вашего имени 0, от имени группы 1
            "publish_date": 0, # Публикация сразу
            "attachments": attachment # Прикрепление картинки
        }
        response = requests.post(url, params=params).json()
        if "error" in response:
            print(f"❌ Ошибка при публикации в группу {group_id}: {response['error']['error_msg']}")
        else:
            print(f"✅ Пост опубликован в группу {group_id}")

    elif status == 2:
        url = "https://api.vk.com/method/wall.post"
        params = {
            "access_token": ACCESS_TOKEN,
            "v": "5.131",
            "owner_id": f"-{group_id}",  # ID группы с минусом
            "message": random.choice(POST_MESSAGES),  # Случайное сообщение
            "from_group": 0,  # Должно быть 1, чтобы пост шел от имени группы, 0  от вашего
            "publish_date": 0  # Публикация сразу
            }
        response = requests.post(url, params=params).json()

        if "error" in response:
            print(f"❌ Ошибка при публикации в группу {group_id}: {response['error']['error_msg']}")
        else:
            print(f"✅ Пост опубликован в группу {group_id}")
    else:
        print('Ошибка')

time_v = [300, 900, 600, 560, 1200, 400]

# Запуск публикации
status = int(input('Введите статус рассылки: \n1 - image_post\n2 - text_post\n'))
for group in GROUPS:
    group_id = get_group_id(group)
    if group_id:
        post_to_vk(group_id, status)
        time.sleep(300) # Пауза чтобы не добавили
