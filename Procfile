web: gunicorn gridgaming.wsgi --workers 6
worker: python manage.py rqworker high low default --worker-class rq.SimpleWorker
background: python manage.py process_tasks


# DONT USE PRELOAD
#web: gunicorn gridgaming.wsgi --preload --workers 3
#worker: python manage.py rqworker high low default --with-scheduler
#worker: python run-worker.py


#worker: python manage.py rqworker high low default --with-scheduler

#worker: python manage.py rqworker high low default --worker-class rq.SimpleWorker
#worker: python manage.py rqworker high low default --worker-class rq.HerokuWorker
