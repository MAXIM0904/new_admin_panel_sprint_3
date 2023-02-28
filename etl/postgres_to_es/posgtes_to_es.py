import datetime
import os
import time

import psycopg2
import elasticsearch
import elasticsearch.helpers
from dotenv import load_dotenv
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor
from etl.postgres_to_es.schema import SchemaInformFilms
from etl.postgres_to_es.backoff import backoff
from contextlib import closing

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


def save_elastic(es, data):
    resp = elasticsearch.helpers.bulk(es, data['mappings'], index='movies')
    print(resp)


def conversion_string(result: list):
    for i_result in result:
        for i_status in ['director', 'actors_names', 'writers_names']:
            str_values = ", ".join(i['name'] for i in i_result[i_status])
            i_result[i_status] = str_values


def load_from_posgre(pg_conn: _connection, es: elasticsearch, package_limit: int, date_update):
    with pg_conn.cursor() as cursor_pg:
        cursor_pg.execute("""SELECT fw.id, fw.rating as imdb_rating, array_agg(DISTINCT g.name) as genre, 
        fw.title, fw.description,
        COALESCE (json_agg(DISTINCT jsonb_build_object('name', p.full_name))
        FILTER (WHERE pfw.role = 'director'), '[]') as director,
        COALESCE (json_agg(DISTINCT jsonb_build_object('name', p.full_name)) 
        FILTER (WHERE pfw.role = 'actor'),'[]') as actors_names,
        COALESCE (json_agg(DISTINCT jsonb_build_object('name', p.full_name)) 
        FILTER (WHERE pfw.role = 'writer'), '[]') as writers_names,
        COALESCE (json_agg(DISTINCT jsonb_build_object('id', p.id, 'name', p.full_name))
        FILTER (WHERE pfw.role = 'actor'), '[]') as actors, 
        COALESCE (json_agg(DISTINCT jsonb_build_object('id', p.id, 'name', p.full_name))
        FILTER (WHERE pfw.role = 'writer'), '[]') as writers
        FROM content.film_work fw
        LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
        LEFT JOIN content.person p ON p.id = pfw.person_id
        LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
        LEFT JOIN content.genre g ON g.id = gfw.genre_id GROUP BY fw.id
        HAVING fw.created > (%s) ORDER BY fw.modified;""", (date_update,))
        print(date_update)
        key = [column[0] for column in cursor_pg.description]
        table_records_query = cursor_pg.fetchmany(package_limit)
        while len(table_records_query) != 0:
            result = []
            for row in table_records_query:
                result.append(dict(zip(key, row)))
            conversion_string(result)
            schema_films = SchemaInformFilms(mappings=result)
            save_elastic(es=es, data=schema_films.dict())
            table_records_query = cursor_pg.fetchmany(package_limit)
    print("Копирование закончено успешно")


@backoff()
def connect_db(date_update):
    dsl = {'dbname': os.environ.get('DB_NAME'), 'user': os.environ.get('DB_USER'),
           'password': os.environ.get('DB_PASSWORD'), 'host': os.environ.get('HOST'), 'port': 5432}
    with closing(psycopg2.connect(**dsl, cursor_factory=DictCursor)) as pg_conn, \
            closing(elasticsearch.Elasticsearch(os.environ.get('HOST_ES'), http_compress=True)) as es:
        load_from_posgre(pg_conn=pg_conn, es=es, package_limit=15, date_update=date_update)


if __name__ == '__main__':
    date_update = '1970-01-01'
    while True:
        try:
            connect_db(date_update=date_update)
            date_update = datetime.datetime.now()
            time.sleep(60)
        except:
            time.sleep(60)
