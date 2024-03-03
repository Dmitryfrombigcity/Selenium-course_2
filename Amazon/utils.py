from pathlib import Path
from time import strftime, localtime

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

profile_dir = Path.cwd() / 'Profile'
cookies_dir = Path.cwd() / 'Cookies'


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


def print_title(driver: WebDriver) -> None:
    print(
        f'######################'
        f'title = {driver.title}',
        '',
        sep='\n'
    )


def print_start() -> None:
    print(
        '',
        f'######################'
        f'Starting',
        sep='\n'
    )


def make_screenshot(
        err: WebDriverException,
        description: str,
        driver: WebDriver
) -> None:
    if not (Path.cwd() / 'Errors').exists():
        (Path.cwd() / 'Errors').mkdir()

    driver.get_screenshot_as_file(
        f'{Path.cwd()}/Errors/{strftime("%d.%m.%Y_%H:%M:%S", localtime())}> {description}>'
        f' {tmp[:50] if isinstance(tmp := err.msg, str) else tmp}.png'
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


def delete_dir(path: Path) -> None:
    for item in path.iterdir():
        if item.is_dir():
            delete_dir(item)
        else:
            item.unlink()
    path.rmdir()
