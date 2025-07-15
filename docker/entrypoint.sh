#!/bin/sh

set -e

# Django migrations
python manage.py migrate

# Create superuser account
python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username="${DJANGO_SUPERUSER_USERNAME}").exists():
    User.objects.create_superuser(
        username="${DJANGO_SUPERUSER_USERNAME}",
        email="${DJANGO_SUPERUSER_EMAIL}",
        password="${DJANGO_SUPERUSER_PASSWORD}"
    )
EOF

# # Load fake data
# python manage.py populate --user --is-staff
# python manage.py populate --author
# python manage.py populate --quote

# # Lancer le serveur de developpement de Django
# python manage.py runserver 0.0.0.0:8000

# Run the app with Gunicorn
echo "Starting Gunicorn..."
exec gunicorn server.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --timeout 120 \
    --log-level info
