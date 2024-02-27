from time import sleep

from selenium.common.exceptions import WebDriverException

from amazon import Page
from browser import Browser
from utils import (make_screenshot, print_err,
                   reset_cookies, print_start)


def collect_data(
        quantity_of_countries: int = 20,
        quantity_of_purchases: int = 5
) -> None:
    """
    Собирает корзины товаров и записывает cookies в файл.

    :param quantity_of_countries: Количество стран.
    :param quantity_of_purchases: Количество попыток покупок для одной страны.
    :return:
    """

    reset_cookies()
    with Page('https://www.amazon.com/') as page:
        for _ in range(quantity_of_countries):
            print_start()
            try:
                page.driver = Browser().driver
                page.get_page()
                page.check_captcha()
                page.select_country()
                for _ in range(quantity_of_purchases):
                    page.collect_cart()
                page.collect_cookies()
                sleep(3)
            except WebDriverException as err:
                make_screenshot(err, 'critical_error', page.driver)
                print_err('critical_error', err)


def show_data() -> None:
    """Показывает корзину товаров для каждой страны."""

    with Page('https://www.amazon.com/cart/') as page:
        page.get_page()
        page.apply_cookies()


if __name__ == '__main__':
    #collect_data()
    show_data()
