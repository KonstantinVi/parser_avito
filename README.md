AVITO парсер | v.00.01 \
Данный Проект создаётся исключительно в образовательных целях.
---
### Development stack:
+ Python
+ Selenium
  + Библиотека undetected_chromedriver
    https://github.com/ultrafunkamsterdam/undetected-chromedriver
  + Библиотека chromedriver-autoinstaller 
    https://github.com/yeongbin-jo/python-chromedriver-autoinstaller
+ ChromeDriver\
  https://chromedriver.chromium.org/downloads
+ Библиотека webdriver_manager 
---

#### Пример запроса:
url = 'https://www.avito.ru/'  
MainParser(url, ['бесплатно', 'телевизор'], 10).parser()
