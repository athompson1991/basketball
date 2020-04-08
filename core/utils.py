import csv
import os
import re
from datetime import datetime

import psycopg2

from core.settings import database_specs, CODES_FILTER

def make_create_sql(table_name, specs):
    col_list = [key + ' ' + specs[key]['dtype'] for key in specs.keys()]
    return "create table " + table_name + "(\n" + ',\n'.join(col_list) + ')'


def make_insert_sql(table_name, specs):
    colnames = specs.keys()
    cols = ',\n'.join(colnames)
    formats = ',\n'.join(['%(' + key + ')s' for key in colnames])
    return 'insert into ' + table_name + '(\n' + cols + ') values (' + formats + '\n)'


def get_codes():
    conn = psycopg2.connect(
        host=database_specs['host'],
        database=database_specs['database'],
        user=database_specs['user'],
        password=database_specs['password']
    )
    cursor = conn.cursor()
    cursor.execute("select code from games where game_date >= date('" + CODES_FILTER + "')")
    rows = cursor.fetchall()
    cursor.close()
    conn.commit()
    return [row[0] for row in rows]

def get_eids():
    conn = psycopg2.connect(
        host=database_specs['host'],
        database=database_specs['database'],
        user=database_specs['user'],
        password=database_specs['password']
    )
    cursor = conn.cursor()
    cursor.execute("select eid from events")
    rows = cursor.fetchall()
    cursor.close()
    conn.commit()
    return [row[0] for row in rows]



def datetime_to_milliseconds(dt):
    root = datetime.utcfromtimestamp(0)
    return int((dt - root).total_seconds() * 1000)
