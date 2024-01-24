from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait


def driver_init() -> WebDriver:
    service = webdriver.ChromeService()
    options = webdriver.ChromeOptions()
    options.add_argument('--window-size=1920,1080')  # type: ignore
    # options.add_argument('--headless')
    return webdriver.Chrome(options=options, service=service)


def waiting(driver: WebDriver) -> WebDriverWait[WebDriver]:
    return WebDriverWait(driver=driver, timeout=5)


def collect_tags(driver: WebDriver,
                 wait: WebDriverWait[WebDriver],
                 url: str,
                 tags: tuple[str, ...]
                 ) -> dict[str, list[WebElement]]:
    elms = {}
    driver.get(url)
    wait.until(ec.presence_of_element_located(('xpath', '//div[@class="card-body"]')))  # wait for the page rendering
    for item in tags:
        elms[item] = driver.find_elements('xpath', f'//{item}')
    return elms


def create_locators(elms: dict[str, list[WebElement]]) -> dict[str, list[tuple[str, str]]]:
    locators: dict[str, list[tuple[str, str]]] = {}
    for item in elms.items():
        tag, web_elms = item
        for web_elem in web_elms:
            if temp := web_elem.get_attribute('id'):
                value = (temp, 'id')
            elif temp := web_elem.get_attribute('class'):
                value = (temp, 'class')
            if temp:
                locators.setdefault(tag, []).append(('xpath', f'//{tag}[@{value[1]}="{value[0]}"]'))
    return locators


def check_tags(driver: WebDriver,
               wait: WebDriverWait[WebDriver],
               locators: dict[str, list[tuple[str, str]]]
               ) -> None:
    driver.refresh()
    wait.until(ec.presence_of_element_located(('xpath', '//div[@class="card-body"]')))  # wait for the page rendering
    for tag in locators.keys():
        for index, locator in enumerate(locators[tag], 1):
            try:
                driver.find_element(*locator)
                print(f'{index:<3}# {locator[-1]:<120} Found')
            except NoSuchElementException:
                print(f'{index:<3}# {locator[-1]:<117} NotFound')


def main() -> None:
    tags = ('div', 'a', 'p')
    url = 'https://hyperskill.org/tracks'
    with driver_init() as driver:
        wait = waiting(driver)
        elms = collect_tags(driver, wait, url, tags)
        locators = create_locators(elms)
        check_tags(driver, wait, locators)


if __name__ == '__main__':
    main()
