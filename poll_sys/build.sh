#!/bin/bash
set -o errexit

# pip install -r requirements.txt

python manage.py collectstatic --no-input

python manage.py migrate

# if [[ $CREATE_SUPERUSER ]]
# then
#     python manage.py createsuperuser \
#         --no-input \
#         --username "$DJANGO_SUPERUSER_USER" \
#         --email "$DJANGO_SUPERUSER_EMAIL"
# fi

# Finally, start the server
exec python manage.py runserver 0.0.0.0:8000
