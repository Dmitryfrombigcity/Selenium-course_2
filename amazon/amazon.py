import json
from pathlib import Path
from random import choice
from time import strftime, localtime, sleep

from selenium import webdriver
# import undetected_chromedriver as webdriver # just in case
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

from locators import Locators


def reset_cookies() -> None:
    (Path.cwd() / 'Cookies/cookies.json').unlink(missing_ok=True)


class Captcha(WebDriverException):
    pass


class Page:
    def __init__(self):
        options = webdriver.ChromeOptions()
        # service = webdriver.ChromeService(service_args=['--log-level=DEBUG'], log_output='log.txt')
        options.add_argument(f'--user-agent=Mozilla/5.0 (X11; Linux x86_64)'  # type: ignore
                             f' AppleWebKit/537.36 (KHTML, like Gecko)'
                             f' Chrome/121.0.0.0 Safari/537.36')
        options.add_argument('--disable-blink-features=AutomationControlled')  # type: ignore
        # options.add_argument('--headless=new')  # type: ignore
        options.add_argument('--window-size=1920,1080')  # type: ignore
        options.add_experimental_option("excludeSwitches", ['enable-automation'])  # type: ignore
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(driver=self.driver, timeout=10, poll_frequency=0.5)
        self.driver.set_page_load_timeout(30)

    def select_country(self):
        try:
            self.wait.until(
                ec.element_to_be_clickable(Locators.deliver_to),
                message='deliver_to is not clickable'
            )
        except TimeoutException as err:
            self.make_screenshot(err, 'homepage_error')
            self.print_err('homepage_error', err)
            self.driver.refresh()
        finally:
            header_state = self.wait.until(
                ec.presence_of_element_located(Locators.header)
            )
            self.wait.until(
                ec.element_to_be_clickable(Locators.deliver_to),
                message='deliver_to was not clickable twice'
            ).click()

        try:
            self.wait.until(
                ec.presence_of_element_located(Locators.countries_dropdown),
                message='countries_dropdown failed'
            )
        except TimeoutException as err:  # sometimes this happens
            self.make_screenshot(err, 'deliver_to_click_err')
            self.print_err('deliver_to_click_err', err)

            self.driver.find_element(*Locators.deliver_to).click()
            self.wait.until(
                ec.presence_of_element_located(Locators.countries_dropdown),
                message='countries_dropdown failed twice'
            )

        dropdown = Select(self.driver.find_element(*Locators.countries_dropdown))
        dropdown.select_by_visible_text(choice(dropdown.options).text)
        self.wait.until(
            ec.presence_of_element_located(Locators.done_button),
            message='done_button is no present'
        ).click()
        self.wait.until(
            ec.staleness_of(header_state),
            message='header_state didn\'t change'
        )

    def collect_cart(self):

        # sleep(5)  # найти способ поменять на ожидание
        #  -> solved by wait.until(ec.staleness_of(header_state))

        action = ActionChains(self.driver)
        action \
            .move_to_element(self.driver.find_element(*Locators.hamburger_menu)) \
            .click(self.driver.find_element(*Locators.hamburger_menu)) \
            .perform()

        # driver.find_element(*hamburger_menu).click() -> doesn't work properly
        # script under hamburger_menu works twice
        # need to hover over hamburger_menu firstly and then click to solve it

        try:
            self.wait.until(
                ec.element_to_be_clickable(Locators.hmenu_compressed_btn),
                message='hmenu_compressed_btn is not clickable'
            ).click()
            category_lst = self.wait.until(
                ec.presence_of_all_elements_located(Locators.menu),
                message='category_menu is not present'
            )[3:25]
            # sometimes invalid URL -> maybe a longer delay is needed
            self.click_element(category_lst, 'categor', action)
            subcategory_lst = self.wait.until(
                ec.visibility_of_all_elements_located(Locators.menu),
                message='subcategory_menu is not present'
            )[1:]
            self.click_element(subcategory_lst, 'subcategor', action)
        except TimeoutException as err:
            self.make_screenshot(err, 'category/subcategory')
            self.print_err('category/subcategory', err)
            self.driver.refresh()
        else:
            try:
                search_results_lst = self.wait.until(
                    ec.visibility_of_all_elements_located(Locators.search_results),
                    message='no_search-results'
                )
            except WebDriverException as err:
                self.make_screenshot(err, 'no_search-results')
                self.print_err('no_search-results', err)
                self.driver.refresh()
            else:
                choice(search_results_lst).click()
                self.add_good()

    def add_good(self):
        self.wait.until(
            ec.presence_of_element_located(Locators.title)
        )
        try:
            print(
                f'######################'
                f'title = {self.driver.title}'
            )
            self.wait.until(
                ec.element_to_be_clickable(Locators.add_to_cart),
                message='good is unavailable'
            ).click()

        except TimeoutException as err:
            self.make_screenshot(err, 'add_to_cart is not selectable')
            self.print_err('add_to_cart is not selectable', err)

    def click_element(self,
                      lst: list[WebElement],
                      prefix: str,
                      action: ActionChains
                      ) -> None:
        lst_copy = lst[:]
        element = choice(lst_copy)
        self.print_items(lst_copy, prefix, element)
        action \
            .move_to_element(element) \
            .pause(1.5) \
            .click(element) \
            .pause(3) \
            .perform()

    @staticmethod
    def print_items(lst_copy: list[WebElement],
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
            self,
            err: WebDriverException,
            description: str
    ) -> None:
        if not (Path.cwd() / 'Errors').exists():
            (Path.cwd() / 'Errors').mkdir()
        self.driver.get_screenshot_as_file(
            f'{Path.cwd()}/Errors/{strftime("%d.%m.%Y_%H:%M:%S", localtime())}> {description}> {err.msg}.png'
        )

    @staticmethod
    def print_err(title: str,
                  err: WebDriverException
                  ) -> None:
        print(
            f'######################'
            f'{strftime("%d.%m.%Y_%H:%M:%S", localtime())}> {title}> {err.__class__.__name__}> {err.msg}',
            sep='\n'
        )

    def check_captcha(self):
        try:  # TODO: Refactor it -> fixed
            self.wait.until(ec.presence_of_element_located(Locators.captcha))
            self.make_screenshot(Captcha('it happened'), 'CAPTCHA')
            self.print_err('CAPTCHA', Captcha('it happened'))
            sleep(3)
            self.driver.refresh()
        except TimeoutException:
            pass

    def collect_cookies(self):
        self.wait.until(
            ec.presence_of_element_located(Locators.title)
        )

        if not (Path.cwd() / 'Cookies').exists():
            (Path.cwd() / 'Cookies').mkdir()
        if not (Path.cwd() / 'Cookies/cookies.json').exists():
            (Path.cwd() / 'Cookies/cookies.json').touch()

        with open(Path.cwd() / 'Cookies/cookies.json', 'r+', encoding='utf-8') as file:
            if not (Path.cwd() / 'Cookies/cookies.json').stat().st_size:
                cookies = [self.driver.get_cookies()]
            else:
                cookies = [*json.load(file), self.driver.get_cookies()]
            file.seek(0)
            json.dump(cookies, file, ensure_ascii=False, indent=4)

    def apply_cookies(self):
        with open(Path.cwd() / 'Cookies/cookies.json', 'r', encoding='utf-8') as file:
            cookies_lst = json.load(file)
        self.driver.get('https://www.amazon.com/cart/')
        sleep(2.5)
        for cookies in cookies_lst:
            for cookie in cookies:
                self.driver.add_cookie(self.convert_cookie(cookie))
            self.driver.refresh()
            print(*self.driver.get_cookies(), '', sep='\n')
            sleep(2.5)

    @staticmethod
    def convert_cookie(cookie: dict[str, str]) -> dict[str, str]:
        if temp := cookie.get('domain'):
            if temp[0] != '.':
                del cookie['domain']
            return cookie
        raise Exception('Invalid cookie')


def main() -> None:
    url = 'https://www.amazon.com/'

    # reset_cookies()
    # for _ in range(2):
    #     page = Page()
    #     print('', f'######################Starting', sep='\n')
    #     try:
    #         page.driver.get(url)
    #         page.check_captcha()
    #         page.select_country()
    #         for _ in range(3):
    #             page.collect_cart()
    #         page.collect_cookies()
    #         sleep(3)
    #     except WebDriverException as err:
    #         page.make_screenshot(err, 'critical_error')
    #         page.print_err('critical_error', err)
    page = Page()
    page.driver.get(url)
    page.apply_cookies()


if __name__ == '__main__':
    main()
