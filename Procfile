web: python manage.py migrate --noinput && python manage.py popular_pets --force && gunicorn totem.wsgi --bind 0.0.0.0:$PORT --log-file -
