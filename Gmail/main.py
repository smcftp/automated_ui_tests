from utils import login_google, change_password, get_data, insert_data_into_google_sheet, change_name
from proxy_setup import create_driver
from multiprocessing import Pool

import random
import string

# Список аккаунтов
accounts = [
    ("akakakvvvcc@gmail.com", "Y1oT5nkQLp")
    # ("email2@gmail.com", "password2"),
    # Добавьте больше аккаунтов
]

def run_test(account):
    email, password = account
    driver = create_driver()
    
    new_password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    first_name = ''.join(random.choices(string.ascii_letters + string.digits, k=5))
    second_name = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    
    if driver:
        try:
            login_google(driver, email, password)
            change_password(driver, new_password)
            change_name(driver, first_name, second_name)
            email, password, name, birthdate, gender = get_data(driver, email, password)
            insert_data_into_google_sheet(email, new_password, name, birthdate, gender)
        except Exception as e:
            print(f"Ошибка выполнения теста: {e}")
        finally:
            driver.quit()
    else:
        print("Не удалось создать драйвер.")

if __name__ == "__main__":
    # Параллельный запуск тестов
    with Pool(5) as p:
        p.map(run_test, accounts)
        

    
    
    
