from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

driver.get('https://www.rambler.ru/')
driver.find_element(By.XPATH, "//a[contains(text(), 'В Роспотребнадзоре')]").click()
sleep(100)
