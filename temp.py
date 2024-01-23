from time import sleep

from selenium import webdriver

from selenium.webdriver.firefox.service import Service

service = Service()
driver = webdriver.Firefox()
sleep(30)