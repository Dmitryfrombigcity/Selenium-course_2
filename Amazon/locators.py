class Locators:
    """Основные локаторы для сайта."""

    deliver_to = 'xpath', '//div[@id="nav-global-location-slot"]'
    countries_dropdown = 'xpath', '//select[@id="GLUXCountryList"]'
    done_button = 'xpath', '//button[@class="a-button-text"]'
    header = 'tag name', 'header'
    hamburger_menu = 'xpath', '//*[@id="nav-hamburger-menu"]'
    menu = 'xpath', '//ul[contains(@class, "hmenu-visible")]//a'
    hmenu_compressed_btn = 'xpath', '//a[@class = "hmenu-item hmenu-compressed-btn"]'
    search_results = 'xpath', '//div[contains(@class, "search-result")]//h2/a'
    title = 'xpath', '//title'
    add_to_cart = 'xpath', '//input[@id="add-to-cart-button"]'
    captcha = 'xpath', '//input[@id="captchacharacters"]'
