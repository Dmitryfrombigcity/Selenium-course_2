from time import sleep

from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.support.select import Select

user_agent = UserAgent(browsers="chrome")
options = webdriver.ChromeOptions()
service = webdriver.ChromeService()
options.add_argument('window-size=1920,1080')
options.add_argument(f'--user-agent=f"{user_agent.random}"')
options.page_load_strategy = 'eager'

with (webdriver.Chrome(options=options, service=service) as driver):
    driver.get('https://the-internet.herokuapp.com/dropdown')
    first_page = driver.current_window_handle
    dropdown = Select(driver.find_element('xpath', '//select[@id="dropdown"]'))
    dropdown_options = dropdown.options
    print(*(item.get_attribute('value') for item in dropdown_options), sep='\n')
    print(*(item.text for item in dropdown_options), sep='\n')
    dropdown.select_by_index(2)
    sleep(1)

    driver.switch_to.new_window('tab')
    driver.get('https://the-internet.herokuapp.com/key_presses')
    driver.find_element('xpath', '//input[@id="target"]'
                        ).send_keys("Hi, it's my", f"{Keys.BACKSPACE}e", f"{Keys.CONTROL} A")
    # driver.find_element('xpath', '//input[@id="target"]'
    #                     ).send_keys(f"Hi, it's my{Keys.BACKSPACE}e {Keys.CONTROL} A")
    sleep(1)

    driver.switch_to.new_window('window')
    driver.get('https://demoqa.com/select-menu')
    driver.find_element('xpath', '//input[@id="react-select-3-input"]').send_keys(f'Prof.{Keys.ENTER}')
    sleep(1)

    # setTimeout(function() { debugger; }, 5000); - включит отложенный старт дебаг-режима в devtools.
    driver.find_element('xpath', "//div[@id='withOptGroup']").click()
    driver.find_element('xpath', "//div[@id='withOptGroup']//div[text()='A root option']").click()
    sleep(1)

    driver.find_element("xpath", "//div[@id='withOptGroup']").click()


    def choose_dropdown_element_by_text(text):
        elements = driver.find_elements("xpath",
                                        "//div[@id='withOptGroup']//div[contains(@id, 'react-select')]"
                                        )
        for element in elements:
            if text in element.text:
                return element


    choose_dropdown_element_by_text("Another root option").click()
    sleep(1)

    driver.find_element('xpath', '//div[contains(text(), "Select...")]').click()
    driver.find_element('xpath', '//div[contains(text(), "Green")]').click()
    driver.find_element('xpath', '//input[@id="react-select-4-input"]').send_keys(f'b{Keys.TAB}{Keys.ESCAPE}')
    sleep(1)

    driver.switch_to.window(first_page)
    sleep(1)
