from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import openai
import time
import random
from selenium.common.exceptions import TimeoutException

from open_ai.openai_utils import generate_tweet

# Вход в Twitter
def login_twitter(driver: webdriver.Chrome, email: str, password: str) -> None:
    try:
        driver.get("https://twitter.com/login")
        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "text"))
        )
        email_input.send_keys(email)
        email_input.send_keys(Keys.ENTER)
        time.sleep(3)

        password_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "password"))
        )
        password_input.send_keys(password)
        password_input.send_keys(Keys.ENTER)
        time.sleep(3)
    except Exception as e:
        print(f"Ошибка при входе в Twitter: {e}")

# Изменение пароля в Twitter
def change_password(driver: webdriver.Chrome, current_password: str, new_password: str) -> None:
    try:
        driver.get("https://twitter.com/settings/password")
        current_password_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "current_password"))
        )
        current_password_input.send_keys(current_password)

        new_password_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "new_password"))
        )
        new_password_input.send_keys(new_password)

        confirm_password_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "password_confirmation"))
        )
        confirm_password_input.send_keys(new_password)

        save_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='settingsDetailSave']"))
        )
        save_button.click()
        time.sleep(10)
    except Exception as e:
        print(f"Ошибка при изменении пароля: {e}")

# Создание случайного поста в Twitter
def post_random_tweet(driver: webdriver.Chrome) -> None:
    try:
        driver.get("https://x.com/home")
        time.sleep(3)
        tweet = generate_tweet()
        
        # Проверка текста в диапазоне BMP
        tweet = ''.join(c for c in tweet if ord(c) <= 0xFFFF)
        
        # Проверка длины и обрезка текста
        max_length = 216
        trim_length = 216
        if len(tweet) > max_length:
            tweet = tweet[:trim_length]
        
        print("tweet = ", tweet)
 
        # Клик по полю для ввода твита
        tweet_input_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@data-testid='tweetTextarea_0RichTextInputContainer']"))
        )
        tweet_input_field.click()
        time.sleep(3)

        # Ввод текста твита
        tweet_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true']"))
        )
        tweet_box.send_keys(tweet)
        time.sleep(3)

        # Клик по кнопке "Post"
        try:
            # Ожидание появления кнопки
            tweet_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@data-testid='tweetButtonInline']"))
            )
            # tweet_button.click()
            driver.execute_script("arguments[0].click();", tweet_button)
            time.sleep(3)
        except TimeoutException:
            # Если обычный клик не сработал, выполняем клик через JavaScript
            print("Обычный клик не сработал, пробуем кликнуть через JS")
            driver.execute_script("arguments[0].click();", tweet_button)
            time.sleep(3)
    except Exception as e:
        print(f"Ошибка при публикации твита: {e}")

