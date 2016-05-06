rm db.sqlite3
rm -rf core/migrations
python manage.py migrate
python manage.py makemigrations core
python manage.py migrate core
python manage.py createsuperuser
