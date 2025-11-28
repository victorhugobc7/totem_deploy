web: python manage.py migrate && python manage.py popular_pets && python manage.py collectstatic --noinput && gunicorn totem.wsgi --bind 0.0.0.0:$PORT --log-file -
