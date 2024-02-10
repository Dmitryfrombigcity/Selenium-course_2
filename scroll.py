from time import sleep

from selenium import webdriver
from selenium.webdriver import ActionChains, Keys

options = webdriver.ChromeOptions()
options.add_argument('--window-size=1980,800')
options.page_load_strategy = 'eager'
driver = webdriver.Chrome(options=options)
driver.get('https://demoqa.com/select-menu')
action = ActionChains(driver)

action \
    .scroll_to_element(driver.find_element('xpath', '//*[text()="Interactions"]')) \
    .send_keys(Keys.ARROW_DOWN) \
    .pause(1) \
    .click(driver.find_element('xpath', '//*[text()="Interactions"]')) \
    .perform()

sleep(10)
