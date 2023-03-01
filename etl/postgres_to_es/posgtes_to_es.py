import datetime
import os
import time
import logging

import psycopg2
import elasticsearch
import elasticsearch.helpers
from dotenv import load_dotenv
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor
from etl.postgres_to_es.schema import SchemaInformFilms
from etl.postgres_to_es.backoff import backoff
from etl.postgres_to_es import sql_requests
from contextlib import closing


logging.basicConfig(level=logging.INFO, filename='es_log.log', filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S')


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


def update(es, i_data, id):
    edit_author1 = {"id": i_data["id"],
                    "imdb_rating": i_data["imdb_rating"],
                    "genre": i_data["genre"],
                    "title": i_data["title"],
                    "description": i_data["description"],
                    "director": i_data["director"],
                    "actors_names": i_data["actors_names"],
                    "writers_names": i_data["writers_names"],
                    "actors": i_data["actors"],
                    "writers": i_data["writers"]
                    }
    res = es.index(index='movies', id=id, body=edit_author1)
    logging.info(res)


def es_search(es, data):
    for i_data in data['mappings']:
        res = es.search(index="movies", query={"match": {"id": i_data['id']}})
        if res['took'] > 0:
            update(es, i_data, i_data['id'])


def save_elastic(es, data):
    resp = elasticsearch.helpers.bulk(es, data['mappings'], index='movies')
    logging.info(resp)


def conversion_string(result: list):
    for i_result in result:
        for i_status in ['director', 'actors_names', 'writers_names']:
            str_values = ", ".join(i['name'] for i in i_result[i_status])
            i_result[i_status] = str_values


def load_from_posgre(pg_conn: _connection, es: elasticsearch, package_limit: int, date_update):
    with pg_conn.cursor() as cursor_pg:
        if date_update == '1970-01-01':
            cursor_pg.execute(sql_requests.initial_loading, (date_update,))
        else:
            cursor_pg.execute(sql_requests.checking_new_records,
                              (date_update, date_update, date_update, date_update, date_update,))
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


def update_es(pg_conn: _connection, es: elasticsearch, date_update):
    list_updates = []
    with pg_conn.cursor() as cursor_pg:
        for sql_request in [sql_requests.changing_entry_film_work,
                  sql_requests.changing_entry_person,
                  sql_requests.changing_entry_genre]:
            cursor_pg.execute(sql_request, (date_update, ))
            key = [column[0] for column in cursor_pg.description]
            data = cursor_pg.fetchall()
            if data:
                result = []
                for row in data:
                    result.append(dict(zip(key, row)))
                conversion_string(result)
                schema_films = SchemaInformFilms(mappings=result)
                list_updates.extend(data)
        es_search(es=es, data=schema_films.dict())



@backoff()
def connect_db(date_update):
    dsl = {'dbname': os.environ.get('DB_NAME'), 'user': os.environ.get('DB_USER'),
           'password': os.environ.get('DB_PASSWORD'), 'host': os.environ.get('HOST'), 'port': 5432}
    with closing(psycopg2.connect(**dsl, cursor_factory=DictCursor)) as pg_conn, \
            closing(elasticsearch.Elasticsearch(os.environ.get('HOST_ES'), http_compress=True)) as es:
        load_from_posgre(pg_conn=pg_conn, es=es, package_limit=15, date_update=date_update)
        if date_update != '1970-01-01':
            update_es(pg_conn=pg_conn, es=es, date_update=date_update)


if __name__ == '__main__':
    date_update = '1970-01-01'
    while True:
        try:
            connect_db(date_update=date_update)
            date_update = datetime.datetime.now()
            time.sleep(60)
        except:
            time.sleep(60)
