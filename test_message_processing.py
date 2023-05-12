import unittest

import os
import json
from dotenv import load_dotenv
from geolocation import process_message
from kafka import KafkaConsumer, KafkaProducer
load_dotenv()

class MessageProcessingTest(unittest.TestCase):
    def test_process_message(self):
        message = {
            'client_id': '123',
            'timestamp': 1683904374000,
            'ip': '8.8.8.8'
        }

        result = process_message(message)

        expected_result = {
            'client_id': '123',
            'timestamp': 1683904374000,
            'ip': '8.8.8.8',
            'latitude': 40.5369987487793,
            'longitude': -82.12859344482422,
            'country': 'United States',
            'region': 'Ohio',
            'city': 'Glenmont'
        }
        self.assertEqual(result, expected_result)


class WrongInputTest(unittest.TestCase):
    def test_message_input(self):
        message = {'foo': 'bar'}
        with self.assertRaises(ValueError):
            process_message(message)

class MessageConsumingTest(unittest.TestCase):
    def test_consume_ip_check_output_topic(self):
        kafka_server = os.getenv("KAFKA_SERVER")
        output_topic = 'ip_check_output'

        message = {
            'client_id': '123',
            'timestamp': 1683904374000,
            'ip': '8.8.8.8'
        }

        consumer = KafkaConsumer(
            output_topic,
            bootstrap_servers=kafka_server,
            value_deserializer=lambda m: json.loads(m.decode('utf-8'))
        )
        message = next(consumer)
        process_message(message)
        consumer.close()

        expected_result = {
            'client_id': '123',
            'timestamp': 1683904374000,
            'ip': '8.8.8.8',
            'latitude': 40.5369987487793,
            'longitude': -82.12859344482422,
            'country': 'United States',
            'region': 'Ohio',
            'city': 'Glenmont'
        }

        self.assertEqual(message.value, expected_result)

if __name__ == '__main__':
    unittest.main()
