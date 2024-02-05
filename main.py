import redis
import bcrypt
import json
import datetime


class SocialNetworkApp:
    def __init__(self, redis_host="localhost", redis_port=6379, redis_db=1):
        self.redis = redis.StrictRedis(host=redis_host, port=redis_port, db=redis_db)  # decode_responses=True

    def add_user(self, username, password):
        if self.redis.hexists('users', username):
            print("Користувач вже існує!")
            return False
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        user_data = {
            'password_hash': password_hash.decode('utf-8'),
            'friends': [],
            'posts': []
        }
        self.redis.hset('users', username, json.dumps(user_data))
        print("Користувач успішно зареєстрований")
        return True

    def login(self, username, password):
        stored_user_data = self.redis.hget('users', username)
        if stored_user_data:
            user_data = json.loads(stored_user_data)
            stored_password_hash = user_data.get("password_hash")
            if stored_password_hash and bcrypt.checkpw(password.encode('utf-8'), stored_password_hash.encode('utf-8')):
                print(f'Ви увійшли як {username}')
                self.current_user = username
                return True
            print('Невірний логін або пароль')
            return False

    def delete_user(self, username):
        if self.redis.hexists('users', username):
            self.redis.hdel('users', username)
            print("Користувач видалений")
        else:
            print("Користувач не знайдений")

    def edit_user(self, username, new_data):
        if not self.redis.hexists('users', username):
            print("Користувач не знайдений!")
            return
        stored_data = self.redis.hget('users', username)
        if stored_data:
            try:
                user_data = json.loads(stored_data)
            except json.JSONDecodeError:
                print("Помилка декодування данних користувача")
                return
        else:
            print("Дані користувача відсутні або пошкоджені")
            return
        for key, value in new_data.items():
            if value:
                user_data[key] = value

        self.redis.hset('users', username, json.dumps(user_data))
        print("Інформація користувача оновлена")