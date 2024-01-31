"""
Разобрался как работает перезапись cookies
удалять заранее не надо
cookie определяют ключи 'name', 'domain', 'path'
ключ 'value' является обязательным,
проблема возникает с 'domain'
могут быть двух видов
www.abc.com или abc.com -> только для текущего домена
.abc.com (точка спереди) ->для текущего домена и все поддоменов
всё чуть сложнее тут подробности http://bayou.io/draft/cookie.domain.html
если использовать driver.add_cookie({'name' : 'foo', 'value' : 'bar'})
то получится www.abc.com или abc.com
если использовать driver.add_cookie({'name' : 'foo', 'value' : 'bar', 'domain' : 'abc.com'})
или driver.add_cookie({'name' : 'foo', 'value' : 'bar', 'domain' : '.abc.com'})
т.е. к явному домену всегда добавляется '.', если её нет
то получится .abc.com
Резюме
всегда смотрите домен в оригинальной cookie,
чтобы не создавать копию cookie
Инфо
https://stackoverflow.com/questions/1062963/how-do-browser-cookie-domains-work?newreg=9029417e5e5148a2a16fa14f98d6c298
"""

from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait


def init_driver() -> WebDriver:
    options = webdriver.ChromeOptions()
    options.add_argument(f'--user-agent=Mozilla/5.0 (X11; Linux x86_64)'   # type: ignore
                         f' AppleWebKit/537.36 (KHTML, like Gecko)'        
                         f' Chrome/121.0.0.0 Safari/537.36')
    options.add_argument('--disable-blink-features=AutomationControlled')  # type: ignore
    options.add_argument('--window-size=1920,1080')                        # type: ignore
    options.page_load_strategy = 'eager'
    return webdriver.Chrome(options=options)


def waiting(driver: WebDriver) -> WebDriverWait[WebDriver]:
    return WebDriverWait(driver=driver, timeout=5, poll_frequency=0.1)


def get_token(driver: WebDriver,
              wait: WebDriverWait[WebDriver]
              ) -> dict[str, str] | None:
    LOGIN_FIELD = ("xpath", "//input[@id='login_email']")
    PASSWORD_FIELD = ("xpath", "//input[@id='password']")
    SUBMIT_BUTTON = ("xpath", "//button[@id='loginformsubmit']")

    wait.until(ec.visibility_of_element_located(LOGIN_FIELD))
    driver.find_element(*LOGIN_FIELD).send_keys("autocheck@ya.ru")
    driver.find_element(*PASSWORD_FIELD).send_keys("123")
    driver.find_element(*SUBMIT_BUTTON).click()

    token = driver.get_cookie('_freeconferencecall_session')
    print(f'Получили {token = }')
    return token


def rewrite_token(driver: WebDriver,
                  wait: WebDriverWait[WebDriver],
                  url: str,
                  token_lst: list[dict[str, str] | None]
                  ) -> None:
    tokens = (item for item in token_lst if item is not None)
    for token in tokens:
        driver.get(url)
        log_out(driver, wait, url)
        correct_add(driver, token, url)
        log_out(driver, wait, url)
        incorrect_add(driver, token, url)
        log_out(driver, wait, url)
        delete_before_add(driver, token, url)


def log_out(driver: WebDriver,
            wait: WebDriverWait[WebDriver],
            url: str) -> None:
    driver.delete_cookie('_freeconferencecall_session')
    driver.get(url)
    wait.until(ec.title_contains('Log in page'))
    print(f'{driver.title = }', sep='\n')


def correct_add(driver: WebDriver,
                token: dict[str, str],
                url: str) -> None:
    """Usage: driver.add_cookie({'name' : 'foo', 'value' : 'bar'})"""

    driver.add_cookie({'name': '_freeconferencecall_session',
                       'value': token.get('value')})
    driver.get(url)
    print('Корректная замена',
          *driver.get_cookies(),
          f'{driver.title = }',
          '',
          sep='\n')


def delete_before_add(driver: WebDriver,
                      token: dict[str, str],
                      url: str) -> None:
    driver.delete_cookie('_freeconferencecall_session')
    driver.add_cookie(token)
    driver.get(url)
    print('Замена с удаление сперва',
          *driver.get_cookies(),
          f'{driver.title = }',
          '',
          sep='\n')


def incorrect_add(driver: WebDriver,
                  token: dict[str, str],
                  url: str) -> None:
    """ Перед значением 'domain'а всегда ставится '.' """

    driver.add_cookie(token)
    driver.get(url)
    print('Некорректная замена',
          *driver.get_cookies(),
          f'{driver.title = }',
          '',
          sep='\n')


def main() -> None:
    url = 'https://www.freeconferencecall.com/login'
    with init_driver() as driver:
        driver.get(url)
        wait = waiting(driver)
        token_lst: list[dict[str, str] | None] = []
        for _ in range(3):
            token_lst.append(get_token(driver, wait))
            driver.delete_all_cookies()
            print('Удалили все cookies', *driver.get_cookies(), '', sep='\n')
            try:
                driver.get(url)
                wait.until(ec.title_contains('Log in page'))
            except TimeoutException:
                terms_of_service = driver.find_element('xpath',
                                                       '//button[@class="btn btn-lg btn-block btn-blue"]')
                terms_of_service.click()
                wait.until(ec.staleness_of(terms_of_service))
                driver.delete_all_cookies()
                driver.get(url)
            print('Перегрузили страницу', *driver.get_cookies(), '', sep='\n')
        rewrite_token(driver, wait, url, token_lst)


if __name__ == '__main__':
    main()
