from time import sleep

from selenium import webdriver
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()

driver.get('https://www.rambler.ru/')
action = ActionChains(driver)
action.key_down(Keys.CONTROL) \
    .click(driver.find_element(By.XPATH, "//a[contains(text(), 'Рамблер')]")) \
    .key_up(Keys.CONTROL) \
    .perform()
driver.switch_to.window(driver.window_handles[-1])
sleep(10)
