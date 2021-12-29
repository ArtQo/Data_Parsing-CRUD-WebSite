from bs4 import BeautifulSoup
import requests

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
import time


# Для кнопки (Загрузить еще)

driver = webdriver.Chrome('')  # Здесь нужно указать путь к драйверу
wait = WebDriverWait(driver, 5)
action = ActionChains(driver)

driver.get("https://russian.rt.com/news")

# driver.execute_script("window.stop();")

i = 0

while i < 5:
    try:
        time.sleep(3)

        # element = driver.find_element(By.XPATH, "//a[@class='button__item button__item_listing']")
        # driver.execute_script("arguments[0].scrollIntoView(true);", element)

        driver.execute_script("window.scrollBy(0, 3500)")
        Load_More = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[@class='button__item button__item_listing']")))
        action.move_to_element(Load_More).click().perform()
        i += 1
        print(f"Clicked {i} time.")
    except:
        print("Reached End of the Page")
        break

page_source = driver.page_source

# Функция парсинга
def parse_news():
    URL = 'https://russian.rt.com/news'
    response = requests.get(URL)

    soup = BeautifulSoup(page_source, 'lxml')
    # soup = BeautifulSoup(response.content, 'html.parser')
    items = soup.findAll('div', class_='listing__card listing__card_all-news')
    news_m = []

    for item in items:
        news_m.append({
            'Article': item.findAll('a', class_='link link_color')[1].get_text(strip=True),
            'Pre_Body': item.findAll('a', class_='link link_color')[2].get_text(strip=True),
            'Link': 'https://russian.rt.com' + item.findAll('a', class_='link link_color')[2].get('href')
        })


    for news in news_m:
        data = {'Article':news["Article"], 'Pre_Body':news["Pre_Body"], 'Link':news["Link"], 'save':'Save'}

        requests.post('http://127.0.0.1:8080/news_data/create/', data=data)

parse_news()

driver.quit()
