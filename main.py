import os
import time
from datetime import datetime

import boto3
from boto3.dynamodb.conditions import Key
from flask import Flask, request
from twilio.rest import Client
from dotenv import load_dotenv
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

load_dotenv()

# Get Twilio credentials from environment variables
account_sid = os.getenv('ACCOUNT_SID')
auth_token = os.getenv('AUTH_TOKEN')
client = Client(account_sid, auth_token)

# Get AWS credentials from environment variables
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
aws_region = 'us-east-2'

offer_message = "HXbe7bee6c57059a6db3c916ee3bd8ee49"
offer_list = "HXc1fc035b2d18fd509cdfec11c42ed0dc"


# Initialize DynamoDB resource with credentials
dynamodb = boto3.resource(
    'dynamodb',
    region_name=aws_region,
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key
)


# Specify your table
table = dynamodb.Table('conversations')

def is_new_user(customer_id):
    # Query DynamoDB to check if the user exists
    response = table.query(
        KeyConditionExpression=Key('customer_id').eq(customer_id)
    )
    return not bool(response['Items'])


def log_message_in_dynamodb(customer_id, message, direction, message_sid, profile_name, to_number):
    # Prepare the item to be inserted into DynamoDB
    item = {
        'customer_id': customer_id,     # Partition Key (sender's phone number)
        'timestamp': datetime.utcnow().isoformat(),  # Sort Key (current timestamp)
        'message': message,             # The actual message
        'direction': direction,         # Direction (incoming or outgoing)
        'message_sid': message_sid,     # Unique identifier for the message
        'profile_name': profile_name,   # WhatsApp profile name
        'to_number': to_number          # Recipient's phone number (your Twilio number)
    }

    # Insert the item into DynamoDB
    table.put_item(Item=item)

    # Log success
    logging.info(f"{direction.capitalize()} message from {customer_id} logged to DynamoDB.")

def is_new_user(customer_id):
    # Query DynamoDB to check if the user exists
    response = table.query(
        KeyConditionExpression=Key('customer_id').eq(customer_id)
    )
    return not bool(response['Items'])


@app.route("/whatsapp", methods=['POST'])
def whatsapp_reply():
    # logging.info(f"Raw Data: {request.data}")
    # logging.info(f"Form Data: {request.form}")
    # Get the phone number from the request
    from_number = request.form.get('From')  # Sender's phone number (e.g., 'whatsapp:+1294304032')
    to_number = request.form.get('To')  # Receiver's phone number (e.g., 'whatsapp:+14155238886')
    message_body = request.form.get('Body')  # The content of the message (e.g., 'Tt')
    message_sid = request.form.get('MessageSid')  # Unique message SID
    profile_name = request.form.get('ProfileName')  # WhatsApp profile name (e.g., 'Bob')

    if is_new_user(from_number):
        message = client.messages.create(
            from_="whatsapp:+18643873878",
            to=from_number,
            content_sid=offer_message,
        )
        # Log the greeting message in DynamoDB
        log_message_in_dynamodb(from_number, message_body, "incoming", message_sid, profile_name, to_number)
        log_message_in_dynamodb(from_number, "Sent welcome mssage", "outgoing", message.sid, profile_name, to_number)
        time.sleep(2)

    list_id = request.form.get('ListId')

    if list_id == '1':
        outgoing_body = "احد خبرائنا سيتواصلون معك في اسرع وقت",
    elif list_id == '2':
        outgoing_body = "إليك لينك العلاوة"
    else:
        outgoing_body = None

    if outgoing_body:
        message = client.messages.create(
            from_="whatsapp:+18643873878",
            to=from_number,
            body=outgoing_body,
        )
        log_message_in_dynamodb(from_number, outgoing_body, "outgoing", message.sid, profile_name, to_number)
    else:
        message = client.messages.create(
            from_="whatsapp:+18643873878",
            to=from_number,
            content_sid=offer_list,
        )
        log_message_in_dynamodb(from_number, "Sent offer list", "outgoing", message.sid, profile_name, to_number)

    return "Message sent", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
