from time import sleep
from typing import TypeVar

from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from browser import Browser
from utils import delete_dir, profile_dir

T = TypeVar('T')


class Base:
    """Класс с базовыми методами."""

    def __init__(
            self,
            url: str,
            timeout: float = 10,
            poll_frequency: float = 0.1
    ) -> None:
        self.url = url
        self._timeout = timeout
        self._poll_frequency = poll_frequency
        self.driver: WebDriver = Browser().driver

    def __enter__(self: T) -> T:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self._driver.close()
        delete_dir(profile_dir)

    @property
    def driver(self) -> WebDriver:
        return self._driver

    @driver.setter
    def driver(self, value: WebDriver) -> None:
        sleep(5)
        self._driver = value
        self.action = ActionChains(self._driver)

    def get_page(self) -> None:
        self.driver.get(self.url)
        sleep(3)

    def presence_of_element(
            self,
            locator: tuple[str, str],
            error: str = '',
            timeout: float | None = None
    ) -> WebElement:

        if timeout is None:
            timeout = self._timeout

        return WebDriverWait(
            self.driver,
            timeout,
            self._poll_frequency,
        ).until(
            ec.presence_of_element_located(locator=locator),
            message=error
        )

    def presence_of_elements(
            self,
            locator: tuple[str, str],
            error: str = '',
            timeout: float | None = None
    ) -> list[WebElement]:

        if timeout is None:
            timeout = self._timeout

        return WebDriverWait(
            self.driver,
            timeout,
            self._poll_frequency,
        ).until(
            ec.presence_of_all_elements_located(locator=locator),
            message=error
        )

    def visibility_of_elements(
            self,
            locator: tuple[str, str],
            error: str = '',
            timeout: float | None = None
    ) -> list[WebElement]:

        if timeout is None:
            timeout = self._timeout

        return WebDriverWait(
            self.driver,
            timeout,
            self._poll_frequency,
        ).until(
            ec.visibility_of_all_elements_located(locator=locator),
            message=error
        )

    def element_is_clickable(
            self,
            locator: tuple[str, str],
            error: str = '',
            timeout: float | None = None
    ) -> WebElement:

        if timeout is None:
            timeout = self._timeout

        return WebDriverWait(
            self.driver,
            timeout,
            self._poll_frequency,
        ).until(
            ec.element_to_be_clickable(mark=locator),
            message=error
        )

    def element_is_stale(
            self,
            element: WebElement,
            error: str = '',
            timeout: float | None = None
    ) -> bool:

        if timeout is None:
            timeout = self._timeout

        return WebDriverWait(
            self.driver,
            timeout,
            self._poll_frequency,
        ).until(
            ec.staleness_of(element=element),
            message=error
        )
