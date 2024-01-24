from selenium import webdriver

options = webdriver.ChromeOptions()
options.add_argument('--window-size=1920,1080')

driver = webdriver.Chrome(options=options)
driver.get('https://www.rambler.ru')
print(f'{driver.title = }')

driver.get('https://google.com')
print(f'{driver.title = }')

driver.back()
assert 'https://www.rambler.ru/' == driver.current_url, f'{driver.current_url = }'

driver.refresh()
print(f'{driver.current_url = }')

driver.forward()
assert 'https://www.google.com/' == driver.current_url, f'{driver.current_url = }'
