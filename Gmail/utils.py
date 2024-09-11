from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver

from oauth2client.service_account import ServiceAccountCredentials
import gspread

import time

# Вход в аккаунт
def login_google(driver: webdriver, email: str, password: str) -> None:
    try:
        
        # Открываем конкретную страницу входа Gmail
        driver.get("https://myaccount.google.com/personal-info")
        time.sleep(2)
        
        # Ожидание и клик по кнопке "Войти"
        sign_in_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@class='gb_Ua gb_yd gb_pd gb_gd']"))
        )
        sign_in_button.click()
        time.sleep(2)
        
        # Ввод email
        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "identifierId"))
        )
        email_input.send_keys(email)
        email_input.send_keys(Keys.ENTER)
        time.sleep(3)

        # Ввод пароля
        password_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='password']"))
        )
        password_input.send_keys(password)
        password_input.send_keys(Keys.ENTER)
        time.sleep(3)
        
    except Exception as e:
        print(f"Ошибка при входе в Google: {e}")

# Получение информации о аккаунте
def get_data(driver: webdriver, email: str, password: str) -> None:
    try:
        
        fields = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "bJCr1d"))
        )
        
        # Получаем текст каждого поля
        name = fields[0].text  # поле имени
        birthdate = fields[1].text  # поле даты рождения
        gender = fields[2].text  # поле пола
        return email, password, name, birthdate, gender
    
    except Exception as e:
        print(f"Ошибка при получении данных: {e}")
        return email, password, "", "", ""

# Вставка информации в Google Таблицы
def insert_data_into_google_sheet(email: str, password: str, name: str, birthdate: str, gender: str) -> None:
    print("Настройка доступа к Google Sheets API")
    try:
        
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name('C:\\Users\\thatn\\Downloads\\secure-granite-432318-u3-0d3b5ce8ff16.json', scope)
        client = gspread.authorize(creds)

        # Открытие таблицы по ссылке
        sheet = client.open_by_url('https://docs.google.com/spreadsheets/d/1FfG5GMMIvNGihymauCQDkVG_pl3t8JbbYmyN09XKXWI/edit?usp=sharing').sheet1

        sheet.append_row([email, password, name, birthdate, gender])
        
    except gspread.exceptions.APIError as e:
        print(f"Ошибка API: {e}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

# Изменение пароля аккаунта
def change_password(driver: webdriver, new_password: str) -> None:
    try:
        
        # Переход на страницу изменения пароля
        password_change_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'signinoptions/password')]"))
        )
        password_change_link.click()
        time.sleep(3)

        # Ввод нового пароля
        # new_password_input.clear()
        new_password_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "i6"))
        )
        new_password_input.send_keys(new_password)
        time.sleep(3)

        # Подтверждение нового пароля
        confirm_password_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "i12"))  # Поле для подтверждения
        )
        confirm_password_input.send_keys(new_password)
        time.sleep(3)

        # Клик по кнопке 'Save'
        save_button = driver.find_element(By.XPATH, "//span[@class='UywwFc-RLmnJb']")
        driver.execute_script("arguments[0].click();", save_button)
        time.sleep(3)
        
    except Exception as e:
        print(f"Ошибка при изменении пароля: {e}")

# Измененние имени аккаунта
def change_name(driver: webdriver, first_name: str, second_name: str) -> None:
    try:
        
        # Ожидание и клик по элементу с иконкой "chevron_right"
        chevron_icon =  WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@aria-label, 'Name')]"))
        )
        chevron_icon.click()
        time.sleep(3)
        
        # Ожидание и клик по ссылке "Edit Name"
        edit_name_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@aria-label, 'Edit Name')]"))
        )
        edit_name_link.click()
        time.sleep(3)
        
        # Ожидание и клик по label, связанному с полем для имени
        first_name_label = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//label[@for='i7']"))
        )
        first_name_label.click()

        # Ожидание появления поля ввода для изменения имени
        first_name_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "i7"))
        )
        
        # Очистка и ввод нового имени
        first_name_input.clear()
        first_name_input.send_keys(first_name)
        
        # Ожидание и клик по метке (label)
        label_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//label[@for='i12']"))
        )
        label_element.click()

        # Ожидание поля ввода и замена текста
        input_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "i12"))
        )
        input_field.clear()  # Очищаем текущее значение
        input_field.send_keys(second_name)  # Вводим новое значение
        
        # Ожидание и клик по элементу с классом "UywwFc-RLmnJb"
        span_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='Save']"))
        )
        span_link.click()
        
        back_button = driver.find_element(By.XPATH, "//div[@role='button' and @aria-label='Back']")
        driver.execute_script("arguments[0].click();", back_button)
        
    except Exception as e:
        print(f"Ошибка при изменении имени: {e}")
