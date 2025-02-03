from database.db import start_db
from operations.parsing_links import open_page_and_scroll
from operations.parsing_products_for_links import pars_product_links


def main():
    links = []
    try:
        all_links_products = open_page_and_scroll()
        links += all_links_products
    except Exception as e:
        print(f"Произошла ошибка при работе драйвера: {e}")

        try:
            all_links_products = open_page_and_scroll()
            links += all_links_products
        except Exception as e:
            print(f"Произошла ошибка при работе драйвера 2 раз: {e}")

    pars_product_links(links, country='ru-RU')


if __name__ == '__main__':
    start_db()
    main()
