FROM python:latest

COPY . . 

RUN pip install -r requirements.txt

EXPOSE 8000
ENV DOCKER=true

ENTRYPOINT ["uvicorn"]
CMD ["API.ItemsAPI:app", "--host", "0.0.0.0"]
#ENTRYPOINT celery \
    #-A celery_app.celery_app \
    #worker \
    #--loglevel INFO
#CMD["celery -A celery_app.celery_app worker --pool=solo -l info -Q items-queue -c 1 -E"]
#ENTRYPOINT powershell -command c:\docker\docker-entrypoint.ps1