import json
from pathlib import Path
from random import choice
from time import strftime, localtime, sleep

from selenium import webdriver
# import undetected_chromedriver as webdriver # just in case
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

from locators import Locators


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
    options.add_experimental_option("excludeSwitches", ['enable-automation'])  # type: ignore
    return webdriver.Chrome(options=options)


def select_country(
        driver: WebDriver,
        wait: WebDriverWait[WebDriver]
) -> None:
    try:
        wait.until(
            ec.element_to_be_clickable(Locators.deliver_to),
            message='deliver_to is not clickable'
        )
    except TimeoutException as err:
        make_screenshot(driver, err, 'homepage_error')
        print_err('homepage_error', err)
        driver.refresh()
    finally:
        header_state = wait.until(
            ec.presence_of_element_located(Locators.header)
        )
        wait.until(
            ec.element_to_be_clickable(Locators.deliver_to),
            message='deliver_to was not clickable twice'
        ).click()

    try:
        wait.until(
            ec.presence_of_element_located(Locators.countries_dropdown),
            message='countries_dropdown failed'
        )
    except TimeoutException as err:  # sometimes this happens
        make_screenshot(driver, err, 'deliver_to_click_err')
        print_err('deliver_to_click_err', err)

        driver.find_element(*Locators.deliver_to).click()
        wait.until(
            ec.presence_of_element_located(Locators.countries_dropdown),
            message='countries_dropdown failed twice'
        )

    dropdown = Select(driver.find_element(*Locators.countries_dropdown))
    dropdown.select_by_visible_text(choice(dropdown.options).text)
    wait.until(
        ec.presence_of_element_located(Locators.done_button),
        message='done_button is no present'
    ).click()
    wait.until(
        ec.staleness_of(header_state),
        message='header_state didn\'t change'
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
    # sleep(5)  # найти способ поменять на ожидание
    #  -> solved by wait.until(ec.staleness_of(header_state))

    action = ActionChains(driver)
    action \
        .move_to_element(driver.find_element(*Locators.hamburger_menu)) \
        .click(driver.find_element(*Locators.hamburger_menu)) \
        .perform()

    # driver.find_element(*hamburger_menu).click() -> doesn't work properly
    # script under hamburger_menu works twice
    # need to hover over hamburger_menu firstly and then click to solve it

    try:
        wait.until(
            ec.element_to_be_clickable(Locators.hmenu_compressed_btn),
            message='hmenu_compressed_btn is not clickable'
        ).click()
        category_lst = wait.until(
            ec.presence_of_all_elements_located(Locators.menu),
            message='category_menu is not present'
        )[3:25]
        # sometimes invalid URL -> maybe a longer delay is needed
        click_element(category_lst, 'categor', action)
        subcategory_lst = wait.until(
            ec.visibility_of_all_elements_located(Locators.menu),
            message='subcategory_menu is not present'
        )[1:]
        click_element(subcategory_lst, 'subcategor', action)
    except TimeoutException as err:
        make_screenshot(driver, err, 'category/subcategory')
        print_err('category/subcategory', err)
        driver.refresh()
    else:
        try:
            search_results_lst = wait.until(
                ec.visibility_of_all_elements_located(Locators.search_results),
                message='no_search-results'
            )
        except WebDriverException as err:
            make_screenshot(driver, err, 'no_search-results')
            print_err('no_search-results', err)
            driver.refresh()
        else:
            choice(search_results_lst).click()
            add_good(driver, wait)


def add_good(
        driver: WebDriver,
        wait: WebDriverWait[WebDriver]
) -> None:
    wait.until(
        ec.presence_of_element_located(Locators.title)
    )
    try:
        print(
            f'######################'
            f'title = {driver.title}'
        )
        wait.until(
            ec.element_to_be_clickable(Locators.add_to_cart),
            message='good is unavailable'
        ).click()

    except TimeoutException as err:
        make_screenshot(driver, err, 'add_to_cart is not selectable')
        print_err('add_to_cart is not selectable', err)


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
        .pause(1.5) \
        .click(element) \
        .pause(3) \
        .perform()


def print_items(
        lst_copy: list[WebElement],
        prefix: str,
        element: WebElement
) -> None:
    print(
        f'######################'
        f'{prefix}ies',
        *(item.get_attribute('text') for item in lst_copy),
        sep='\n'
    )
    print(
        f"######################"
        f"{prefix}y = {element.get_attribute('text')}"
    )


def make_screenshot(
        driver: WebDriver,
        err: WebDriverException,
        description: str
) -> None:
    if not (Path.cwd() / 'Errors').exists():
        (Path.cwd() / 'Errors').mkdir()
    driver.get_screenshot_as_file(
        f'{Path.cwd()}/Errors/{strftime("%d.%m.%Y_%H:%M:%S", localtime())}> {description}> {err.msg}.png'
    )


def print_err(
        title: str,
        err: WebDriverException
) -> None:
    print(
        f'######################'
        f'{strftime("%d.%m.%Y_%H:%M:%S", localtime())}> {title}> {err.__class__.__name__}> {err.msg}',
        sep='\n'
    )


def check_captcha(
        driver: WebDriver,
        wait: WebDriverWait[WebDriver]
) -> None:
    try:  # TODO: Refactor it -> fixed
        wait.until(ec.presence_of_element_located(Locators.captcha))
        make_screenshot(driver, Captcha('it happened'), 'CAPTCHA')
        print_err('CAPTCHA', Captcha('it happened'))
        sleep(3)
        driver.refresh()
    except TimeoutException:
        pass


def collect_cookies(
        driver: WebDriver,
        wait: WebDriverWait[WebDriver]
) -> None:
    wait.until(
        ec.presence_of_element_located(Locators.title)
    )

    if not (Path.cwd() / 'Cookies').exists():
        (Path.cwd() / 'Cookies').mkdir()
    if not (Path.cwd() / 'Cookies/cookies.json').exists():
        (Path.cwd() / 'Cookies/cookies.json').touch()

    with open(Path.cwd() / 'Cookies/cookies.json', 'r+', encoding='utf-8') as file:
        if not (Path.cwd() / 'Cookies/cookies.json').stat().st_size:
            cookies = [driver.get_cookies()]
        else:
            cookies = [*json.load(file), driver.get_cookies()]
        file.seek(0)
        json.dump(cookies, file, ensure_ascii=False, indent=4)


def reset_cookies() -> None:
    (Path.cwd() / 'Cookies/cookies.json').unlink(missing_ok=True)


def apply_cookies(
        driver: WebDriver,
) -> None:
    with open(Path.cwd() / 'Cookies/cookies.json', 'r', encoding='utf-8') as file:
        cookies_lst = json.load(file)
    driver.get('https://www.amazon.com/cart/')
    sleep(2.5)
    for cookies in cookies_lst:
        for cookie in cookies:
            driver.add_cookie(convert_cookie(cookie))
        driver.refresh()
        print(*driver.get_cookies(), '', sep='\n')
        sleep(2.5)


def convert_cookie(cookie: dict[str, str]) -> dict[str, str]:
    if temp := cookie.get('domain'):
        if temp[0] != '.':
            del cookie['domain']
        return cookie
    raise Exception('Invalid cookie')


def main() -> None:
    url = 'https://www.amazon.com/'
    reset_cookies()
    for _ in range(2):
        print('', f'######################Starting', sep='\n')
        with init_driver() as driver:
            wait = waiting(driver)
            driver.set_page_load_timeout(30)
            try:
                driver.get(url)
                check_captcha(driver, wait)
                select_country(driver, wait)
                for _ in range(3):
                    collect_cart(driver, wait)
                collect_cookies(driver, wait)
                sleep(3)
            except WebDriverException as err:
                make_screenshot(driver, err, 'critical_error')
                print_err('critical_error', err)
    # with init_driver() as driver:
    #     driver.set_page_load_timeout(30)
    #     apply_cookies(driver)


if __name__ == '__main__':
    main()
