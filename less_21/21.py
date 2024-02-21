import os
from random import choice
from time import strftime, localtime, perf_counter, sleep

from selenium import webdriver
# import undetected_chromedriver as webdriver # just in case
from selenium.common import TimeoutException, WebDriverException
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait


class Captcha(WebDriverException):
    pass


def init_driver() -> WebDriver:
    options = webdriver.ChromeOptions()
    # service = webdriver.ChromeService(service_args=['--log-level=DEBUG'], log_output='log.txt')
    options.add_argument(f'--user-agent=Mozilla/5.0 (X11; Linux x86_64)'  # type: ignore
                         f' AppleWebKit/537.36 (KHTML, like Gecko)'
                         f' Chrome/121.0.0.0 Safari/537.36')
    options.add_argument('--disable-blink-features=AutomationControlled')  # type: ignore
    # options.add_argument('--headless=new')  # type: ignore
    options.add_argument('--window-size=1920,1080')  # type: ignore
    return webdriver.Chrome(options=options)


def select_country(
        driver: WebDriver,
        wait: WebDriverWait[WebDriver]
) -> None:
    deliver_to = (
        'xpath', '//div[@id="nav-global-location-slot"]'
    )
    countries_dropdown = (
        'xpath', '//select[@id="GLUXCountryList"]'
    )
    done_button = (
        'xpath', '//button[@class="a-button-text"]'
    )

    header = (
        'tag name', 'header'
    )
    try:
        wait.until(
            ec.element_to_be_clickable(deliver_to),
            message='deliver_to is not clickable'
        )
    except TimeoutException as err:
        make_screenshot(driver, err, 'homepage_error')
        print_err('homepage_error', err)
        driver.refresh()
    finally:
        header_state = wait.until(
            ec.presence_of_element_located(header)
        )
        wait.until(
            ec.element_to_be_clickable(deliver_to),
            message='deliver_to was not clickable twice'
        ).click()

    try:
        wait.until(
            ec.presence_of_element_located(countries_dropdown),
            message='countries_dropdown failed'
        )
    except TimeoutException as err:  # sometimes this happens
        make_screenshot(driver, err, 'deliver_to_click_err')
        print_err('deliver_to_click_err', err)

        driver.find_element(*deliver_to).click()
        wait.until(
            ec.presence_of_element_located(countries_dropdown),
            message='countries_dropdown failed twice'
        )

    dropdown = Select(driver.find_element(*countries_dropdown))
    dropdown.select_by_visible_text(choice(dropdown.options).text)
    wait.until(
        ec.presence_of_element_located(done_button),
        message='done_button is no present'
    ).click()
    start = perf_counter()
    print(header_state.id)
    wait.until(
        ec.staleness_of(header_state),
        message='header_state didn\'t change'
    )
    print(
        perf_counter() - start,
        driver.find_element(*header).id
    )


def waiting(driver: WebDriver) -> WebDriverWait[WebDriver]:
    return WebDriverWait(
        driver=driver,
        timeout=10,
        poll_frequency=0.5
    )


def collect_cart(
        driver: WebDriver,
        wait: WebDriverWait[WebDriver]
) -> None:
    hamburger_menu = (
        'xpath', '//*[@id="nav-hamburger-menu"]'
    )
    category_menu = (
        'xpath', '//a[@data-menu-id]'
    )
    hmenu_compressed_btn = (
        'xpath', '//a[@class = "hmenu-item hmenu-compressed-btn"]'
    )
    subcategory_menu = (
        'xpath', '//ul[contains(@class, "hmenu-visible")]//a'
    )
    search_results = (
        'xpath', '//div[contains(@class, "search-result")]//h2/a'
    )
    title = (
        'xpath', '//title'
    )

    # sleep(5)  # TODO: найти способ поменять на ожидание
    #  -> solved by wait.until(ec.staleness_of(header_state))

    action = ActionChains(driver)
    action \
        .move_to_element(driver.find_element(*hamburger_menu)) \
        .click(driver.find_element(*hamburger_menu)) \
        .perform()

    # driver.find_element(*hamburger_menu).click() -> doesn't work properly
    # script under hamburger_menu works twice
    # need to hover over hamburger_menu firstly and then click to solve it

    wait.until(
        ec.element_to_be_clickable(hmenu_compressed_btn),
        message='hmenu_compressed_btn is not clickable'
    ).click()
    category_lst = wait.until(
        ec.presence_of_all_elements_located(category_menu),
        message='category_menu is not present'
    )[3:25]

    # sometimes invalid URL -> maybe a longer delay is needed
    click_element(category_lst, 'categories', action)
    subcategory_lst = wait.until(
        ec.visibility_of_all_elements_located(subcategory_menu),
        message='subcategory_menu is not present'
    )[1:]
    click_element(subcategory_lst, 'subcategories', action)

    try:
        search_results_lst = wait.until(
            ec.visibility_of_all_elements_located(search_results),
            message='no_search-results'
        )
    except WebDriverException as err:
        make_screenshot(driver, err, 'no_search-results')
        print_err('no_search-results', err)
    else:
        choice(search_results_lst).click()
        wait.until(
            ec.presence_of_element_located(title)
        )
        print(
            f'######################'
            f'title = {driver.title}'
        )


def click_element(
        lst: list[WebElement],
        prefix: str,
        action: ActionChains
) -> None:
    lst_copy = lst[:]
    element = choice(lst_copy)
    print_items(lst_copy, prefix, element)
    action \
        .move_to_element(element) \
        .pause(3) \
        .click(element) \
        .pause(3) \
        .perform()


def print_items(
        lst_copy: list[WebElement],
        prefix: str,
        element: [WebElement]
) -> None:
    print(
        f'######################'
        f'{prefix}',
        *(item.get_attribute('text') for item in lst_copy),
        sep='\n'
    )
    print(
        f"######################"
        f"{prefix} = {element.get_attribute('text')}"
    )


def make_screenshot(
        driver: WebDriver,
        err: WebDriverException,
        description: str
) -> None:
    driver.get_screenshot_as_file(
        f'{os.getcwd()}/Errors/{strftime("%d.%m.%Y_%H:%M:%S", localtime())}> {description}> {err.msg}.png'
    )


def print_err(
        title: str,
        err: WebDriverException
) -> None:
    print(
        f'######################'
        f'{title}> {err.__class__.__name__}> {err.msg}',
        sep='\n'
    )


def check_captcha(
        driver: WebDriver,
        wait: WebDriverWait[WebDriver]
) -> None:
    h4 = (
        'tag name', 'h4'
    )
    try:  # TODO: Refactor it
        if wait.until(ec.presence_of_element_located(h4)).text == 'Enter the characters you see below':
            make_screenshot(driver, Captcha('it happened'), 'CAPTCHA')
            print_err('CAPTCHA', Captcha('it happened'))
            sleep(3)
            driver.refresh()
    except TimeoutException:
        pass


def main() -> None:
    url = 'https://www.amazon.com/'
    for _ in range(20):
        print('', f'######################Starting', sep='\n')
        with init_driver() as driver:
            wait = waiting(driver)
            driver.set_page_load_timeout(30)
            try:
                driver.get(url)
                check_captcha(driver, wait)
                select_country(driver, wait)
                collect_cart(driver, wait)
            except WebDriverException as err:
                make_screenshot(driver, err, 'critical_error')
                print_err('critical_error', err)


if __name__ == '__main__':
    main()
