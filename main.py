from social_network_app import SocialNetworkApp

if __name__ == "__main__":
    app = SocialNetworkApp()


    while True:
        print("\nМеню:")
        print("1. Вхід за логіном і паролем")
        print("2. Додати користувача")
        print("3. Видалити користувача")
        print("4. Редагувати інформацію про користувача")
        print("5. Пошук користувача за ПІБ")
        print("6. Перегляд інформації про користувача")
        print("7. Перегляд усіх друзів користувача")
        print("8. Перегляд усіх публікацій користувача")
        print("9. Додати друга")
        print("10. Додати публікацію")
        print("0. Вихід")

        choice = input("Оберіть опцію: ")

        if choice == "1":
            username = input("Введіть логін: ")
            password = input("Введіть пароль: ")
            app.login(username, password)
        elif choice == "2":
            user_data = {
                'username': input("Введіть логін користувача: "),
                'password': input("Введіть пароль користувача: "),
                'full_name': input("Введіть ПІБ користувача: "),
                # Додаткові дані, які можна додати
            }
            app.add_user(user_data['username'], user_data['password'])
        elif choice == "3":
            username = input("Введіть логін користувача для видалення: ")
            app.delete_user(username)
        elif choice == "4":
            username = input("Введіть логін користувача для редагування: ")
            new_data = {
                'password': input("Введіть новий пароль (натисніть Enter, якщо не хочете змінювати): "),
                'full_name': input("Введіть нове ПІБ (натисніть Enter, якщо не хочете змінювати): "),
                # Додаткові дані для редагування
            }
            app.edit_user(username, new_data)
        elif choice == "5":
            full_name = input("Введіть ПІБ користувача для пошуку: ")
            result = app.search_user_by_name(full_name)
            print(f"Результат для користувача з ПІБ {full_name}: {result}")
        elif choice == "6":
            username = input("Введіть логін користувача для перегляду інформації: ")
            result = app.view_user_info(username)
            print(f"Інформація про користувача {username}: {result}")
        elif choice == "7":
            username = input("Введіть логін користувача для перегляду друзів: ")
            result = app.view_user_friends(username)
            print(f"Друзі користувача {username}: {result}")
        elif choice == "8":
            username = input("Введіть логін користувача для перегляду публікацій: ")
            result = app.view_user_posts(username)
            print(f"Публікації користувача {username}: {result}")

        elif choice == "9":
            username = input("Введіть ваш логін: ")
            friend_username = input("Введіть логін користувача, якого хочете додати в друзі: ")
            app.add_friend(username, friend_username)

        elif choice == "10":
            username = input("Введіть ваш логін: ")
            text = input("Введіть текст публікації: ")
            app.add_post(username, text)

        elif choice == "0":
            break
        else:
            print("Невірний вибір. Спробуйте ще раз.")
