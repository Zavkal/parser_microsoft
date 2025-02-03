import re
import time
from seleniumbase import Driver
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from config import main_game_list


def open_page_and_scroll(links: list = main_game_list):
    all_link_products = []
    for link in links:
        driver = Driver()
        driver.open(link)
        time.sleep(2)  # Небольшая задержка для загрузки страницы
        while True:
            try:
                load_more_button = WebDriverWait(driver, 20).until(
                    EC.visibility_of_element_located((By.XPATH, '//button[contains(@aria-label, "Load more")]'))
                )
                if load_more_button.is_displayed():
                    load_more_button.click()  # Кликнуть на кнопку
                    time.sleep(2)  # Ожидание для загрузки новых элементов
                else:
                    print("Кнопка 'Load more' не отображается.")
                    break
            except NoSuchElementException:
                print("Кнопка 'Load more' больше не доступна.")
                break
            except TimeoutException:
                print("Таймаут при ожидании кнопки 'Load more'.")
                break

        all_link_products += get_product_links(driver)
        driver.quit()

    return list(set(all_link_products))


def get_product_links(driver):
    product_containers = driver.find_elements(By.XPATH, '//div[contains(@class,"ProductCard-module__cardWrapper___")]')
    links = []
    try:
        for container in product_containers:
            try:
                html_content = container.get_attribute('outerHTML')
                link = re.findall(r'href=["\'](.*?)["\']', html_content)
                link = ''.join(link)
                links.append(link)
            except Exception as e:
                print(f"Ошибка при извлечении ссылки: {e}")
        driver.quit()
        return links
    except Exception as e:
        print(f'ФАТАЛЬНАЯ ОШИБКА РАБОТЫ {e}')
        driver.quit()


def clear_price_symbol(text: str):
    text = text.replace("+", '')
    text = text.replace("$", '')
    text = text.replace('Free', '0')
    text = text.replace("-", '')
    text = text.replace('%', '')

    return float(text)




