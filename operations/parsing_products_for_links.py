import requests
import json
import re


async def pars_product_links(links):
    for link in links:
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
                    # Извлекаем данные, которые начинаются с window.__PRELOADED_STATE__}
                    preloaded_state = match.group(1)
                    # Преобразуем строку в Python-словарь
                    try:
                        preloaded_state_data = json.loads(preloaded_state)
                        with open("preloaded_state.json", "w", encoding="utf-8") as json_file:
                            json.dump(preloaded_state_data, json_file, ensure_ascii=False, indent=4)

                        if preloaded_state_data['core2']['products']['productSummaries'][f'{product_id}']['languagesSupported']:
                            print(preloaded_state_data['core2']['products']['productSummaries'][f'{product_id}']['languagesSupported']['ru-RU']['isAudioSupported'])
                            print(preloaded_state_data['core2']['products']['productSummaries'][f'{product_id}']['languagesSupported']['ru-RU']['isInterfaceSupported'])
                            print(preloaded_state_data['core2']['products']['productSummaries'][f'{product_id}']['languagesSupported']['ru-RU']['areSubtitlesSupported'])
                        print(preloaded_state_data['core2']['products']['productSummaries'][f'{product_id}']['title']) #  Название
                        print(preloaded_state_data['core2']['products']['productSummaries'][f'{product_id}']['cmsVideos'][0]['url']) #  Видео
                        print(preloaded_state_data['core2']['products']['productSummaries'][f'{product_id}']['images']['screenshots']) #  Скрины
                        print(preloaded_state_data['core2']['products']['productSummaries'][f'{product_id}']['description']) #  Описание игры

                        print(preloaded_state_data['core2']['products']['productSummaries'][f'{product_id}']['shortDescription']) #  Короткое описание
                        print(preloaded_state_data['core2']['products']['productSummaries'][f'{product_id}'].get('developerName')) #  Разработчик
                        print(preloaded_state_data['core2']['products']['productSummaries'][f'{product_id}'].get('publisherName')) #  Публ название разработчика

                        print(preloaded_state_data['core2']['products']['productSummaries'][f'{product_id}']['includedWithPassesProductIds']) #  Подписки xbox
                        print(preloaded_state_data['core2']['products']['productSummaries'][f'{product_id}']['maxInstallSize']) #  Вес игры
                        print(preloaded_state_data['core2']['products']['productSummaries'][f'{product_id}']['categories']) #  Категории
                        print(preloaded_state_data['core2']['products']['productSummaries'][f'{product_id}']['specificPrices']['purchaseable'][0]['msrp']) # Ориг цена
                        print(preloaded_state_data['core2']['products']['productSummaries'][f'{product_id}']['specificPrices']['purchaseable'][0]['listPrice']) # Скид цена
                        print(preloaded_state_data['core2']['products']['productSummaries'][f'{product_id}']['specificPrices']['purchaseable'][0]['discountPercentage']) # % скидки
                        print(preloaded_state_data['core2']['products']['productSummaries'][f'{product_id}']['specificPrices']['purchaseable'][0]['endDate']) # День окончания скидки

                    except json.JSONDecodeError:
                        print("Ошибка при парсинге JSON данных.")
                else:
                    print("Не удалось найти данные с __PRELOADED_STATE__.")

            else:
                print(f"Ошибка: код ответа {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при выполнении запроса: {e}")

