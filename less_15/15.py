# ./selenium-manager --browser chrome --driver-version 117 --debug --browser-version 118
import subprocess
from random import choices
from time import sleep

from selenium import webdriver

service = webdriver.ChromeService(executable_path='/home/me/.cache/selenium/chromedriver/linux64/117.0.5938.149/chromedriver',
                                  service_args=['--log-level=INFO'], log_output=subprocess.STDOUT)
options = webdriver.ChromeOptions()
options.page_load_strategy = 'eager'
options.add_argument('--window-size=1920,1080')
options.binary_location = '/home/me/.cache/selenium/chrome/linux64/118.0.5993.70/chrome'
# options.add_argument('--incognito')

driver = webdriver.Chrome(options=options, service=service)

driver.get('https://demoqa.com/selectable')
driver.find_element('xpath', '//a[@id="demo-tab-grid"]').click()
BUTTONS = driver.find_elements('xpath', '//div[@id="gridContainer"]//li')
while True:
    for button in choices(BUTTONS, k=3):
        state_button = button.get_attribute('class')
        button.click()
        assert state_button != button.get_attribute('class'), 'Error occurred'
    sleep(3)
