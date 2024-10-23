from twilio.rest import Client

# Your Account SID and Auth Token from console.twilio.com
account_sid = "AC9076f2e034e87ed36e71137fe8bc4ce9"
auth_token  = "67c6417566a35b483a69adb7860b0942"

client = Client(account_sid, auth_token)

client.messages.create(
        from_="whatsapp:+18643873878",
        body="Hello from Python!",
        to= "whatsapp:+201000947764",
)
print("sent")