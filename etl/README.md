<h2>Проект "Перенос данных из PostgreSQL в Elasticsearch"</h2>


<h3>Реализовано в проекте:</h3>
<ul>
  <li> Валидация конфигурации происходит с помощью pydantic.</li>
  <li> Информация из PostgreSQL получана при помощи SQL-запросов.</li>
  <li> Для логирования использован модуль logging из стандартной библиотеки Python</li>
  <li> В создана модель индексов Elasticsearch, в которую должна производиться загрузка фильмов</li>
</ul>



<p>Для запуска приложения необходимо:</p>
<ol>
   <li>Создать в папке etl/postgres_to_es файл с названием .env</li>
   <li>В файле .env создать и заполнить переменные для подключения к PostgreSQL и порту Elasticsearch:</li>
      <p>DB_NAME, DB_USER, DB_PASSWORD, HOST, HOST_ES. HOST_ES - формат http://127.0.0.1:9200</p>
   <li>Перейти в каталог etl командой:</li>  
      <p>cd etl</p>
   <li>Выполнить запуск докера командой:</li>  
      <p>docker-compose up --build</p>
   <li>После установки всех пакетов необходимо копировать базу данный из файла movies_database.dump командой:</li>  
      <p>pg_restore –d name_database -h 127.0.0.1 -U name_user path\movies_database.dump</p>
      <p>Вместо name_database - наименование базы данных; name_user - имя юзера; path - абсолютный путь до файла movies_database.dump</p>
   <li>Запустить выполнение файла create_elastic_index.py. Указанный файл создаст индексы. В случае использования curl, код для создания индексов можно взять из elasticsearch.txt.</li>  
    <li>Запустить выполнение файла posgtes_to_es.py.</li> 
