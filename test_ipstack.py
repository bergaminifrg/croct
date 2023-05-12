import requests
import unittest

import os
from dotenv import load_dotenv

load_dotenv()
ipstack_api_key = os.getenv("IPSTACK_API_KEY")

class IPStackAPITest(unittest.TestCase):
    def test_ipstack_api_response(self):
        api_key = ipstack_api_key
        ip_address = '8.8.8.8'
        url = f'http://api.ipstack.com/{ip_address}?access_key={api_key}'
        response = requests.get(url)
        self.assertEqual(response.status_code, 200, f'API call returned a {response.status_code} status code')

if __name__ == '__main__':
    unittest.main()