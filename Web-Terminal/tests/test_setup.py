import unittest

from tests.base import BaseTestCase


class SetupTest(BaseTestCase):
    def test_setup(self):
        """
        Test application setup by asserting 'app', 'client' and context presence
        """
        self.assertTrue(self.app    is not None)
        self.assertTrue(self.client is not None)
        self.assertTrue(self._ctx   is not None)


if __name__ == '__main__':
    unittest.main()