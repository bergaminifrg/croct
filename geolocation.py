import json
from kafka import KafkaConsumer, KafkaProducer
import requests
import redis
import os
from dotenv import load_dotenv

load_dotenv()

kafka_server = os.getenv("KAFKA_SERVER")
ipstack_api_key = os.getenv("IPSTACK_API_KEY")
redis_host = os.getenv("REDIS_HOST")
redis_port = os.getenv("REDIS_PORT")
redis_ttl = os.getenv("REDIS_TTL")

IPSTACK_API_URL = f"http://api.ipstack.com/"

KAFKA_INPUT_TOPIC = "ip_check_input"
KAFKA_OUTPUT_TOPIC = "ip_check_output"

consumer = KafkaConsumer(
    KAFKA_INPUT_TOPIC,
    bootstrap_servers=kafka_server,
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='earliest'
)

producer = KafkaProducer(
    bootstrap_servers=kafka_server,
    value_serializer=lambda m: json.dumps(m).encode('utf-8')
)

redis_client = redis.Redis(host=redis_host, port=redis_port)


def process_message(msg):
    client_id = msg.get("client_id")
    timestamp = msg.get("timestamp")
    ip_address = msg.get("ip")
    if not all([client_id, timestamp, ip_address]):
        raise ValueError()
    
    user_data = {
        "client_id": client_id,
        "timestamp": timestamp,
        "ip": ip_address
    }
    
    try:
        cache_key = f"{ip_address}"
        stored_info = redis_client.get(cache_key)
        if stored_info:
            result = {**user_data, **json.loads(stored_info)}
            producer.send(KAFKA_OUTPUT_TOPIC, value=result)
            return result
        
        response = requests.get(f"{IPSTACK_API_URL}{ip_address}?access_key={ipstack_api_key}")
        response.raise_for_status()
        location_data = response.json()
        location = {
            "latitude": location_data.get("latitude"),
            "longitude": location_data.get("longitude"),
            "country": location_data.get("country_name"),
            "region": location_data.get("region_name"),
            "city": location_data.get("city")
        }
        result = {**user_data, **location}
        redis_client.setex(cache_key, redis_ttl, json.dumps(location))
        producer.send(KAFKA_OUTPUT_TOPIC, value=result)
        return result
    except Exception as e:
        print(f"Error processing message {msg}: {e}")

def run():
    for msg in consumer:
        process_message(msg.value)
        consumer.commit()
        
if __name__ == "__main__":
    run()