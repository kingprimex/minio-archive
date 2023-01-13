import boto3
import json
import zipfile
from contextlib import closing
from zipfile import ZipFile
from kafka import KafkaConsumer

def write_to_minio(bucket, archive):
  minio_client = boto3.client(
      's3',
      endpoint_url='http://minio:9000',
      aws_access_key_id='minio',
      aws_secret_access_key='minio123'
  )
  minio_client.upload_file(archive, bucket, 'archive'+archive)
  print('Uploaded archive to minio')


def create_archive(bucket, file_path, archive_name, total_number_of_files):
    # Create a ZIP file
    if  archive_name.endswith(".zip") == False:
      archive_name=archive_name + '.zip'
    zip = zipfile.ZipFile('/tmp/'+ archive_name,'a')
    zip.write(filename='/tmp/'+file_path, arcname=file_path )
    zip.close()
    print('Added '+ file_path +' to archive')
    with closing(ZipFile('/tmp/' + archive_name)) as archive:
      count = len(archive.infolist())
    print('Number of files in the archive is: ' + str(count))
    if count >= int(total_number_of_files):
      write_to_minio(bucket, '/tmp/' + archive_name)


def read_from_minio(bucket, file, archive_name, total_number_of_files):
  minio_client = boto3.client(
      's3',
      endpoint_url='http://minio:9000',
      aws_access_key_id='minio',
      aws_secret_access_key='minio123'
  )

  # Set the bucket name and file key
  bucket_name = bucket
  file_key = file
  file_name_list = file.split("/")
  file_name = file_name_list[-1]
  # Get the file from the Minio server
  response = minio_client.get_object(Bucket=bucket_name, Key=file_key)
  minio_client.download_file(bucket_name, file_key, '/tmp/'+file_name)
  file_contents = response['Body'].read()
  create_archive(bucket_name, file_name, archive_name, total_number_of_files)
 

if __name__ == "__main__":
    consumer = KafkaConsumer('string-topic', bootstrap_servers = 'kafka:9092', group_id='archival1')
    for message in consumer:
        read_from_minio(json.loads(message.value)['bucket'],
                        json.loads(message.value)['path'],
                        json.loads(message.value)['archive_name'],
                        json.loads(message.value)['total_number_of_files'])
