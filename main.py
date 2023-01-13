import asyncio
import os
import aiokafka
import boto3
import json
import time
from flask import Flask, request, jsonify
from kafka import KafkaProducer, KafkaConsumer


async def produce_message(producer, topic, message):
    # Produce the message to the Kafka topic asynchronously
    await producer.send(topic, message)
    producer.flush()

async def produce_messages(producer, paths):
    # Produce a message for each path in the list
    for path in paths:
        # Create a message payload with the S3 bucket name and file path
        message = {"bucket_name": "my-bucket", "path": path}

        # Convert the message to a JSON string
        message_json = json.dumps(message)

        # Produce the message to the Kafka topic asynchronously
        await producer.send("download-queue", message_json)

#async def app(scope, receive, send):
#    assert scope['type'] == 'http'

#    await send({
#        'type': 'http.response.start',
#        'status': 200,
#        'headers': [
#            [b'content-type', b'text/plain'],
#        ],
#    })
#    await send({
#        'type': 'http.response.body',
#        'body': b'Hello, world!',
#    })

#async def main():
    # Create a Kafka producer
#    producer = aiokafka.AIOKafkaProducer(loop=loop, bootstrap_servers="localhost:9092")

    # Set the list of paths to be downloaded
#    paths = ["path/to/file1.txt", "path/to/file2.txt", "path/to/file3.txt"]

    # Produce the messages to the Kafka topic
#    await produce_messages(producer, paths)

#if __name__ == "__main__":
#    loop = asyncio.get_event_loop()
#    loop.run_until_complete(main())


#loop = asyncio.new_event_loop()
#asyncio.set_event_loop(loop)

app = Flask(__name__)
#for variable, value in os.environ.items():
#    app.config[env_name] = value

    
def kafkaProducer():
    print("Sent to consumer")
    return jsonify({
        "message": "You will receive an email in a short while with the plot", 
        "status": "Pass"})

producer = KafkaProducer (
    bootstrap_servers = 'kafka:9092',
    api_version = (0, 11, 15)
)



@app.route("/ingest", methods=["POST"])
def ingest():
    # Get the two strings from the request body
    string1 = request.json["bucket"]
    string2 = request.json["path"]
    req = request.get_json()
    json_payload = json.dumps(req)
    json_payload = str.encode(json_payload)
		# push data into INFERENCE TOPIC
    payload = json.loads(json_payload)
    paths = payload['path']

    file_names = payload ['file_name']
    bucket = payload['bucket']
    archive_name = payload['archive_name']
    #total_number_of_files = json.loads(json_payload.value)['total_number_of_files']
    total_number_of_files = payload['total_number_of_files']
    length = len(paths)
    i = 0
    # Iterating using while loop
    while i < length:
        print(paths[i])
        print(file_names[i])
        json_producer = {
          "bucket": bucket,
          "path" : paths[i],
          "file_name" : file_names[i],
          "archive_name" : archive_name,
          "total_number_of_files" : total_number_of_files
        }
        json_object = json.dumps(json_producer)
        json_bytes = json_object.encode()
        producer.send("string-topic", json_bytes)
        producer.flush()
        i += 1
    #produce_message(producer, "string-topic", b"Hello, world!")

    print("Sent into kafka")
    return jsonify({
        "message": "Your file(s) were added to the queue", 
        "status": "Success"})

@app.route("/download", methods=["GET"])
def download():
  
    consumer = KafkaConsumer('string-topic', bootstrap_servers = 'kafka:9092', group_id='archival1')

    # Get the two strings from the request body
    try: 
        message = consumer.poll(10.0)

        if not message:
            time.sleep(120) # Sleep for 2 minutes

        if message.error():
            print(f"Consumer error: {message.error()}")
        print(f"Received message: {message.value().decode('utf-8')}")
    except Exception as e: 
      print( repr(e))
        # Handle any exception here
    finally:
      consumer.close()
      #print("Goodbye")
  
    messages = consumer.poll()
    print(messages)
    for topic, message in messages.items():
        return jsonify(message[0].value)

if __name__ == "__main__":
    app.run(host="0.0.0.0")

