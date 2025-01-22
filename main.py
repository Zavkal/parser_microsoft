from database.db import start_db
from operations.parsing_links import open_page_and_scroll


def main():
    try:
        all_links_products = open_page_and_scroll()
    except Exception as e:
        print(f"Произошла ошибка при работе драйвера: {e}")

        try:
            all_links_products = open_page_and_scroll()
        except Exception as e:
            print(f"Произошла ошибка при работе драйвера 2 раз: {e}")

    finally:
        pass



if __name__ == '__main__':
    start_db()
    main()
