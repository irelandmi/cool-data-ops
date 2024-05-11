import boto3
import os
import uuid
import json
from datetime import datetime

# Lambda function to generate a unique file name
generate_unique_filename = lambda: f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4()}.txt"



# Initialize the SQS client
sqs = boto3.client('sqs')
s3 = boto3.client('s3')

def lambda_handler(event, context):
    
    # URL of the SQS queue
    queue_url = "enter sqs url here"
    
    # Retrieve the ApproximateNumberOfMessages attribute
    response = sqs.get_queue_attributes(
        QueueUrl=queue_url,
        AttributeNames=['ApproximateNumberOfMessages']
    )
    
    # Extract the approximate number of messages
    num_messages = response['Attributes']['ApproximateNumberOfMessages']
    print(f"Total Messages Available: {num_messages}")
    
    responses = []
    messages = []
    count = 0
    while int(num_messages) > 10:
        count += 1
        print(f"Loop: {count}")
        # Receive a message from the SQS queue
        response = sqs.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=10,  # Adjust as needed
            WaitTimeSeconds=1
        )

        # Check if the queue is empty
        if 'Messages' not in response:
            print("Queue is now empty.")
            break
        
        # Example of usage
        unique_filename = generate_unique_filename()
        
        body = []
        for i in response["Messages"]:
            body.append(i["Body"])
        
        responses.append(body)
        
        # Process and delete the messages
        for message in response['Messages']:
            # Process the message (optional)
            print("Processing message: ", message['Body'])
            messages.append(message['ReceiptHandle'])
        
        # Retrieve the ApproximateNumberOfMessages attribute
        response = sqs.get_queue_attributes(
            QueueUrl=queue_url,
            AttributeNames=['ApproximateNumberOfMessages']
        )
        
        # Extract the approximate number of messages
        num_messages = response['Attributes']['ApproximateNumberOfMessages']
        print(f"Total Messages Available: {num_messages}")
            
    # Writing to S3
    s3.put_object(
        Bucket='bucket name here',  # Replace with your S3 bucket name
        Key=f"messages/bulk-{unique_filename}.json",
        Body=json.dumps(responses)
    )
    
    for m in messages:
        # Delete the message from the queue
        sqs.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=m
        )

    return {
        'statusCode': 200,
        'body': 'Queue emptied successfully'
    }
