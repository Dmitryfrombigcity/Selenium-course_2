from copy import deepcopy
from random import choice
from time import sleep

from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait


def init_driver() -> WebDriver:
    options = webdriver.ChromeOptions()
    options.add_argument(f'--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)'
                         f' Chrome/121.0.0.0 Safari/537.36')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--window-size=1920,1080')
    return webdriver.Chrome(options=options)


def waiting(driver: WebDriver) -> WebDriverWait[WebDriver]:
    return WebDriverWait(driver=driver, timeout=10, poll_frequency=0.1)


def select_country(driver: WebDriver,
                   wait: WebDriverWait[WebDriver],
                   deliver_to: tuple[str, str],
                   countries_dropdown: tuple[str, str],
                   done_button: tuple[str, str]
                   ) -> None:
    try:
        wait.until(ec.element_to_be_clickable(deliver_to)).click()
    except TimeoutException:
        print('CUPCHA or homepage_error')
        driver.refresh()
        wait.until(ec.element_to_be_clickable(deliver_to)).click()

    try:
        wait.until(ec.presence_of_element_located(countries_dropdown))
    except TimeoutException:
        print('deliver_to_click_err')
        driver.find_element(*deliver_to).click()
        wait.until(ec.presence_of_element_located(countries_dropdown))

    dropdown = Select(driver.find_element(*countries_dropdown))
    dropdown.select_by_visible_text(choice(dropdown.options).text)
    wait.until(ec.presence_of_element_located(done_button)).click()


def collect_cart(driver: WebDriver,
                 wait: WebDriverWait[WebDriver],
                 category: str
                 ) -> list[dict[str, str]]:
    hamburger_menu_locator = ('xpath', '//a[@id="nav-hamburger-menu"]')
    category_locator = ('xpath', f'//a[text()= "{category}"]')

    items_locator = ('xpath', '//div[contains(@class, "s-product-image-container")]')
    add_to_cart_locator = ('xpath', '//input[@id="add-to-cart-button"]')
    cart_locator = ('xpath', '//div[@id="nav-cart-count-container"]')

    current_tab = driver.current_window_handle
    wait.until(ec.element_to_be_clickable(hamburger_menu_locator)).click()
    try:
        link = wait.until(ec.presence_of_element_located(category_locator)).get_attribute('href')

    except TimeoutException:
        print('good_link_error')
        link = driver.find_element(*category_locator).get_attribute('href')

    driver.switch_to.new_window('tab')
    for item in range(3):
        driver.get(link)
        try:
            choice(wait.until(ec.presence_of_all_elements_located(items_locator))).click()
            wait.until(ec.element_to_be_clickable(add_to_cart_locator)).click()
        except TimeoutException:
            print('add_good_error')
    driver.close()
    driver.switch_to.window(current_tab)
    wait.until(ec.element_to_be_clickable(cart_locator)).click()
    wait.until(ec.title_is('Amazon.com Shopping Cart'))
    return driver.get_cookies()


def replace_cookies(driver: WebDriver,
                    wait: WebDriverWait[WebDriver],
                    cookies_lst: list[list[dict[str, str]]]
                    ) -> None:
    cookies_copy = deepcopy(cookies_lst)
    driver.switch_to.new_window('tab')
    driver.get('https://www.amazon.com/cart/')
    wait.until(ec.title_is('Amazon.com Shopping Cart'))
    driver.delete_all_cookies()
    for index, cookies in enumerate(cookies_copy, 1):
        for cookie in cookies:
            driver.add_cookie(convert_cookie(cookie))
        sleep(5)
        driver.refresh()
        print(*driver.get_cookies(), '', sep='\n')


def convert_cookie(cookie: dict[str, str]) -> dict[str, str]:
    cookie_conv = cookie.copy()
    if temp := cookie_conv.get('domain'):
        if temp[0] != '.':
            del cookie_conv['domain']
        return cookie_conv
    raise Exception('Invalid cookie')


def main() -> None:
    url = 'https://www.amazon.com/'

    categories = ('Cell Phones & Accessories',
                  'Data Storage',
                  'Cats',
                  'Shoes',
                  'Kitchen & Dining')
    deliver_to = ('xpath', '//a[@id="nav-global-location-popover-link"]')
    countries_dropdown = ('xpath', '//select[@id="GLUXCountryList"]')
    done_button = ('xpath', '//button[@class="a-button-text"]')

    with init_driver() as driver:
        wait = waiting(driver)
        cookies_lst: list[list[dict[str, str]]] = []
        for _ in range(5):
            try:
                driver.get(url)
                select_country(driver,
                               wait,
                               deliver_to,
                               countries_dropdown,
                               done_button
                               )
                cookies_lst.append(collect_cart(driver,
                                                wait,
                                                choice(categories)
                                                ))
            except Exception:
                print('critical_error')
                if len(driver.window_handles) > 1:
                    driver.close()
            finally:
                driver.delete_all_cookies()
                # driver.back()
                sleep(5)

        replace_cookies(driver,
                        wait,
                        cookies_lst,
                        )
        sleep(3)


if __name__ == '__main__':
    main()
