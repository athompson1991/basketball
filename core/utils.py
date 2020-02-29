import re
import csv
from datetime import datetime
import os

import psycopg2

from core.settings import database_specs


def get_most_recent_scrape(target_dir, head="games"):
    regex_pattern = '%Y-%m-%d_%H%M%S'
    regex = re.compile(r'\.csv')
    files = os.listdir(target_dir)
    csv_files = list(filter(regex.search, files))
    dates = [datetime.strptime(f, head + "_" + regex_pattern + ".csv") for f in csv_files]
    out = head + "_" +  max(dates).strftime("%Y-%m-%d_%H%M%S") + ".csv"
    return out

def get_codes(target_dir):
    most_recent_scrape = get_most_recent_scrape(target_dir)
    filename = target_dir + most_recent_scrape
    with open(filename, 'r', newline='') as f:
        reader = csv.DictReader(f)
        out = [row['code'] for row in reader]
    return out

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
    cursor.execute("select code from games")
    rows = cursor.fetchall()
    cursor.close()
    conn.commit()
    return [row[0] for row in rows]

