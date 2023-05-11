# flask-celery-poc
POC on Flask and Celery

1. Install requirements
2. Run redis on one terminal
    ```redis-server```
3. Run celery app using:
   ```celery -A app.celery worker --loglevel=info ```
4. Run flower:
   ```celery flower --port=5555```