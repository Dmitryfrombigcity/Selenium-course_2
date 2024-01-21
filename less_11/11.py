from time import sleep

from selenium import webdriver
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

service = webdriver.ChromeService(executable_path=ChromeDriverManager().install())
options = webdriver.ChromeOptions()
options.add_argument('--window-size=1980,1080')  # type: ignore

driver = webdriver.Chrome(options=options, service=service)
wait = WebDriverWait(driver=driver, timeout=15)
driver.get('https://chercher.tech/practice/explicit-wait-sample-selenium-webdriver')

CHANGE_TEXT_BUTTON = ('xpath', '//button[@id="populate-text"]')
CHANGE_TEXT_FIELD = ('xpath', '//h2[@class="target-text"]')
DISPLAY_AFTER_SECS = ('xpath', '//button[@id="display-other-button"]')
HIDDEN_BUTTON = ('xpath', '//button[@id="hidden"]')
ENABLE_AFTER_SECS = ('xpath', '//button[@id="enable-button"]')
DISABLED_BUTTON = ('xpath', '//button[@id="disable"]')
CLICK_TO_OPEN_ALERT = ('xpath', '//button[@id="alert"]')

driver.find_element(*CHANGE_TEXT_BUTTON).click()
wait.until(EC.text_to_be_present_in_element(CHANGE_TEXT_FIELD, 'Selenium Webdriver'))
# wait.until(lambda d: driver.find_element(*CHANGE_TEXT_FIELD).text == 'Selenium Webdriver')
assert driver.find_element(*CHANGE_TEXT_FIELD).text == 'Selenium Webdriver'

driver.find_element(*DISPLAY_AFTER_SECS).click()
wait.until(EC.visibility_of_element_located(HIDDEN_BUTTON))
# wait.until(lambda d: driver.find_element(*HIDDEN_BUTTON).is_displayed())
assert driver.find_element(*HIDDEN_BUTTON).is_displayed()

driver.find_element(*ENABLE_AFTER_SECS).click()
wait.until(EC.element_to_be_clickable(DISABLED_BUTTON))
# wait.until(lambda d: driver.find_element(*DISABLED_BUTTON).is_enabled())
assert driver.find_element(*DISABLED_BUTTON).is_enabled()

driver.find_element(*CLICK_TO_OPEN_ALERT).click()
alert = wait.until(EC.alert_is_present())
if alert:
    alert.accept()
try:
    assert driver.switch_to.alert
except NoAlertPresentException:
    pass
else:
    print("Not good")

sleep(5)
