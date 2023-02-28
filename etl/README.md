Для запуска приложения необходимо:
1. Создать в папке etl/postgres_to_es файл с названием .env
2. В файле .env создать и заполнить переменные DB_NAME, DB_USER, DB_PASSWORD, HOST, 
HOST_ES - формат http://127.0.0.1:9200.
3.Перейти в каталог etl командой:
- cd etl
4.Выполнить запуск докера
docker-compose up --build
5. После установки всех пакетов необходимо копировать базу данный из файла movies_database.dump командой
pg_restore –d name_database -h 127.0.0.1 -U name_user path\movies_database.dump
Вместо name_database - поставить имя базы, name_user - имя пользователя, path - путь до файла movies_database.dump
6.Запустить выполнение файла create_elastic_index.py. Указанный файл создаст индексы. В случае использования curl 
код для создания индексов можно взять из elasticsearch.txt.
7.Запустить файл posgtes_to_es.py.
