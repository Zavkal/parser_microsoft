from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from operations.parsing_links import open_page_and_scroll
from operations.parsing_price_products import pars_price


def pars_link_for_auto_pars():
    links = []
    options = Options()
    options.add_argument("--headless")  # Фоновый режим
    driver = webdriver.Chrome(options=options)
    try:
        driver.get("https://www.xbox.com/en-us/promotions/sales/sales-and-specials?xr=shellnav")

        # Ищем все кнопки с "SHOP MORE"
        buttons = driver.find_elements(By.XPATH, '//a[.//span[contains(text(), "SHOP MORE")]]')

        links = [button.get_attribute("href") for button in buttons if button.get_attribute("href")]
        links = [link.replace("xbox.com/", "xbox.com/en-US/") for link in links]
        driver.quit()
    except Exception as e:
        print(e)

    if len(links) > 0:
        all_links_products = open_page_and_scroll(links)
        links += all_links_products
        pars_price(links, country="en-US")




if __name__ == '__main__':
    pars_link_for_auto_pars()
