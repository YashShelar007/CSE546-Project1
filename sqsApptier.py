import boto3
client = boto3.client('sqs')

def get_queue_url(queue_name):
    print("required Queue URL in a Dictionary")
    aws_response = client.get_queue_url(
        QueueName = queue_name,
        QueueOwnerAWSAccountId = 707951519696
    )
    return aws_response["QueueUrl"]

def get_request(queue_url):
    print("got reponse from request queue as a Dictionary")
    aws_response = client.receive_message(
        QueueUrl = queue_url,
        MaxNumberOfMessages = 20,
    )

    messages_array = aws_response["Messages"]
    response_dict = {}
    for message in messages_array:
        response_dict["messageID"] = message["MessageId"]
        response_dict["messageBody"] = message["Body"]
        response_dict["ReceiptHandle"] = message["ReceiptHandle"]

    return response_dict

def send_response(queue_url, message):
    print("sent reponse to respond queue")
    aws_response = client.send_message(
        QueueUrl = queue_url,
        MessageBody = message,
    )
    return aws_response["MessageId"]

def delete_reponse(queue_url, receipt_handle):
    print("deleted response from request queue")
    client.delete_message(
        QueueUrl = queue_url,
        ReceiptHandle = receipt_handle
    )
