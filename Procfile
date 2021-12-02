web: gunicorn kairos_medical_center.wsgi --log-file -
worker: celery -A kairos_medical_center worker -l INFO -P gevent