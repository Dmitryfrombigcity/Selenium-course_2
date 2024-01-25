import os
from time import sleep

from fake_useragent import UserAgent
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

options = webdriver.ChromeOptions()
service = webdriver.ChromeService(executable_path=ChromeDriverManager().install())
options.add_argument('--window-size=1920,1080')
# options.add_argument('--ignore-certificate-errors')
options.add_argument('--disable-blink-features=AutomationControlled')
# options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_argument(f'--user-agent={UserAgent().random}')
options.add_argument('--headless')
# options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver=driver, timeout=10)
driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
    'source': '''
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_JSON;
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Object;
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Proxy;
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
'''
})
driver.get('https://www.ozon.ru')
driver.save_screenshot(f"{os.getcwd()}/before.png")
wait.until(ec.presence_of_element_located(('xpath', '//button[@id="reload-button"]'))).click()
driver.save_screenshot(f"{os.getcwd()}/after.png")
print(driver.title)
sleep(300)
