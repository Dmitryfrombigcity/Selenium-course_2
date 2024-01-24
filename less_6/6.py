from time import sleep

from selenium import webdriver

options = webdriver.ChromeOptions()
options.add_argument('--window-size=1920,1080')

driver = webdriver.Chrome(options=options)
driver.get('https://testautomationpractice.blogspot.com/')

driver.find_element('xpath', '//img[@class="wikipedia-icon"]').click()
driver.switch_to.window(driver.window_handles[1])
sleep(3)

driver.switch_to.window(driver.window_handles[0])
driver.find_element('xpath', '//input[@id="Wikipedia1_wikipedia-search-input"]').send_keys('OK')
driver.find_element('xpath', '//input[@class="wikipedia-search-button"]').click()
sleep(3)
