# flask-celery-poc
POC on Flask and Celery

1. Install requirements
2. Run redis on one terminal
    ```redis-server```
3. Run celery app using:
   ```celery -A tasks worker --loglevel=info ```
4. Run application:
   ```python3 app.py```

When running application locally, make sure to change the broker and backend URL as per neccessary.

Running using Docker:

```docker-compose up --build```


When running locally,

`broker='redis://localhost:6379/0'`
`backend='redis://localhost:6379/0'`

When running using a docker-compose,

`broker='redis://redis:6379/0'`
`backend='redis://redis:6379/0'`