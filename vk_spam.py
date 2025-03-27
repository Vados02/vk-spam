import requests
import random
import time

# 🔹 Твой токен VK API (https://vkhost.github.io/)
ACCESS_TOKEN = ""

# 🔹 ID групп
GROUPS = []

# 🔹 Сообщения для публикации
POST_MESSAGES = []


# Получаем числовой ID группы по короткому имени
def get_group_id(group_name):
    url = "https://api.vk.com/method/groups.getById"
    params = {
        "access_token": ACCESS_TOKEN,
        "v": "5.131",
        "group_id": group_name
    }
    response = requests.get(url, params=params).json()
    
    if "error" in response:
        print(f"❌ Ошибка получения ID группы {group_name}: {response['error']['error_msg']}")
        return None
    return response["response"][0]["id"]

# Функция для публикации поста
def post_to_vk(group_id):
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

# Интервалы по времени чтобы не забанили
time = []

# Запуск рассылки
for group in GROUPS:
    group_id = get_group_id(group)  # Получаем ID группы
    if group_id:
        post_to_vk(group_id)
        time.sleep(random.choice(time))  # Пауза, чтобы не словить бан за спам
