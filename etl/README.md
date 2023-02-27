Для запуска приложения необходимо:
1. Создать в папке etl/postgres_to_es файл с названием .env
2. В файле .env создать и заполнить переменные DB_NAME, DB_USER, DB_PASSWORD, HOST, 
HOST_ES - формат http://127.0.0.1:9200.
3.Перейти в каталог etl командой:
- cd etl
4.Выполнить запуск докера
docker-compose up --build
5.Запустить выполнение файла create_elastic_index.py. Указанный файл создаст индексы. В случае использования curl 
код для создания индексов можно взять из elasticsearch.txt.
6. Запустить файл posgtes_to_es.py.
