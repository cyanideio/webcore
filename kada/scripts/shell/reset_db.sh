echo "Cleaning Up..."
rm db.sqlite3
rm -rf core/migrations
echo "Initializing..."
python manage.py migrate
python manage.py makemigrations core
python manage.py migrate core
echo "Loading Data..."
python scripts/py/load_test_data.py
echo "Finished Loading Data..."

