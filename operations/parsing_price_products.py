import json
import re

import requests


def pars_price(links: list, country: str) -> None:
    for link in links:
        product_id = link.split(',')[-2]
        link = link.replace('en-US', country)
        try:
            response = requests.get(link)

            if response.status_code == 200:

                # Используем регулярное выражение для поиска данных, начиная с window.__PRELOADED_STATE__
                pattern = r'window\.__PRELOADED_STATE__\s*=\s*(\{.*?\});'
                match = re.search(pattern, response.text, re.DOTALL)

                if match:
                    preloaded_state = match.group(1)
                    preloaded_state_data = json.loads(preloaded_state)
                    try:
                        # Цены и скидки
                        specific_prices = preloaded_state_data['core2']['products']['productSummaries'][f'{product_id}'].get('specificPrices', {}).get('purchaseable')
                        if len(specific_prices) > 0:
                            original_price = specific_prices[0].get('msrp', 0)
                            discounted_price = specific_prices[0].get('listPrice', 0)
                            discounted_percentage = specific_prices[0].get('discountPercentage', 0)
                            end_date_sale = specific_prices[0].get('endDate')
                        else:
                            original_price = discounted_price = discounted_percentage = 0
                            end_date_sale = None

                    except Exception as e:
                        print(f"Ошибка парсинга цены для продукта {product_id}")
        except Exception as e:
            print(f"Ошибка при обработке {link}: {e}")
