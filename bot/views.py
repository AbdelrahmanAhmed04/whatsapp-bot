from django.http.response import HttpResponse
from django.shortcuts import render
from twilio.rest import Client
from django.views.decorators.csrf import csrf_exempt
import json
# Create your views here.

account_sid = '###########'
auth_token = '###########'
client = Client(account_sid, auth_token)
welcome_message = "HXfdf3119d45c9eddb40ed53c15e3a1716"
offer_message = "HXbe7bee6c57059a6db3c916ee3bd8ee49"
offer_list = "HXc1fc035b2d18fd509cdfec11c42ed0dc"
abdul2="whatsapp:+201552750504"

# client.messages.create(
#         from_="whatsapp:+18643873878",
#         content_sid= welcome_message,
#         content_variables=json.dumps(
#         {
#             "username": "Hola",
#         }
#     ),
#         to= abdul2,
# )
client.messages.create(
        from_="whatsapp:+18643873878",
        content_sid=offer_message,
        to= abdul2,
)
client.messages.create(
        from_="whatsapp:+18643873878",
        content_sid=offer_list,
        to= abdul2,
)

@csrf_exempt
def bot(request):
    # message = request.POST["Body"]
    listId = request.POST["ListId"]
    # print(listId)
    # senderName = request.POST["ProfileName"]
    senderNumber = request.POST["From"]    

    if listId == "1":
        client.messages.create(
        from_="whatsapp:+18643873878",
        body="احد خبرائنا سيتواصلون معك في اسرع وقت",
        to= senderNumber,
)
    if listId == "2":
        client.messages.create(
        from_="whatsapp:+18643873878",
        body="إليك لينك العلاوة",
        to= senderNumber,
)
    return HttpResponse("hello")


