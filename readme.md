# Croct Location Detector Challenge

This repository contains a standalone Kafka streaming application that translates IP addresses into geographical locations using the IPStack free API made as a challenge for Croct.

## Requirements

To run the application, you will need:

- Python and Docker installed on your machine
- Kafka, Zookeeper and Redis running (possibly via docker-compose) on your machine or reachable
- An valid API key from IPStack

## Setup Instructions

1. **Docker**: Run the containers (Kafka, Zookeeper and Redis) using the following command:
   docker-compose up -d

2. **Python Libraries**: Install the required Python libraries by running the following command in your terminal or command prompt:
   pip install -r requirements.txt

3. **Tests**: Use the following command to run tests:
   python test_message_processing.py

4. **Run the Application**: Execute the Python script by running the following command in your terminal or command prompt:
   python geolocation.py

5. **Running stress and load tests (Not advised - IPStack will hate us)**:
   python test_load_and_stress.py