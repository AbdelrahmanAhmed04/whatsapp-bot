#### To run
```bash
nohup gunicorn -w 4 -b 0.0.0.0:8080 main:app > gunicorn.log 2>&1 & echo $! > gunicorn.pid
```


#### To stop
```bash
kill `cat gunicorn.pid`
``` 