from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from lists.views import home_page
from lists.models import Item

class HomePageTest(TestCase):

	def test_home_page_returns_correct_html(self):
		response = self.client.get('/')
		html = response.content.decode('utf8')

		self.assertTrue(html.startswith('<html>'))
		self.assertIn('<title>To-Do lists</title>', html)
		self.assertTrue(html.strip().endswith('</html>'))

	def test_can_save_a_POST_request(self):
		self.client.post('/', data={'item_text': 'A new list item'})
		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first()
		self.assertEqual(new_item.text, 'A new list item')

	def test_redirects_after_POST(self):
		response = self.client.post('/', data={'item_text': 'A new list item'})
		self.assertEqual(response.status_code, 302)
		self.assertEqual(response['location'], '/lists/the-only-list-in-the-world/')

class ListViewTest(TestCase):

	def test_user_list_tamplate(self):
		response = self.client.get('/lists/the-only-list-in-the-woirl/')
		self.assertTemplateUsed(response, 'list.html')