from selenium import webdriver
import random
from multiprocessing import Pool

from x_utils import login_twitter, change_password, post_random_tweet
from proxy_setup import create_driver

# Функция для тестирования одного аккаунта
def test_account(account):
    email, password = account
    driver = create_driver()
    
    new_password = ''.join(random.choices("abcdefghijklmnopqrstuvwxyz0123456789", k=10))
    print(f"Testing account: {email}, new password: {new_password}")

    try:
        # Вход в Twitter
        login_twitter(driver, email, password)

        # Изменение пароля
        change_password(driver, password, new_password)

        # Пост в Twitter
        post_random_tweet(driver)

    except Exception as e:
        print(f"Ошибка при работе с аккаунтом {email}: {e}")

    finally:
        driver.quit()

# Основной процесс
if __name__ == "__main__":
    # Список аккаунтов
    accounts = [
        ("email1@example.com", "password1"),
        ("email2@example.com", "password2"),
        # Добавьте больше аккаунтов
    ]

    # Параллельное тестирование
    with Pool(processes=len(accounts)) as pool:
        pool.map(test_account, accounts)

