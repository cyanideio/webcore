#!/bin/bash
echo "清除数据..."
if [ "$KADA_ENV" = "local" ]; then
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
echo "开始导入数据..."
python scripts/py/load_test_data.py
echo "导入完成..."
