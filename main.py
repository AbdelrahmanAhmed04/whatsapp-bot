import os
import re
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


#Content template SIDs
offer_message = "HXa2fee0b7ea14d1e8439c12f3cdf89738"
offer_list = "HXc1fc035b2d18fd509cdfec11c42ed0dc"
betfinal_check_registration = "HX218d8de3f93f3e050264272c496bbd5e"
casino_888_check_registration = "HX84da6ba9ab8b2e5d7a17fa8223a9583a"
betinal_offer = "HXaef0a489a0439eb52b98ebd204234ae3"
registration_success_followup = "HX41554486f2e99df288ff117777f1e2a9"
casino_888_offer = "HXe0d3ebb6249757ea114d7e5eeefea201"

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
    message_status = request.form.get('SmsStatus')
    list_id = request.form.get('ListId')
    error_code = request.form.get('ErrorCode')
    error_message = request.form.get('ErrorMessage')
    error_status = request.form.get('MessageStatus')
    sms_sid = request.form.get('SmsSid')
    

####SETTING UP CUSTOM COMMANDS####

    if "run algorithm send messages auto" in message_body:

        pattern = r'\+\d+'
        phone_numbers = re.findall(pattern, message_body)

        # Function to send a message to a list of numbers
        for number in phone_numbers:
            message = client.messages.create(
                from_="whatsapp:+18643873878",
                to=f"whatsapp:{number}",  # Each number should be prefixed with 'whatsapp:'
                content_sid=offer_message,
            )
            time.sleep(1)
            message = client.messages.create(
                from_="whatsapp:+18643873878",
                to=f"whatsapp:{number}",  # Each number should be prefixed with 'whatsapp:'
                content_sid=offer_list,
            )
            log_message_in_dynamodb(number, "sent automated welcome message!", "outgoing", message.sid,
                                        profile_name, to_number)
            logging.info(f"Message sent to {number}")

    
    if "send custom message to number" in message_body:

        def process_custom_message(message_body):
            # Regular expression to extract phone number and message
            pattern = r"send custom message to number (\+\d+)\s(.+)"
            match = re.match(pattern, message_body)

            phone_number = match.group(1)
            custom_message = match.group(2)

            client.messages.create(
                from_="whatsapp:+18643873878",
                to=f"whatsapp:{phone_number}",  # Each number should be prefixed with 'whatsapp:'
                body=custom_message,
            )
            log_message_in_dynamodb(phone_number, "sent manual message", "outgoing", message_sid, profile_name, to_number)
        process_custom_message(message_body)
        # Send the message via Twilio

    if "send 888 offer message" in message_body:

        pattern = r'\+\d+'
        phone_numbers = re.findall(pattern, message_body)

        # Function to send a message to a list of numbers
        for number in phone_numbers:
            message = client.messages.create(
                from_="whatsapp:+18643873878",
                to=f"whatsapp:{number}",  # Each number should be prefixed with 'whatsapp:'
                content_sid=casino_888_offer,
            )
            time.sleep(1)
            message = client.messages.create(
                from_="whatsapp:+18643873878",
                to=f"whatsapp:{number}",  # Each number should be prefixed with 'whatsapp:'
                content_sid=casino_888_check_registration,
            )
            log_message_in_dynamodb(from_number, "sent casino 888 offer message manually", "outgoing", message.sid, profile_name, to_number)

            logging.info(f"Message sent to {number}")

    if "send betfinal offer message" in message_body:

        pattern = r'\+\d+'
        phone_numbers = re.findall(pattern, message_body)

        # Function to send a message to a list of numbers
        for number in phone_numbers:
            message = client.messages.create(
                from_="whatsapp:+18643873878",
                to=f"whatsapp:{number}",  # Each number should be prefixed with 'whatsapp:'
                content_sid=betinal_offer,
            )
            time.sleep(1)
            message = client.messages.create(
                from_="whatsapp:+18643873878",
                to=f"whatsapp:{number}",  # Each number should be prefixed with 'whatsapp:'
                content_sid=betfinal_check_registration,
            )
            log_message_in_dynamodb(from_number, "sent casino betfinal offer message manually", "outgoing", message.sid, profile_name, to_number)
            logging.info(f"Message sent to {number}")
        # Send the message via Twilio
        
####CUSTOM COMMANDS DONE####


    if is_new_user(from_number):
        message = client.messages.create(
            from_="whatsapp:+18643873878",
            to=from_number,
            content_sid=offer_message,
        )
        client.messages.create(
            from_="whatsapp:+18643873878",
            to=from_number,
            content_sid=offer_list,
        )
        # Log the greeting message in DynamoDB
        log_message_in_dynamodb(from_number, "sent welcome message and offer list", "outgoing", message_sid, profile_name, to_number)


    if list_id == "1":
        message = client.messages.create(
            from_="whatsapp:+18643873878",
            to=from_number,
            body="احد خبرائنا سيتواصلون معك في اسرع وقت",
        )
        log_message_in_dynamodb(from_number, "One of our agents will contact you", "outgoing", message.sid, profile_name, to_number)
    elif list_id == "2":
        message = client.messages.create(
        from_="whatsapp:+18643873878",
        to=from_number,
        content_sid=casino_888_offer
        )        
        log_message_in_dynamodb(from_number, "Sent Casino 888 offer", "outgoing", message.sid, profile_name, to_number)
        time.sleep(2)
        message = client.messages.create(
        from_="whatsapp:+18643873878",
        to=from_number,
        content_sid=casino_888_check_registration
        )
        log_message_in_dynamodb(from_number, "Check casino 888 registration", "outgoing", message.sid, profile_name, to_number)

    elif list_id == "liked first casino 888":
        message = client.messages.create(
        from_="whatsapp:+18643873878",
        to=from_number,
        content_sid=registration_success_followup
        )        
        log_message_in_dynamodb(from_number, list_id, "outgoing", message.sid, profile_name, to_number)
    
    elif list_id == "didn't liked first casino 888":
        message = client.messages.create(
        from_="whatsapp:+18643873878",
        to=from_number,
        content_sid=betinal_offer
        )
        log_message_in_dynamodb(from_number, "Sent Casino betfinal offer", "outgoing", message.sid, profile_name, to_number)
        time.sleep(2)
        message = client.messages.create(
        from_="whatsapp:+18643873878",
        to=from_number,
        content_sid=betfinal_check_registration
        )        
        log_message_in_dynamodb(from_number, "Check casino betfinal registration", "outgoing", message.sid, profile_name, to_number)
    elif list_id == "liked second casino betfinal":
        message = client.messages.create(
        from_="whatsapp:+18643873878",
        to=from_number,
        content_sid=registration_success_followup
        )
        log_message_in_dynamodb(from_number, list_id, "outgoing", message.sid, profile_name, to_number)

    elif list_id == "didn't liked second casino betfinal":
        message = client.messages.create(
            from_="whatsapp:+18643873878",
            to=from_number,
            body="احد خبرائنا سيتواصلون معك في اسرع وقت",
        )


    # if sms_sid or error_code or error_message or error_status:
    #     log_message_in_dynamodb(to_number, error_code, error_status , sms_sid, error_message, from_number)

    if message_status =='received':
        log_message_in_dynamodb(from_number, message_body, "incoming", message_sid, profile_name, to_number)

    return "Message sent", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)