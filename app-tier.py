import boto3
import json
import os
import subprocess

access_key = ''
secret_key = ''

def get_sqs_url(queue_name):
    sqs_client = boto3.client("sqs", region_name = "us-east-1", aws_access_key_id=access_key, aws_secret_access_key=secret_key)
    name = queue_name
    queue_name = sqs_client.get_queue_url(
        QueueName = name
    )
    return queue_name["QueueUrl"]

def read_message(queue_url):
    file = open('read_message.txt', 'a')
    response = []
    sqs_client = boto3.client("sqs", region_name = "us-east-1", aws_access_key_id=access_key, aws_secret_access_key=secret_key)
    response = sqs_client.receive_message(
        QueueUrl = queue_url,
        MaxNumberOfMessages =1, 
        WaitTimeSeconds=10,
    )
    file.write(f"Read message {response}\n")
    if len(response.get("Messages", []))>0:
        file.write(f"Message not empty\n")
        for message in response.get("Messages", []):
            message_body = message["Body"]
            message_reciet = message["ReceiptHandle"]
        file.write(f"Message body: {message_body}\n")
        file.close()
        return message_body, message_reciet
    else:
        file.close()
        return None, None
    
def download_images_from_s3(s3_bucket_name, image_name):
    session = boto3.session.Session(aws_access_key_id=access_key, aws_secret_access_key=secret_key)
    s3_resource = session.resource("s3")
    file_name = '/home/ubuntu/images/' + image_name
    s3_resource.meta.client.download_file(s3_bucket_name,image_name,file_name)

def classify_images(image_name):
    path = '/home/ubuntu/images/' + image_name
    image_file_name = image_name.split(".")[0]
    filename = '/home/ubuntu/result/'+ image_file_name + '.txt'
    subprocess.run(['touch', filename])
    output_file = open(filename, "w")
    subprocess.run(('python3', './image_classification.py', path ), stdout=output_file)

def write_message_to_response(queue_url, message_body):
    sqs_client = boto3.client("sqs", region_name = "us-east-1", aws_access_key_id=access_key, aws_secret_access_key=secret_key)
    message = message_body
    response = sqs_client.send_message(
        QueueUrl = queue_url,
        MessageBody = json.dumps(message)
    )
   
    return response['ResponseMetadata']["HTTPStatusCode"]

def send_classification_result_to_response_queue(image_name, queue_url):
    image_file_name = image_name.split(".")[0]
    file_name = '/home/ubuntu/result/'+ image_file_name + '.txt'
    with open (file_name,'r') as f:
        lines = f.readline()
    lines = lines.split("\n")
    message_body = lines[0].split(",")[1]
    sqs_message = image_name + ":" + message_body
    write_message_to_response(queue_url, sqs_message )

def write_response_to_bucket(s3_bucket_name, image_name):
    image_file_name = image_name.split(".")[0]
    result_file = '/home/ubuntu/result/'+ image_file_name + '.txt'
    with open (result_file, 'r') as f:
        lines = f.readline()
    lines = lines.split("\n")
    message_body = image_name + "," + lines[0].split(",")[1]
    s3_client = boto3.client("s3", aws_access_key_id=access_key, aws_secret_access_key=secret_key)
    s3_client.put_object(Bucket = s3_bucket_name, Body=message_body, Key = image_name)

def delete_message_from_resuest_queue(queue_url,receipt_handle):
    sqs_client = boto3.client("sqs", region_name = "us-east-1", aws_access_key_id=access_key, aws_secret_access_key=secret_key)
    response = sqs_client.delete_message(
        QueueUrl = queue_url,
        ReceiptHandle=receipt_handle,
    )
    return response["ResponseMetadata"]["HTTPStatusCode"]

def delete_image(image_name):
    file_path = "/home/ubuntu/images/" + image_name
    if os.path.exists(file_path):
        os.remove(file_path)
    else:
        print("The file does not exist")
    return True

if __name__=="__main__":
    try:
        with open ('access.txt', 'r') as f:
            access_key = f.readline()

        with open ('secret.txt', 'r') as f:
            secret_key = f.readline()

        file = open('output_results.txt', 'a')
        request_queue_url = get_sqs_url('cloudCrowd-request')
        response_queue_url = get_sqs_url('cloudCrowd-response')

        input_bucket = "cloudcrowd-input546"
        output_bucket = "cloudcrowd-output546"
        file.write(f"Request-> {request_queue_url} response-> {response_queue_url}\n")

        while (True):
            image_name, reciept_handle = read_message(request_queue_url)
            if image_name!=None and reciept_handle!=None :
                file.write(f"Got message: {image_name}\n")
                download_images_from_s3(input_bucket, image_name)
                classify_images(image_name)
                send_classification_result_to_response_queue(image_name, response_queue_url)
                write_response_to_bucket(output_bucket, image_name)
                delete_message_from_resuest_queue(request_queue_url, reciept_handle)
                delete_image(image_name)
            else:
                file.write("No images left in the queue")
                break
        
        file.close()
    except Exception as e:
        file = open('errors.txt', 'a')
        file.write(f"Found error {e}")
        file.close()
