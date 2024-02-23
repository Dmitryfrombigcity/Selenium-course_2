from time import sleep

from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from browser import Browser


class Base:
    def __init__(
            self,
            url: str,
            timeout: float = 10,
            poll_frequency: float = 0.1
    ) -> None:
        self.url = url
        self._timeout = timeout
        self._poll_frequency = poll_frequency
        self._driver: WebDriver = Browser().driver

    @property
    def driver(self) -> WebDriver:
        return self._driver

    @driver.setter
    def driver(self, value: WebDriver) -> None:
        self.driver.close()
        self._driver = value

    @property
    def action(self) -> ActionChains:
        return ActionChains(self._driver)

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
