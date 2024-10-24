#### To start the WhatsApp bot
```bash
(note: 4 is the number of workers, so if you start receiving lot more SMS, possibly up it to 6-12)
```bash
cd whatsapp-bot
source venv/bin/activate
nohup gunicorn -w 4 -b 0.0.0.0:8080 main:app > gunicorn.log 2>&1 & echo $! > gunicorn.pid
```


#### To stop the WhatsApp bot
```bash
kill `cat gunicorn.pid`
``` 


### Conversations storage
- The conversations are stored in Amazon DynamoDB. Both the receiver and sender messages are logged