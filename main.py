import os

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from starlette.responses import PlainTextResponse
from twilio.rest import Client

import logging

from twilio.twiml.messaging_response import MessagingResponse

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename='app.log'
)
logger = logging.getLogger(__name__)

load_dotenv()

ACCOUNT_SID=os.getenv('ACCOUNT_SID')
AUTH_TOKEN=os.getenv('AUTH_TOKEN')
client = Client(ACCOUNT_SID, AUTH_TOKEN)


app = FastAPI()

@app.post("/whatsapp", response_class=PlainTextResponse)
async def receive_whatsapp(
        request: Request,
):
    form = await request.form()
    from_number = form.get('From')
    body = form.get('Body')

    logger.info(f'From: {from_number}, Body: {body}')

    response = MessagingResponse()
    response.message("received message")

    return str(response)
