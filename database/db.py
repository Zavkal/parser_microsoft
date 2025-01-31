import os
import sqlite3
from datetime import datetime, timedelta, timezone

base_dir = os.path.dirname(os.path.abspath(__file__))

db_path = os.path.join(base_dir, '../db.db')

conn = sqlite3.connect(db_path)
cur = conn.cursor()


def start_db():
    """
    ru-RU en-US es-AR tr-TR en-NG uk-UA en-IN \n -- Полное описание бд при создании
    *1. Уникальный id товара на сайте, \n
    *2. Ссылка на товар, \n
    *3. Название игры, \n
    *4. Окончание скидки, \n
    *5. Поддерживаемые платформы, \n
    *6. Описание, \n
    *7. Короткое описание, \n
    *8. Разработчик, \n
    *9. Публичное название разработчика, \n
    *10. Ссылка на постер товара, \n
    *11. Гейм пассы, \n
    *12. Дата выхода игры, \n
    *13. Возможности игры, \n
    *14. Категории, \n
    *15. Ссылка на трейлер, \n
    *16. Ссылка на скриншоты, \n
    *17. Вес игры
    *18. Русс озвучка, \n
    *19. Русс интерфейс, \n
    *20. Русс субтитры, \n
    """

    cur.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id TEXT,
        url_product TEXT,
        game_name TEXT,
        end_date_sale TEXT,
        device TEXT,
        description TEXT,
        short_description TEXT,
        developer_name TEXT,
        publisher_name TEXT,
        image_url TEXT,
        pass_product_id TEXT,
        release_date TEXT,
        capabilities TEXT,
        category TEXT,
        link_video TEXT,
        link_screenshot TEXT,
        game_weight INTEGER,
        audio_ru INTEGER,
        interface_ru INTEGER,
        subtitles_ru INTEGER
    );
    ''')

    cur.execute('''
    CREATE TABLE IF NOT EXISTS "ru-RU" (
        product_id TEXT,
        original_price REAL,
        discounted_price REAL,
        discounted_percentage REAL,
        FOREIGN KEY(product_id) REFERENCES products(product_id)
    );
    ''')

    cur.execute('''
    CREATE TABLE IF NOT EXISTS "en-US" (
        product_id TEXT,
        original_price REAL,
        discounted_price REAL,
        discounted_percentage REAL,
        FOREIGN KEY(product_id) REFERENCES products(product_id)
    );
    ''')

    cur.execute('''
    CREATE TABLE IF NOT EXISTS "es-AR" (
        product_id TEXT,
        original_price REAL,
        discounted_price REAL,
        discounted_percentage REAL,
        FOREIGN KEY(product_id) REFERENCES products(product_id)
    );
    ''')

    cur.execute('''
    CREATE TABLE IF NOT EXISTS "tr-TR" (
        product_id TEXT,
        original_price REAL,
        discounted_price REAL,
        discounted_percentage REAL,
        FOREIGN KEY(product_id) REFERENCES products(product_id)
    );
    ''')

    cur.execute('''
    CREATE TABLE IF NOT EXISTS "en-NG" (
        product_id TEXT,
        original_price REAL,
        discounted_price REAL,
        discounted_percentage REAL,
        FOREIGN KEY(product_id) REFERENCES products(product_id)
    );
    ''')

    cur.execute('''
    CREATE TABLE IF NOT EXISTS "uk-UA" (
        product_id TEXT,
        original_price REAL,
        discounted_price REAL,
        discounted_percentage REAL,
        FOREIGN KEY(product_id) REFERENCES products(product_id)
    );
    ''')

    cur.execute('''
    CREATE TABLE IF NOT EXISTS "en-IN" (
        product_id TEXT,
        original_price REAL,
        discounted_price REAL,
        discounted_percentage REAL,
        FOREIGN KEY(product_id) REFERENCES products(product_id)
    );
    ''')

    conn.commit()


def add_product(
        product_id: str,
        url_product: str,
        game_name: str = None,
        end_date_sale: str = None,
        device: str = None,
        description: str = None,
        short_description: str = None,
        developer_name: str = None,
        publisher_name: str = None,
        image_url: str = None,
        pass_product_id: str = None,
        release_date: str = None,
        capabilities: str = None,
        category: str = None,
        link_video: str = None,
        link_screenshot: str = None,
        game_weight: str = None,
        audio_ru: bool = False,
        interface_ru: bool = False,
        subtitles_ru: bool = False):
    cur.execute("SELECT COUNT(*) FROM products WHERE product_id = ?", (product_id,))
    exists = cur.fetchone()[0] > 0

    if not exists:
        # Если записи нет, создаем новую
        cur.execute(
            '''INSERT INTO products (product_id, url_product, game_name, end_date_sale, device, description, short_description,
            developer_name, publisher_name, image_url, pass_product_id, release_date, capabilities, category, link_video, link_screenshot,
             game_weight, audio_ru, interface_ru, subtitles_ru) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            (product_id, url_product, game_name, end_date_sale, device, description, short_description,
             developer_name, publisher_name, image_url, pass_product_id, release_date, capabilities, category,
             link_video, link_screenshot, game_weight, audio_ru, interface_ru, subtitles_ru)
        )

    else:
        pass

    conn.commit()


def update_audio_product(audio: bool, product_id: str):
    cur.execute(
        'UPDATE products SET audio_ru = ? WHERE product_id = ?', (audio, product_id)
    )
    conn.commit()


def update_interface_product(interface: bool, product_id: str):
    cur.execute(
        'UPDATE products SET interface_ru = ? WHERE product_id = ?', (interface, product_id)
    )
    conn.commit()


def update_subtitles_product(subtitles: bool, product_id: str):
    cur.execute(
        'UPDATE poducts SET subtitles_ru = ? WHERE product_id = ?', (subtitles, product_id)
    )
    conn.commit()


def update_capabilities_product(capabilities: str, product_id: str):
    cur.execute('UPDATE products SET capabilities = ? WHERE product_id = ?', (capabilities, product_id)
                )
    conn.commit()


def update_category_product(category: str, product_id: str):
    cur.execute('UPDATE products SET category = ? WHERE product_id = ?', (category, product_id)
                )
    conn.commit()


def update_description_product(description: str, product_id: str):
    cur.execute('UPDATE products SET description = ? WHERE product_id = ?', (description, product_id)
                )
    conn.commit()


def update_game_name_product(game_name: str, product_id: str):
    cur.execute('UPDATE products SET game_name = ? WHERE product_id = ?', (game_name, product_id)
                )
    conn.commit()


def update_link_screenshots_product(link_screenshot: str, product_id: str):
    pass


def update_price_products():
    pass


def get_all_url_products():
    cur.execute('SELECT url_product FROM products')
    result = []
    for url in cur.fetchall():
        result.append(url[0])

    return result


def get_all_sale_product(days=7):
        current_date = datetime.now(timezone.utc)
        future_date = current_date + timedelta(days=days)

        # Запрос для выборки данных
        query = 'SELECT url_product FROM products WHERE end_date_sale BETWEEN ? AND ?;'

        # Выполняем запрос с подстановкой дат
        cur.execute(query, (current_date.strftime("%Y-%m-%d"), future_date.strftime("%Y-%m-%d")))

        result = []
        for url in cur.fetchall():
            result.append(url[0])

        return result





#  -------------------------------------------------------------------------------------------Работа с ценами и странами


def update_price_product_en_us(
        product_id: str,
        original_price: float,
        discounted_price: float = 0,
        discounted_percentage: float = 0):

    cur.execute('SELECT COUNT(*) FROM "en-US" WHERE product_id = ?', (product_id,))
    exists = cur.fetchone()[0] > 0

    if not exists:
        # Если записи нет, создаем новую
        cur.execute('INSERT INTO "en-US" (product_id, original_price, discounted_price, discounted_percentage)'
                    ' VALUES (?, ?, ?, ?)',
                    (product_id, original_price, discounted_price, discounted_percentage)
                    )
    else:
        cur.execute(
            'UPDATE "en-US" SET original_price = ?, discounted_price = ?, discounted_percentage = ? WHERE product_id = ?',
            (original_price, discounted_price, discounted_percentage, product_id)
            )

        conn.commit()











































