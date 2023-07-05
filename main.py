from selenium import webdriver
import undetected_chromedriver as uc
import chromedriver_autoinstaller

chromedriver_autoinstaller.install()
# Check if the current version of chromedriver exists
# and if it doesn't exist, download it automatically,
# then add chromedriver to path

driver = webdriver.Chrome()
driver.get("https://www.avito.ru")

