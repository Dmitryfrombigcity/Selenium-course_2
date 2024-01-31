from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

service = webdriver.ChromeService()
options = webdriver.ChromeOptions()
options.add_argument('--window-size=1980,1080')  # type: ignore
options.page_load_strategy = 'eager'

driver = webdriver.Chrome(options=options, service=service)
wait = WebDriverWait(driver=driver, timeout=15)
driver.get('https://demoqa.com/nestedframes')
driver.switch_to.frame(0)
print(driver.find_element('tag name', 'html').text)
driver.switch_to.default_content()
