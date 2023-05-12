import unittest
import threading
import time
from geolocation import process_message

def produce_messages_in_batch(amount_of_messages):
    for i in range(amount_of_messages):
        ip24 = i
        if(i > 255):
          ip24 = i % 255
        ip16 = round(i/255)
        message = {
            'client_id': f'client_{i}',
            'timestamp': int(time.time() * 1000),
            'ip': f'192.168.{ip16}.{ip24}'
        }
        process_message(message)

class PerformanceAndScalabilityTest(unittest.TestCase):
    def test_load(self):
        amount_of_messages = 10000
        amount_of_threads = 10

        threads = []
        for _ in range(amount_of_threads):
            thread = threading.Thread(target=produce_messages_in_batch, args=(amount_of_messages,))
            threads.append(thread)

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        # Assert performance metrics here

    def test_scalability(self):
        amount_of_messages = 1000
        amount_of_threads = 5

        threads = []
        for _ in range(amount_of_threads):
            thread = threading.Thread(target=produce_messages_in_batch, args=(amount_of_messages,))
            threads.append(thread)

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        # Assert performance metrics here

    def test_stress(self):
        amount_of_messages = 1000 
        amount_of_threads = 20

        threads = []
        for _ in range(amount_of_threads):
            thread = threading.Thread(target=produce_messages_in_batch, args=(amount_of_messages,))
            threads.append(thread)

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        # Assert performance metrics here

if __name__ == '__main__':
    unittest.main()