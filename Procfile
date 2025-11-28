release: python manage.py makemigrations && python manage.py migrate
web: python manage.py popular_pets --force && gunicorn totem.wsgi --bind 0.0.0.0:$PORT --log-file -
