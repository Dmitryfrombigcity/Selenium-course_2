from random import choice
from time import sleep


from selenium import webdriver
from selenium.common import TimeoutException, MoveTargetOutOfBoundsException, WebDriverException
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait


options = webdriver.ChromeOptions()
options.add_argument('--window-size=1980,800')
options.page_load_strategy = 'eager'
driver = webdriver.Chrome(options=options)
driver.get('https://demoqa.com/select-menu')
# dropdown = Select(driver.find_element('id', 'cars'))
# dropdown.select_by_visible_text('Opel')
# driver.find_element('xpath', '//*[text()="Interactions"]').click()
action = ActionChains(driver)


sleep(5)

action.click(driver.find_element('xpath', '//*[text()="Interactions"]')) \
    .send_keys(Keys.ARROW_DOWN) \
    .pause(1) \
    .click(driver.find_element('xpath', '//*[text()="Interactions"]')) \
    .perform()

# print(driver.find_element('xpath', '//*[text()="Interactions"]').is_enabled(),
#       driver.find_element('xpath', '//*[text()="Interactions"]').is_displayed()
#       )
# driver.find_element('xpath', '//*[text()="Interactions"]').click()
sleep(50)
