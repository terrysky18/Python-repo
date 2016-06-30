"""
A quick test to use selenium with Firefox webdriver to
access Defence Travel System test environment ATEST03
"""

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

DTS = 'Defense Travel System'
test_site = 'https://192.168.103.245:31917/wl/site/index.jsp'

class DTSpageTestCase(unittest.TestCase):

	def setUp(self):
		self.browser = webdriver.Firefox()

	def testPageTitle(self):
		self.browser.get(test_site)
		assert DTS in self.browser.title

	def tearDown(self):
		self.browser.close()

if __name__ == '__main__':
	unittest.main(verbosity=2)

