import os
from celery import Celery

celery_app = Celery(
        "worker",
        broker="redis://redis:6379/0",
        backend="redis://redis:6379/1",
        include=["celery_app.tasks"],
                  )

#if not bool(os.getenv("DOCKER")):  # running example without docker
#    celery_app = Celery(
#        "worker",
#        broker="redis://localhost:6379/0",
#        backend="redis://localhost:6379/1",
#        include=["celery_app.tasks"],
#    )
#else:  # running example with docker
#    celery_app = Celery(
#        "worker",
#        broker="redis://redis:6379/0",
#        backend="redis://redis:6379/1",
#        include=["celery_app.tasks"],
#    )


