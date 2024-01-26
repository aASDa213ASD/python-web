import unittest
from flask import url_for
from tests.base import BaseTestCase


class MainViewsTests(BaseTestCase):
    def test_root_page(self):
        """
        Test if root page loads with a 200
        """
        with self.client:
            response = self.client.get(url_for('main.root'))
            self.assertEqual(response.status_code, 200)

            self.assertIn(b'help', response.data)

    def test_skills_page(self):
        """
        Test if the skills page loads with a 200
        """
        with self.client:
            response = self.client.get(url_for('main.skills'))
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Assembly', response.data)

    def test_projects_page(self):
        """
        Test if projects page loads with 200
        """
        with self.client:
            response = self.client.get(url_for('main.projects'))
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'True-Sight', response.data)


if __name__ == "__main__":
    unittest.main()