import unittest

from VELORA_MOTORS.app import app


class ShopSearchTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_search_by_car_name(self):
        response = self.client.get('/shop?q=SF90')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'SF90 Stradale', response.data)

    def test_search_by_brand_name(self):
        response = self.client.get('/shop?q=Ferrari')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Ferrari', response.data)


if __name__ == '__main__':
    unittest.main()
