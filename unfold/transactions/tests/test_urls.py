from django.urls import reverse, resolve

from test_plus.test import TestCase

class TestTransactionURLs(TestCase):

    def setUp(self):
        self.user = self.make_user()

    def test_purchase_reverse(self):
        """users:list should reverse to /users/."""
        self.assertEqual(reverse('transactions:purchase-view'), '/purchase')

    def test_reload_reverse(self):
        """users:list should reverse to /users/."""
        self.assertEqual(reverse('transactions:reload-view'), '/reload')

    def test_charges_reverse(self):
        """users:list should reverse to /users/."""
        self.assertEqual(reverse('transactions:charges-view'), '/charges')

    def test_articles_reverse(self):
        """users:list should reverse to /users/."""
        self.assertEqual(reverse('transactions:articles-view'), '/articles')

    def test_new_api_key_reverse(self):
        """users:list should reverse to /users/."""
        self.assertEqual(reverse('transactions:new-api-key-view'), '/new-api-key')