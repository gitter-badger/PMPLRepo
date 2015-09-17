from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase

class NewVisitorTest(LiveServerTestCase):
	def setUp(self):
		self.browser = webdriver.Firefox()
		self.browser.implicitly_wait(3)

	def tearDown(self):
		self.browser.quit()
	
	def check_for_row_in_list_table(self, row_text):
		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertIn(row_text, [row.text for row in rows])

	def test_can_start_a_list_and_retrieve_it_later(self):
		self.browser.get(self.live_server_url)
	
		self.assertIn('To-Do', self.browser.title)
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('To-Do', header_text)
		
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Buy peacock feathers')
		inputbox.send_keys(Keys.ENTER)
		#self.check_for_row_in_list_table('1: Buy peacock feathers')
		#table = self.browser.find_elements_by_id('id_list_table')
		#rows = table.find_elements_by_tag_name('tr')
		#self.assertIn('1: Buy peacock feathers', [row.text for row in rows])
		#self.assertEqual(
		#	inputbox.get_attribute('placeholder'),
		#	'Enter a to-do item'
		#)

		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Use peacock feathers to make a fly')
		inputbox.send_keys(Keys.ENTER)
		
		self.check_for_row_in_list_table('1: Buy peacock feathers')
		self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')		
		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertIn('1: Buy peacock feathers', [row.text  for row in rows])
		self.assertIn(
			'2: Use peacock feathers to make a fly',
			[row.text for row in rows]
		)
		
		count = 0
		statusku = self.browser.find_element_by_id('statusku')
		for row in rows:
			count = count + 1
	
		if count == 0:
			self.assertIn('yey, waktunya libur', statusku.text)
			self.fail('yey, waktunya libur')
		elif count !=0 and count < 5:
			self.assertIn('sibuk tapi santai', statusku.text)
			self.fail('sibuk tapi santai')
		else:
			self.assertIn('oh tidak', statusku.text)
			self.fail('oh tidak')
	
		#self.fail('Finish the test!')	
