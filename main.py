from selenium import webdriver
import undetected_chromedriver as uc
import chromedriver_autoinstaller
from selenium.webdriver.common.by import By
import json

chromedriver_autoinstaller.install()
# Check if the current version of chromedriver exists
# and if it doesn't exist, download it automatically,
# then add chromedriver to path



class MainParser:
    def _url_request_creation(self, url, parameter):
        """Создание url запроса.
        :param url: [str] Ресурс.
        :param parameter: [list] Перечисление параметров поиска.
        """
        if parameter is not None:
            ad_param = list(map(str, parameter))
            return url + 'all?q=' + "+".join(ad_param)
        else:
            return url

    def __init__(self, url, param=None, page=5):
        """
        Инициализатор Экземпляра Класса MainParser.
        Метод инициализации парсинга .parser()
        :param url: [str] Ресурс.
        :param param: [list] Перечисление параметров поиска.
        :param page: [int] Количество страниц, которые будем парсить.
        """
        self.url = self._url_request_creation(url, param)
        self.page = page
        self.counter = 0

    def parser(self):
        """Запускает парсинг."""
        self._driver_loading()
        self._page_extraction()
        self._paginator()
        self.driver.quit()
        print('Работа сделана!')

    def _driver_loading(self):
        """Подключение драйвера Google Chrome."""
        self.driver = webdriver.Chrome()

    def _page_extraction(self):
        """Получение страницы."""
        self.driver.get(self.url)

    def _paginator(self):
        """Проход по страницам."""
        selector_button_next = rf'[data-marker="pagination-button/nextPage"]'
        next_page_button = self.driver.find_elements(By.CSS_SELECTOR, selector_button_next)
        # Итерация по страницам.
        while next_page_button and self.page > 0:
            self._parse_one_page()
            self.counter += 1
            self._save_page()
            print(fr'Обработано страниц: {self.counter}.')
            print(fr'Файл page_{self.counter}.json создан и записан.')
            try:
                next_page_button = self.driver.find_element(By.CSS_SELECTOR, selector_button_next)
                next_page_button.click()
            except Exception:
                self.page -= 1
                break

    def _parse_one_page(self):
        """Метод парсинга одной страницы."""
        selector_promotional_card = rf'[data-marker="item"]'
        advertisement_list = self.driver.find_elements(By.CSS_SELECTOR, selector_promotional_card)
        """Список рекламных объявлений."""
        self.data_ads = []
        # Итерация по объявлениям на одной странице.
        for single_ad in advertisement_list:

            selector_ad_name = fr'[itemprop="name"]'
            tmp_ad_name = single_ad.find_element(By.CSS_SELECTOR, selector_ad_name)
            ad_name = tmp_ad_name.text
            """Название объявления."""

            selector_ad_url = fr'[data-marker="item-title"]'
            tmp_ad_url = single_ad.find_element(By.CSS_SELECTOR, selector_ad_url)
            ad_url = tmp_ad_url.get_attribute('href')
            """url объявления."""

            selector_ad_text = fr'[class^=iva-item-descriptionStep-] > p'
            tmp_ad_text = single_ad.find_element(By.CSS_SELECTOR, selector_ad_text)
            ad_text = tmp_ad_text.text
            """Краткий текст объявления."""

            selector_ad_price = fr'[itemprop="price"]'
            tmp_ad_price = single_ad.find_element(By.CSS_SELECTOR, selector_ad_price)
            ad_price = tmp_ad_price.get_attribute('content')
            """Цена товара."""

            if ad_price == '0':
                tmp_dict_ad = {
                    'Имя объявления: ': ad_name,
                    'url объявления: ': ad_url,
                    'Краткий текст объявления: ': ad_text,
                    'Цена товара: ': ad_price,
                }
                self.data_ads.append(tmp_dict_ad)

    def _save_page(self):
        """Метод сохранения результата по 1 странице"""
        with open(fr'data_parse/page_{self.counter}.json', 'w', encoding='utf-8') as json_file:
            json.dump(self.data_ads, json_file, indent=4,  ensure_ascii=False)


if __name__ == '__main__':
    url = 'https://www.avito.ru/'
    MainParser(url, ['бесплатно', 'телевизор'], 10).parser()
