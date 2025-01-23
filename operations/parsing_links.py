import re
import time
from seleniumbase import Driver
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from config import main_game_list


def open_page_and_scroll():
    all_link_products = []
    for link in main_game_list:
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
                # product_id = link.split('/')[-2]
                # add_product(url_product=link, product_id=product_id)
                # try:
                #     price = clear_price_symbol(container.find_element(By.CSS_SELECTOR, '[class*="Price-module__originalPrice___"]').text)
                #     discounted_price = clear_price_symbol(container.find_element(By.CSS_SELECTOR, '.Price-module__boldText___1i2Li').text)
                #     percentage = clear_price_symbol(container.find_element(By.CSS_SELECTOR, '[class*="ProductCard-module__discountTag"]').text)
                #     update_price_product_en_us(original_price=price,
                #                                product_id=product_id,
                #                                discounted_price=discounted_price,
                #                                discounted_percentage=percentage)
                # except:
                #     price = clear_price_symbol(container.find_element(By.CSS_SELECTOR, '.Price-module__boldText___1i2Li').text)
                #     update_price_product_en_us(original_price=price,
                #                                product_id=product_id,
                #                                discounted_price=price,
                #                                discounted_percentage=0)
            except Exception as e:
                print(f"Ошибка при извлечении ссылки: {e}")
        driver.quit()
        return links
    except Exception as e:
        print(f'ФАТАЛЬНАЯ ОШИБКА РАБОТЫ {e}')
        driver.quit()

# def save_links_to_file(links, filename):
#     with open(filename, 'w') as file:
#         for link in links:
#             file.write(link + '\n')
#     print(f"Ссылки сохранены в файл {filename}")


# def create_unique_link_set(file_list):
#     unique_links = set()  # Множество для хранения уникальных ссылок
#     for file_name in file_list:
#         try:
#             with open(file_name, 'r', encoding='utf-8') as file:
#                 for line in file:
#                     link = line.strip()  # Убираем лишние пробелы и переносы строк
#                     if link:  # Проверяем, что строка не пустая
#                         unique_links.add(link)
#         except FileNotFoundError:
#             print(f"Файл {file_name} не найден.")
#         except Exception as e:
#             print(f"Ошибка при обработке файла {file_name}: {e}")
#
#     return list(unique_links)


def clear_price_symbol(text: str):
    text = text.replace("+", '')
    text = text.replace("$", '')
    text = text.replace('Free', '0')
    text = text.replace("-", '')
    text = text.replace('%', '')

    return float(text)




