import re
import time
from seleniumbase import Driver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

from database.db import update_audio_product, update_interface_product, update_subtitles_product, \
    update_category_product, update_capabilities_product, add_product, update_description_product, \
    update_game_name_product


def parser_product(product_links):
    counter = 0
    driver = Driver()
    for link in product_links:

        #  Ставим перезапуск браузера для стабильности (Выбивало ошибку) - возможно из-за хром драйвера.
        if counter % 100 == 0:
            driver.quit()
            time.sleep(5)
            driver = Driver()
        product_id = link.split('/')[-2]
        add_product(url_product=link)
        link = link.replace("en-US", "ru-RU")
        driver.open(link)

        #  Проверяем наличие игры на РФ сайте
        try:
            driver.find_element(By.XPATH, '//h2[text()="К сожалению, запрошенная страница не найдена."]')
            link = link.replace("ru-RU", "en-US")
            driver.open(link)
        except:
            pass

        #  Находим категории игры
        container = driver.find_element(By.XPATH,
'//div[@class="typography-module__xdsSubTitle1___N02-X ProductInfoLine-module__productInfoLine___Jw2cv" and @data-testid="ProductInfoLinePublisherName"]')

        html_category = container.get_attribute('outerHTML')
        soup = BeautifulSoup(html_category, 'html.parser')
        categories_span = soup.find('span', class_='ProductInfoLine-module__textInfo___jOZ96')
        if categories_span:
            categories_text = categories_span.text.strip()
            categories = categories_text.split('•')  # Разделяем текст по знаку "•"
            categories = [category.strip() for category in categories if category.strip()]  # Убираем лишние пробелы

            update_category_product(','.join(categories[1:-1]), product_id)

        #  Находим название игры
        try:
            game_title_element = driver.find_element(
                By.XPATH, '//h1[@data-testid="ProductDetailsHeaderProductTitle"]'
            )
            game_name = game_title_element.text
            update_game_name_product(game_name, product_id)
        except Exception as e:
            pass

        #  Находим доп опции игры (Возможности)
        container = driver.find_elements(By.XPATH, '//ul[contains(@class, "FeaturesList-module__wrapper___")]')
        if len(container) == 2:
            html_capabilities = container[1].get_attribute('outerHTML')
            items = ','.join(list(filter(lambda x: x != '', re.findall(r'>(.*?)<', html_capabilities))))
            update_capabilities_product(items, product_id)

        #  Находим описание игры
        try:
            description_element = driver.find_element(
                By.XPATH, '//div[contains(@class, "Description-module__descriptionContainer___hlY8t")]/p'
            )
            description_text = description_element.text
            update_description_product(description_text, product_id)
        except Exception as e:
            pass

        #  Если ссылка есть на русском, находим озвучку
        try:
            driver.find_element(By.XPATH, '//button[text()="ЕЩЕ"]').click()
            try:
                driver.find_element(By.XPATH, '//h2[text()="Поддерживаемые языки"]')
                try:
                    driver.find_elements(By.XPATH, '//svg[@aria-label="АУДИО на Русский поддерживается"]')
                    update_audio_product(True, product_id)
                except Exception as e:
                    pass
                try:
                    driver.find_elements(By.XPATH, '//svg[@aria-label="ИНТЕРФЕЙС на Русский поддерживается"]')
                    update_interface_product(True, product_id)
                except Exception as e:
                    pass
                try:
                    driver.find_elements(By.XPATH, '//svg[@aria-label="СУБТИТРЫ на Русский поддерживается"]')
                    update_subtitles_product(True, product_id)
                except Exception as e:
                    pass

            except Exception as e:
                pass
        except Exception as e:
            pass
        counter += 1

    driver.quit()

