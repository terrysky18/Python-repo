"""
A simple to script to refresh webmail page and prevents it from timing out
"""

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

mail_url = 'https://owaeast.ngc.com/owa/#path=/mail'

my_browser = webdriver.Firefox()
my_browser.get(mail_url)
page_title = my_browser.title

print(page_title, ' loaded')

