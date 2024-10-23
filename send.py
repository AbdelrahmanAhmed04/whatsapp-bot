from twilio.rest import Client

# Your Account SID and Auth Token from console.twilio.com
account_sid = "AC9076f2e034e87ed36e71137fe8bc4ce9"
auth_token  = "571b81b4b3b4d6cf8bbcd27a5c5785cf"

client = Client(account_sid, auth_token)

client.messages.create(
        from_="whatsapp:+18643873878",
        body="Hello from Python!"
        to= "whatsapp:+201000947764",
)
print(message.sid)