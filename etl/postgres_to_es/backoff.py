import sys
import time
import logging
from functools import wraps
import psycopg2

logging.basicConfig(level=logging.INFO, filename='es_log.log', filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S')


def print_psycopg2_exception(err):
    err_type, err_obj, traceback = sys.exc_info()
    line_num = traceback.tb_lineno
    errors_log = ("\npsycopg2 ERROR:", err, "on line number:", line_num,
                  "psycopg2 traceback:", traceback.tb_frame, "-- type:", err_type,
                  "\nextensions.Diagnostics:", err.diag,
                  "pgerror:", err.pgerror, "pgcode:", err.pgcode, "\n")
    logging.info(errors_log)
    print(errors_log)


def backoff(start_sleep_time=0.1, factor=2, border_sleep_time=10):
    def func_wrapper(func):
        @wraps(func)
        def _inner(tm=1, *args, **kwargs):
            while True:
                try:
                    return func(*args, **kwargs)
                except psycopg2.OperationalError as err:
                    print_psycopg2_exception(err)
                    logging.info(f"Потеря соединения, повтор через {tm} сек.")
                    if tm < border_sleep_time:
                        tm += (start_sleep_time * factor)
                    elif tm > border_sleep_time:
                        tm = border_sleep_time
                    time.sleep(tm)
        return _inner
    return func_wrapper
