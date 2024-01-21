import os
from time import sleep

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

options = webdriver.ChromeOptions()
options.page_load_strategy = 'eager'
prefs = {
    "download.default_directory": f"{os.getcwd()}/Downloads/"
}
options.add_experimental_option('prefs', prefs)
options.add_argument('--window-size=1980,800')
service = webdriver.ChromeService(executable_path=ChromeDriverManager().install())

driver = webdriver.Chrome(service=service, options=options)
driver.get('https://demoqa.com/upload-download')
ref = driver.find_element('xpath', '//input[@id="uploadFile"]')
ref.send_keys(f'{os.getcwd()}/Uploads/funny_doctors.png')
sleep(5)

driver.get('https://the-internet.herokuapp.com/download')
ref_lst = driver.find_elements('xpath', '//a')
for ref in ref_lst[1:-1]:
    print(f'Downloading:  {ref.get_attribute("href")}')
    ref.click()
sleep(5)
