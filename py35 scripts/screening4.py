import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By

class TestWebForm(unittest.TestCase):

	def setUp(self):
		chromeDriver = r"C:\Devs\Python\chromedriver.exe"
		driver = webdriver.Chrome(chromeDriver)
		driver.implicitly_wait(20)	# 20 seconds maximum wait time

	def testCorrectAnswer(self):
		test_url = "www.example.com/for_test"
		driver.get(test_url)
		text_box = driver.find_element_by_css_selector(["answer_field"])
		button = driver.find_element_by_css_selector(["submit_button"])
		text_box.clear()
		text_box.send_keys("correct answer")
		button.click()
		self.assertTrue(self.is_element_present(By.CSS_SELECTOR, ["correct_response"]))

	def testIncorrectAnswer(self):
		test_url = "www.example.com/for_test"
		driver.get(test_url)
		text_box = driver.find_element_by_css_selector(["answer_field"])
		button = driver.find_element_by_css_selector(["submit_button"])
		text_box.clear()
		text_box.send_keys("incorrect answer")
		button.click()
		self.assertTrue(self.is_element_present(By.CSS_SELECTOR, ["incorrect_response"]))

	def tearDown(self):
		driver.quit()


if __name__ == "__main__":
	unittest.main()
