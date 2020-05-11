from datetime import datetime, timedelta

import psycopg2
import numpy as np

from core.settings import CODES_FILTER
from core.db import database_specs


def create_connection():
    return psycopg2.connect(
        host=database_specs['host'],
        database=database_specs['database'],
        user=database_specs['user'],
        password=database_specs['password']
    )

def make_create_sql(table_name, specs):
    col_list = [key + ' ' + specs[key]['dtype'] for key in specs.keys()]
    return "create table " + table_name + "(\n" + ',\n'.join(col_list) + ')'

def make_insert_sql(table_name, specs):
    colnames = specs.keys()
    cols = ',\n'.join(colnames)
    formats = ',\n'.join(['%(' + key + ')s' for key in colnames])
    return 'insert into ' + table_name + '(\n' + cols + ') values (' + formats + '\n)'

def run_query(sql):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    cursor.close()
    conn.commit()
    data = [row[0] for row in rows]
    return data

def get_codes():
    return run_query("select code from games where game_date >= date('" + CODES_FILTER + "')")

def get_eids():
    return run_query("select eid from events")

def datetime_to_milliseconds(dt):
    root = datetime.utcfromtimestamp(0)
    return int((dt - root).total_seconds() * 1000)

def generate_dates(start, end):
    datetime_start = datetime.strptime(start, '%Y-%m-%d')
    datetime_end = datetime.strptime(end, '%Y-%m-%d')
    delta = datetime_end - datetime_start
    dates = [datetime_start + timedelta(i) for i in range(delta.days)]
    return dates

def make_ms(start, end):
    dates = generate_dates(start, end)
    ms = [datetime_to_milliseconds(date) for date in dates]
    return ms

def get_implied_probability(ml):
    if ml > 0:
        return 100 / (ml + 100)
    else:
        return -ml / (-ml + 100)

def zero_to_one(x):
    return np.exp(x)/(1+np.exp(x))

def to_infinity(x):
    return np.log(x/(1-x))

def get_implied_probability_vec(ml_vec):
    return np.array([get_implied_probability(ml) for ml in ml_vec])

def join_stats(stat_df, game_df, side='home', i=1):
    stat_df = stat_df.rename(columns=lambda x: x + '_' + side + '_lag_' + str(i))
    stat_df = stat_df.assign(game_num_lag_join=stat_df['game_num_' + side + '_lag_' + str(i)] + i)
    merged = game_df.merge(
        stat_df,
        left_on=[side + '_code', side + '_game_num'],
        right_on=['team_' + side + '_lag_' + str(i), 'game_num_lag_join']
    )
    merged = merged.filter(regex='^code$|.*_' + side + '_lag')
    return merged

def join_away_and_home(stat_df, game_df, lags=[1]):
    dfs = []
    for lag in lags:
        home = join_stats(stat_df, game_df, side='home', i=lag).set_index('code')
        away = join_stats(stat_df, game_df, side='away', i=lag).set_index('code')
        dfs.append(home)
        dfs.append(away)
    game_df = game_df.set_index('code')
    game_df = game_df.join(dfs)
    return game_df
