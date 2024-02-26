import json
from pathlib import Path
from random import choice
from time import sleep

from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.select import Select

from base import Base
from exceptions import Captcha
from locators import Locators
from utils import (print_items, make_screenshot, print_err,
                   print_title)


class Page(Base):

    def select_country(self) -> None:
        try:
            self.element_is_clickable(
                Locators.deliver_to,
                error='deliver_to is not clickable'
            )
        except TimeoutException as err:
            make_screenshot(err, 'homepage_error', self.driver)
            print_err('homepage_error', err)
            self.driver.refresh()
        finally:
            header_state = self.presence_of_element(Locators.header)
            self.element_is_clickable(
                Locators.deliver_to,
                error='deliver_to was not clickable twice'
            ).click()

        try:
            self.presence_of_element(
                Locators.countries_dropdown,
                error='countries_dropdown failed'
            )
        except TimeoutException as err:  # sometimes this happens
            make_screenshot(err, 'deliver_to_click_err', self.driver)
            print_err('deliver_to_click_err', err)

            self.presence_of_element(Locators.deliver_to).click()
            self.presence_of_element(
                Locators.countries_dropdown,
                error='countries_dropdown failed twice'
            )

        dropdown = Select(
            self.presence_of_element(Locators.countries_dropdown)
        )
        dropdown.select_by_visible_text(choice(dropdown.options).text)
        self.presence_of_element(
            Locators.done_button,
            error='done_button is no present'
        ).click()

        self.element_is_stale(
            header_state,
            error='header_state didn\'t change'
        )

    def collect_cart(self) -> None:
        self.action \
            .move_to_element(self.presence_of_element(Locators.hamburger_menu)) \
            .click(self.presence_of_element(Locators.hamburger_menu)) \
            .perform()

        # driver.find_element(*hamburger_menu).click() -> doesn't work properly
        # script under hamburger_menu works twice
        # need to hover over hamburger_menu firstly and then click to solve it

        try:
            self.element_is_clickable(
                Locators.hmenu_compressed_btn,
                error='hmenu_compressed_btn is not clickable'
            ).click()

            category_lst = self.presence_of_elements(
                Locators.menu,
                error='category_menu is not present'
            )[3:25]

            # sometimes invalid URL -> maybe a longer delay is needed
            self._click_element(category_lst, 'categor')
            subcategory_lst = self.visibility_of_elements(
                Locators.menu,
                error='subcategory_menu is not present'
            )[1:]

            self._click_element(subcategory_lst, 'subcategor')
        except TimeoutException as err:
            make_screenshot(err, 'category/subcategory', self.driver)
            print_err('category/subcategory', err)
            self.driver.refresh()
        else:
            try:
                search_results_lst = self.visibility_of_elements(
                    Locators.search_results,
                    error='no_search-results'
                )
            except WebDriverException as err:
                make_screenshot(err, 'no_search-results', self.driver)
                print_err('no_search-results', err)
                self.driver.refresh()
            else:
                choice(search_results_lst).click()
                self._add_good()

    def collect_cookies(self) -> None:
        self.presence_of_element(Locators.title)
        self._check_cookies_file()

        with open(Path.cwd() / 'Cookies/cookies.json', 'r+', encoding='utf-8') as file:
            if not (Path.cwd() / 'Cookies/cookies.json').stat().st_size:
                cookies = [self.driver.get_cookies()]
            else:
                cookies = [*json.load(file), self.driver.get_cookies()]
            file.seek(0)
            json.dump(cookies, file, ensure_ascii=False, indent=4)

    def apply_cookies(self) -> None:
        with open(Path.cwd() / 'Cookies/cookies.json', 'r', encoding='utf-8') as file:
            cookies_lst = json.load(file)

        for cookies in cookies_lst:
            for cookie in cookies:
                self.driver.add_cookie(self._convert_cookie(cookie))
            self.driver.refresh()
            print(*self.driver.get_cookies(), '', sep='\n')
            sleep(3)

    def check_captcha(self) -> None:
        try:
            self.presence_of_element(Locators.captcha, timeout=1)
            make_screenshot(Captcha('it happened'), 'CAPTCHA', self.driver)
            print_err('CAPTCHA', Captcha('it happened'))
            sleep(1)
            self.driver.refresh()
        except TimeoutException:
            pass

    def _add_good(self) -> None:
        self.presence_of_element(Locators.title)
        try:
            print_title(self.driver)
            self.element_is_clickable(
                Locators.add_to_cart,
                error='good is unavailable',
                timeout=3
            ).click()

        except TimeoutException as err:
            make_screenshot(err, 'add_to_cart is not selectable', self.driver)
            print_err('add_to_cart is not selectable', err)

    def _click_element(
            self,
            lst: list[WebElement],
            prefix: str
    ) -> None:
        lst_copy = lst[:]
        element = choice(lst_copy)
        print_items(lst_copy, prefix, element)
        self.action \
            .move_to_element(element) \
            .pause(1.5) \
            .click(element) \
            .pause(3) \
            .perform()

    @staticmethod
    def _convert_cookie(cookie: dict[str, str]) -> dict[str, str]:
        if temp := cookie.get('domain'):
            if temp[0] != '.':
                del cookie['domain']
            return cookie
        raise Exception('Invalid cookie')

    @staticmethod
    def _check_cookies_file() -> None:
        if not (Path.cwd() / 'Cookies').exists():
            (Path.cwd() / 'Cookies').mkdir()
        if not (Path.cwd() / 'Cookies/cookies.json').exists():
            (Path.cwd() / 'Cookies/cookies.json').touch()
