import requests
import json
import re

from database.db import add_product


def pars_product_links(links: list) -> None:
    for link in links:
        capabilities_list = []
        try:
            # Отправляем GET-запрос
            response = requests.get(link)
            product_id = link.split('/')[-2]

            # Проверяем, успешен ли запрос
            if response.status_code == 200:

                # Используем регулярное выражение для поиска данных, начиная с window.__PRELOADED_STATE__
                pattern = r'window\.__PRELOADED_STATE__\s*=\s*(\{.*?\});'
                match = re.search(pattern, response.text, re.DOTALL)

                if match:
                    preloaded_state = match.group(1)
                    preloaded_state_data = json.loads(preloaded_state)
                    try:
                        product_summary = preloaded_state_data['core2']['products']['productSummaries'][f'{product_id}']

                        # Проверка языковой поддержки
                        languages_supported = product_summary.get('languagesSupported', {}).get('ru-RU', {})
                        audio_ru = languages_supported.get('isAudioSupported', False)
                        interface_ru = languages_supported.get('isInterfaceSupported', False)
                        subtitles_ru = languages_supported.get('areSubtitlesSupported', False)

                        # Название игры
                        game_name = product_summary.get('title')

                        # Видео
                        cms_videos = product_summary.get('cmsVideos')
                        link_video = cms_videos[0]['url'] if cms_videos else None

                        # Скриншоты
                        link_screenshot = product_summary.get('images', {}).get('screenshots', [])
                        # Извлекаем только URL-адреса из списка словарей
                        link_screenshot_str = ','.join(
                            item['url'] for item in link_screenshot if isinstance(item, dict) and 'url' in item)

                        image_url = product_summary.get('images', {}).get('boxArt', {}).get('url')


                        # Описание
                        description = product_summary.get('description')
                        short_description = product_summary.get('shortDescription')

                        # Разработчик и издатель
                        developer_name = product_summary.get('developerName')
                        publisher_name = product_summary.get('publisherName')

                        # Категории и возможности
                        category = ','.join(product_summary.get('categories'))
                        capabilities = product_summary.get('capabilities')
                        if capabilities:
                            for item in capabilities:
                                capabilities_list.append(capabilities[item])
                        capabilities_list = ','.join(capabilities_list)

                        # Совместимость девайсов
                        device = ','.join(product_summary.get('availableOn'))

                        # Релиз
                        release_date = product_summary.get('releaseDate')

                        # Подписки и вес игры
                        pass_product_id = ','.join(product_summary.get('includedWithPassesProductIds'))
                        game_weight = product_summary.get('maxInstallSize')

                        # Цены и скидки
                        specific_prices = product_summary.get('specificPrices', {}).get('purchaseable')
                        if specific_prices:
                            original_price = specific_prices[0].get('msrp', 0)
                            discounted_price = specific_prices[0].get('listPrice', 0)
                            discounted_percentage = specific_prices[0].get('discountPercentage', 0)
                            end_date_sale = specific_prices[0].get('endDate')
                        else:
                            original_price = discounted_price = discounted_percentage = 0
                            end_date_sale = None

                        # Добавление продукта
                        add_product(
                            product_id=product_id,
                            url_product=link.replace('ru-RU', 'eu-EN'),
                            game_name=game_name,
                            end_date_sale=end_date_sale,
                            description=description,
                            short_description=short_description,
                            developer_name=developer_name,
                            publisher_name=publisher_name,
                            image_url=image_url,
                            device=device,
                            pass_product_id=pass_product_id,
                            release_date=release_date,
                            capabilities=capabilities_list,
                            category=category,
                            link_video=link_video,
                            link_screenshot=link_screenshot_str,
                            game_weight=game_weight,
                            audio_ru=audio_ru,
                            interface_ru=interface_ru,
                            subtitles_ru=subtitles_ru,
                        )
                        print(f'Найдена игра {game_name}')
                    except json.JSONDecodeError:
                        print(f"Ошибка парсинга JSON для продукта {product_id}")
                else:
                    print(f"Не удалось найти __PRELOADED_STATE__ в {link}")
        except Exception as e:
            print(f"Ошибка при обработке {link}: {e}")


# async def pars_product_links(links):
#     """
#     Асинхронно обрабатывает список ссылок.
#     """
#     async with aiohttp.ClientSession() as session:
#         tasks = [fetch_and_process(session, link.replace('en-US', 'ru-RU')) for link in links]
#         await asyncio.gather(*tasks)



