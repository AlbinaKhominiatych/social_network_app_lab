import redis
import bcrypt
import json
import datetime

class SocialNetworkApp:
    def __init__(self, redis_host='localhost', redis_port=6379, redis_db=1):
        self.redis = redis.StrictRedis(host=redis_host, port=redis_port, db=redis_db, decode_responses=True)

    def add_user(self, username, password):
        # Перевірка, чи користувач вже існує
        if self.redis.hexists('users', username):
            print("Користувач вже існує.")
            return False
        # Зберігання хешу пароля у Redis
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        # Створення базової структури даних для нового користувача
        user_data = {
            'password_hash': password_hash.decode('utf-8'),  # Зберігаємо хеш пароля
            'friends': [],  # Початковий порожній список друзів
            'posts': []  # Початковий порожній список публікацій
        }

        # Зберігання даних користувача у форматі JSON
        self.redis.hset('users', username, json.dumps(user_data))
        print("Користувач успішно зареєстрований.")
        return True

    def login(self, username, password):
        # Перевірка логіну та пароля
        stored_user_data = self.redis.hget('users', username)
        if stored_user_data:
            user_data = json.loads(stored_user_data)  # Декодування даних користувача з формату JSON
            stored_password_hash = user_data.get('password_hash')
            # Перевірка хешу пароля
            if stored_password_hash and bcrypt.checkpw(password.encode('utf-8'), stored_password_hash.encode('utf-8')):
                print(f"Ви увійшли як {username}.")
                self.current_user = username
                return True
        # Якщо логін або пароль невірний
        print("Невірний логін або пароль.")
        return False

    def delete_user(self, username):
        # Видалити користувача з бази даних
        if self.redis.hexists('users', username):
            self.redis.hdel('users', username)
            print("Користувач видалений.")
        else:
            print("Користувач не знайдений.")

    def edit_user(self, username, new_data):
        # Редагувати інформацію про користувача
        if not self.redis.hexists('users', username):
            print("Користувач не знайдений.")
            return
        stored_data = self.redis.hget('users', username)
        # Переконуємось, що збережені дані не є пустими та можуть бути декодовані як JSON
        if stored_data:
            try:
                user_data = json.loads(stored_data)
            except json.JSONDecodeError:
                print("Помилка декодування даних користувача.")
                return
        else:
            print("Дані користувача відсутні або пошкоджені.")
            return

        # Оновлюємо дані користувача новими значеннями
        for key, value in new_data.items():
            if value:  # Переконуємось, що значення не є пустим перед оновленням
                user_data[key] = value

        # Зберігаємо оновлені дані назад у Redis
        self.redis.hset('users', username, json.dumps(user_data))
        print("Інформація про користувача оновлена.")

    def search_user_by_name(self, full_name):
        # Пошук користувача за ПІБ
        # Зауважте, цей метод може бути неефективним на великій кількості даних
        all_users = self.redis.hgetall('users')
        for username, user_info in all_users.items():
            user_data = json.loads(user_info)
            if user_data.get('full_name') == full_name:
                return user_data
        return "Користувач не знайдений."

    def view_user_info(self, username):
        # Перегляд інформації про користувача
        if self.redis.hexists('users', username):
            return json.loads(self.redis.hget('users', username))
        else:
            return "Користувач не знайдений."

    def view_user_friends(self, username):
        # Перегляд усіх друзів користувача
        # Припускаємо, що є список 'friends' в даних користувача
        user_info = self.view_user_info(username)
        if 'friends' in user_info:
            return user_info['friends']
        else:
            return "Список друзів не знайдено."

    def view_user_posts(self, username):
        # Перегляд усіх публікацій користувача
        # Припускаємо, що є список 'posts' в даних користувача
        user_info = self.view_user_info(username)
        if 'posts' in user_info:
            return user_info['posts']
        else:
            return "Публікації не знайдені."

    def add_friend(self, username, friend_username):
        # Перевірка, чи обидва користувачі існують
        if not self.redis.hexists('users', username) or not self.redis.hexists('users', friend_username):
            print("Один із користувачів не знайдений.")
            return False

        # Отримання і оновлення списку друзів користувача
        user_data = json.loads(self.redis.hget('users', username))
        if 'friends' not in user_data:
            user_data['friends'] = []
        if friend_username not in user_data['friends']:
            user_data['friends'].append(friend_username)
            # Зберігання оновлених даних користувача
            self.redis.hset('users', username, json.dumps(user_data))
            print(f"{friend_username} доданий до списку друзів {username}.")
            return True
        else:
            print(f"{friend_username} вже є в списку друзів {username}.")
            return False

    def add_post(self, username, text):
            # Перевірка, чи користувач існує
            if not self.redis.hexists('users', username):
                print("Користувач не знайдений.")
                return False

            # Отримання і оновлення списку публікацій користувача
            user_data = json.loads(self.redis.hget('users', username))
            post = {
                'text': text,
                'date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            if 'posts' not in user_data:
                user_data['posts'] = []
            user_data['posts'].append(post)
            # Зберігання оновлених даних користувача
            self.redis.hset('users', username, json.dumps(user_data))
            print(f"Нова публікація додана для {username}.")
            return True

