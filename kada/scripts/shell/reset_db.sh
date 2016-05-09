echo "Cleaning Up..."
if [$KADA_ENV == 'local']; then
	rm db.sqlite3
	rm -rf core/migrations
else
	echo "Cleaning on Server...."
	mysql -uroot  -p21345 -Bse "
		DROP DATABASE kada_db; 
		CREATE DATABASE kada_db;
		ALTER DATABASE kada_db CHARACTER SET utf8 COLLATE utf8_general_ci;
	"	
fi
echo "Initializing..."
python manage.py migrate
python manage.py makemigrations core
python manage.py migrate core
echo "Loading Data..."
python scripts/py/load_test_data.py
echo "Finished Loading Data..."

