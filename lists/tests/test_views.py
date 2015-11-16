from django.template.loader import render_to_string
from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from lists.views import home_page
from lists.models import Item, List

class HomePageTest(TestCase): 
	
	def test_root_url_resolves_to_home_page_view(self):
		found = resolve('/')
		self.assertEqual(found.func, home_page)

	#def test_home_page_returns_correct_html(self):
	#	request = HttpRequest()
	#	response = home_page(request)
	#	expected_html = render_to_string('home.html')
	#	self.assertEqual(response.content.decode(), expected_html)	

	#def test_home_page_displays_all_list_items(self):
		#Item.objects.create(text='itemey 1')
		#Item.objects.create(text='itemey 2')

		#request = HttpRequest()
		#response = home_page(request)
		#self.assertIn('itemey 1', response.content.decode())
		#self.assertIn('itemey 2', response.content.decode())

	def test_komentar_pribadi_otomatis(self):
		count_item = Item.objects.all()
		request = HttpRequest()
		home_page(request)
		if count_item.count() == 0:
			self.assertEqual(count_item.count(), 0, "yey, waktunya libur")
		elif count_item.count() != 0  and count_item.count() < 5 :
			self.assertEqual(count_item.count(), 5, "sibuk tapi santai")
		else:
			self.assertGreaterEqual(count_item.count(), 5, "oh,tidak")

 
class ListViewTest(TestCase):
	
	def test_uses_list_templates(self):
		list_ =List.objects.create()		
		response = self.client.get('/lists/%d/' % (list_.id,))
		self.assertTemplateUsed(response, 'list.html')

	def test_displays_all_items(self):
		correct_list = List.objects.create()		
		Item.objects.create(text='itemey 1', list=correct_list)
		Item.objects.create(text='itemey 2', list=correct_list)
		other_list = List.objects.create()
		Item.objects.create(text='other list item 1', list=other_list)
		Item.objects.create(text='other list item 2', list=other_list)
		
		response = self.client.get('/lists/%d/' % (correct_list.id,))
		self.assertContains(response, 'itemey 1')
		self.assertContains(response, 'itemey 2')
		self.assertNotContains(response, 'other list item 1')
		self.assertNotContains(response, 'other list item 2')
	def test_passes_correct_list_to_template(self):
		other_list = List.objects.create()
		correct_list = List.objects.create()
		response = self.client.post(
			'/lists/%d/' % (correct_list.id,))
		self.assertEqual(response.context['list'], correct_list)

class NewListTest(TestCase):

	def test_saving_a_POST_request(self):
		self.client.post(
			'/lists/new',
			data={'item_text': 'A new list item'}
		)
		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first()
		self.assertEqual(new_item.text, 'A new list item')
	
	def test_redirects_after_POST(self):
		response = self.client.post(
			'/lists/new',
			data={'item_text': 'A new list item'}
		)
		new_list = List.objects.first()
		self.assertRedirects(response, '/lists/%d/' % (new_list.id,))

class NewItemTest(TestCase):

	def test_can_save_a_POST_request_to_an_existing_list(self):
		other_list = List.objects.create()
		correct_list = List.objects.create()		
		self.client.post(
			'/lists/%d/add_item' % (correct_list.id,),
			data={'item_text': 'A new item for an existing list'}
		)
		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first()
		self.assertEqual(new_item.text, 'A new item for an existing list')
		self.assertEqual(new_item.list, correct_list)
	
	def test_redirects_to_list_view(self):
		other_list = List.objects.create()
		correct_list = List.objects.create()
		response = self.client.post(
			'/lists/%d/add_item' % (correct_list.id,),
			data={'item_text': 'A new item for an existing list'}
		)
		self.assertRedirects(response, '/lists/%d/' % (correct_list.id,))
