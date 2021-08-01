#!/bin/sh

uvicorn API.ItemsAPI:app --reload

celery -A celery_app.celery_app worker --pool=solo -l info -Q items-queue -c 1 -E