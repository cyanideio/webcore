#!/bin/bash
echo "清除数据..."
if [ "$MANIFEST_ENV" = "local" ]; then
	rm db.sqlite3
	rm -rf core/migrations
else
	mysql -uroot  -p21345 -Bse "
		DROP DATABASE kada_db; 
		CREATE DATABASE kada_db;
		ALTER DATABASE kada_db CHARACTER SET utf8 COLLATE utf8_general_ci;
	"	
fi;
echo "初始化..."
python manage.py migrate
python manage.py makemigrations core
python manage.py migrate core
python manage.py makemigrations kada
python manage.py migrate kada
echo "开始导入数据..."
python scripts/py/load_test_data.py
echo "导入完成..."
