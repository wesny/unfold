from django.urls import reverse, resolve

from test_plus.test import TestCase


class TestUserURLs(TestCase):
    """Test URL patterns for users app."""

    def setUp(self):
        self.user = self.make_user()

    def test_redirect_reverse(self):
        """users:redirect should reverse to /users/~redirect/."""
        self.assertEqual(reverse('users:redirect'), '/user~redirect')

    def test_redirect_resolve(self):
        """/users/~redirect/ should resolve to users:redirect."""
        self.assertEqual(
            resolve('/user~redirect/').view_name,
            'users:redirect'
        )

    def test_detail_reverse(self):
        """users:detail should reverse to /users/testuser/."""
        self.assertEqual(
            reverse('users:detail'),
            '/user'
        )

    def test_detail_resolve(self):
        """/users/testuser/ should resolve to users:detail."""
        self.assertEqual(resolve('/user').view_name, 'users:detail')

    def test_update_reverse(self):
        """users:update should reverse to /users/~update/."""
        self.assertEqual(reverse('users:update'), '/user~update')

    def test_update_resolve(self):
        """/users/~update/ should resolve to users:update."""
        self.assertEqual(
            resolve('/user~update').view_name,
            'users:update'
        )
