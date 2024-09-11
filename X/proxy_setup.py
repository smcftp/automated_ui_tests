from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from fake_useragent import UserAgent

# def create_driver():
#     # Настройка прокси и user-agent
#     proxy = "123.123.123.123:8080"
#     user_agent = UserAgent().random

#     chrome_options = webdriver.ChromeOptions()
#     chrome_options.add_argument(f"--proxy-server={proxy}")
#     chrome_options.add_argument(f"user-agent={user_agent}")

#     # Создаем драйвер с настройками
#     # driver = webdriver.Chrome(service=Service('/path/to/chromedriver'), options=chrome_options)
#     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
#     return driver


def create_driver():
    try:
        # Настройка драйвера без прокси и пользовательского user-agent
        chrome_options = webdriver.ChromeOptions()
        
        # Создаем драйвер с минимальными настройками
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        
        return driver
    except Exception as e:
        print(f"Ошибка при создании драйвера: {e}")
        return None

