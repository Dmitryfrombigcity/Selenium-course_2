from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

options = webdriver.ChromeOptions()
options.page_load_strategy = 'eager'
options.add_argument('--window-size=1920,780')

service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
# driver.maximize_window()

driver.get('https://demoqa.com/text-box')
full_name = driver.find_element('xpath', '//input[@id="userName"]')
email = driver.find_element('xpath', '//input[@id="userEmail"]')
current_address = driver.find_element('xpath', '//textarea[@id="currentAddress"]')
permanent_address = driver.find_element('xpath', '//textarea[@id="permanentAddress"]')

data = {
    full_name: 'Jon Snow',
    email: 'XXX@gmail.com',
    current_address: 'The Wall',
    permanent_address: 'Neverland'
}

for key, value in data.items():
    key.clear()
    key.send_keys(value)
    assert value in key.get_attribute('value')

sleep(3)
driver.find_element('xpath', '//button[@id="submit"]').click()
sleep(5)

driver.get('https://the-internet.herokuapp.com/status_codes')
data_lst = driver.find_elements('xpath', '//a[contains(@href, "status_code")]')
sleep(5)
for item in data_lst:
    item.click()
    sleep(3)
    driver.back()
sleep(5)
