from flask import Flask, request, jsonify
from kafka import KafkaProducer, KafkaConsumer
from pymongo import MongoClient
import threading
import json
import os

app = Flask(_name_)

# Kafka ve MongoDB ayarları
KAFKA_TOPIC = 'my_topic'
KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka.dev.svc.cluster.local:9092').split(',')
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://mongodb.dev.svc.cluster.local:27017')
MONGO_DB = 'mydatabase'
MONGO_COLLECTION = 'mycollection'

# Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    security_protocol='PLAINTEXT'  # Bu satırı ekleyin!
)

# MongoDB Client
mongo_client = MongoClient(MONGO_URI)
mongo_collection = mongo_client[MONGO_DB][MONGO_COLLECTION]

# Kafka Consumer Thread
def consume_and_store():
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        auto_offset_reset='earliest',
        group_id='my-group',
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        security_protocol='PLAINTEXT'  # Bu satırı ekleyin!
    )
    for msg in consumer:
        print(f"Consumed message: {msg.value}")
        mongo_collection.insert_one(msg.value)

threading.Thread(target=consume_and_store, daemon=True).start()

@app.route('/publish', methods=['GET', 'POST'])
def publish():
    value = request.args.get('value')
    if request.method == 'POST' and not value:
        data = request.get_json()
        value = data.get('value') if data else None

    if not value:
        return jsonify({'error': 'No value provided'}), 400

    producer.send(KAFKA_TOPIC, {'value': value})
    producer.flush()

    return jsonify({'message': f'Value \"{value}\" sent to Kafka'})

if _name_ == '_main_':
    app.run(host='0.0.0.0', port=5000)
