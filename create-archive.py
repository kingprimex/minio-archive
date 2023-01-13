import asyncio
import aiokafka
import boto3
import json
import zipfile

async def download_file_from_s3(s3_client, bucket_name, path):
    # Download the file asynchronously using aiohttp
    async with session.get(f"https://{bucket_name}.s3.amazonaws.com/{path}") as response:
        data = await response.read()
        # Save the downloaded file to disk
        with open(path, "wb") as f:
            f.write(data)

def create_archive(files):
    # Create a ZIP file
    zip = zipfile.ZipFile('/home/user/a/b/c/test.zip','a')
    zip.write('/home/user/a/b/c/1.txt')
    zip.close()

    with zipfile.ZipFile("/tmp/archive.zip", "w") as zipf:
        # Add each file to the ZIP archive
        for file in files:
            zipf.write(file)

def send_email(to, subject, body):
    # TODO: Implement this function to send an email with the given subject and body to the given email address
    pass

async def consume_messages(consumer):
    # Consume messages from the Kafka topic asynchronously
    async for msg in consumer:
        # Parse the message as JSON
        message = json.loads(msg.



