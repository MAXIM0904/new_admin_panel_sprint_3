import os

import elasticsearch
from dotenv import load_dotenv
from postgres_to_es.backoff import logging

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


settings = {
    "refresh_interval": "1s",
    "analysis": {
        "filter": {
            "english_stop": {
                "type": "stop",
                "stopwords": "_english_"
            },
            "english_stemmer": {
                "type": "stemmer",
                "language": "english"
            },
            "english_possessive_stemmer": {
                "type": "stemmer",
                "language": "possessive_english"
            },
            "russian_stop": {
                "type": "stop",
                "stopwords": "_russian_"
            },
            "russian_stemmer": {
                "type": "stemmer",
                "language": "russian"
            }
        },
        "analyzer": {
            "ru_en": {
                "tokenizer": "standard",
                "filter": [
                    "lowercase",
                    "english_stop",
                    "english_stemmer",
                    "english_possessive_stemmer",
                    "russian_stop",
                    "russian_stemmer"
                ]
            }
        }
    }
}

mappings = {
    "dynamic": "strict",
    "properties": {
        "id": {
            "type": "keyword"
        },
        "imdb_rating": {
            "type": "float"
        },
        "genre": {
            "type": "keyword"
        },
        "title": {
            "type": "text",
            "analyzer": "ru_en",
            "fields": {
                    "raw": {
                        "type":  "keyword"
                    }
            }
        },
        "description": {
            "type": "text",
            "analyzer": "ru_en"
        },
        "director": {
            "type": "text",
            "analyzer": "ru_en"
        },
        "actors_names": {
            "type": "text",
            "analyzer": "ru_en"
        },
        "writers_names": {
            "type": "text",
            "analyzer": "ru_en"
        },
        "actors": {
            "type": "nested",
            "dynamic": "strict",
            "properties": {
                    "id": {
                        "type": "keyword"
                    },
                "name": {
                        "type": "text",
                        "analyzer": "ru_en"
                        }
            }
        },
        "writers": {
            "type": "nested",
            "dynamic": "strict",
            "properties": {
                    "id": {
                        "type": "keyword"
                    },
                "name": {
                        "type": "text",
                        "analyzer": "ru_en"
                        }
            }
        }
    }
}

es = elasticsearch.Elasticsearch(os.environ.get('HOST_ES'))
resp = es.info()

try:
    es.indices.create(index='movies', settings=settings, mappings=mappings)
    logging.info(True, 'Индекс успешно создан.')
    print('Индекс успешно создан.')
except elasticsearch.RequestError as err:
    logging.info(err)
finally:
    es.close()
