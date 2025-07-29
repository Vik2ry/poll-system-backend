set -o errexit

pip install -r requirements.txt

python poll_sys/manage.py collectstatic --no-input

python poll_sys/manage.py migrate


# if [[ $CREATE_SUPERUSER ]]
# then
#     python manage.py createsuperuser --no-input
# fi