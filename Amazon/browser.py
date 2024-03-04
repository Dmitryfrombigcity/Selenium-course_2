from selenium import webdriver

from utils import delete_dir, profile_dir


# import undetected_chromedriver as webdriver # just in case


class Browser:
    """Класс для инициализации браузера."""

    def __init__(self) -> None:
        options = webdriver.ChromeOptions()
        options.add_argument(f'--user-agent=Mozilla/5.0 (X11; Linux x86_64)'  # type: ignore
                             f' AppleWebKit/537.36 (KHTML, like Gecko)'
                             f' Chrome/121.0.0.0 Safari/537.36')
        options.add_argument('--disable-blink-features=AutomationControlled')  # type: ignore
        # options.add_argument('--headless=new')  # type: ignore
        # service = webdriver.ChromeService(service_args=['--log-level=DEBUG'], log_output='log.txt') # type: ignore
        options.add_argument('--window-size=1920,1080')  # type: ignore
        if profile_dir.exists():
            delete_dir(profile_dir)
        options.add_argument(f"--user-data-dir={profile_dir}")

        options.add_experimental_option("excludeSwitches", ['enable-automation'])
        self.driver = webdriver.Chrome(options=options)
        self.driver.set_page_load_timeout(30)
