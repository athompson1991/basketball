import os

import jinja2
import pandas as pd
import psycopg2
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm
from matplotlib.cm import get_cmap

from core.settings import database_specs

pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)



client2 = psycopg2.connect(
    host=database_specs['host'],
    database=database_specs['database'],
    user=database_specs['user'],
    password=database_specs['password']
)

cursor = client2.cursor()
cursor.execute('select * from games')
# print("helloi world")
cursor.close()


latex_jinja_env = jinja2.Environment(
    block_start_string="\BLOCK{",
    block_end_string="}",
    variable_start_string="\VAR{",
    variable_end_string="}",
    comment_start_string="\#{",
    comment_end_string="}",
    line_statement_prefix="%-",
    line_comment_prefix="%#",
    trim_blocks=True,
    autoescape=False,
    loader=jinja2.FileSystemLoader(os.path.abspath("."))
)

template = latex_jinja_env.get_template("analysis/document/doc.tex")
document = template.render(place="Seattle")

with open("analysis/document/doc_render.tex", "w") as output:
    output.write(document)

conn = psycopg2.connect(
    host="localhost",
    database="sports",
    user="postgres",
    password=open("core/password").read()
)

cursor = conn.cursor()
cursor.execute(
    """
    select *
    from pbp 
    where 
      code = '201906020TOR'
      and score_change is not null
     order by seconds_into_game
    """
)
rows = cursor.fetchall()
cursor.close()
conn.commit()


df = pd.DataFrame(rows)
df.columns = database_specs['tables']['pbp'].keys()
df['t'] = df['seconds_into_game'] / 2880

def p_funk(score, t, mu=0.55, sigma_squared=2):
    return norm.cdf((score + (1 - t) * mu) / np.sqrt(((1-t) * sigma_squared)))

df['probability'] = p_funk(df['score_diff'], df['t'], 0, 10*10)

df_continuous = pd.DataFrame({'seconds_into_game': list(range(0, 2880))})
df_continuous['t'] = df_continuous['seconds_into_game'] / 2880
df_continuous = df_continuous.merge(df[['score_diff', 'seconds_into_game']], on='seconds_into_game', how='left')
df_continuous['score_diff'][0] = 0
df_continuous['filled_score_diff'] = df_continuous['score_diff'].fillna(method="ffill")


over_under = -2.5
var = 16*16
for i in range(-10, 12, 2):
    plt.plot(df_continuous['t'], p_funk(i, df_continuous['t'], over_under, var), color=((i+10) / 22, 0, 1 - ((i+10) / 22)))
plt.plot(df_continuous['t'], p_funk(df_continuous['filled_score_diff'], df_continuous['t'], over_under, var), color="green")
plt.legend(labels=[str(i) + "pt lead" for i in range(-10, 12, 2)] + ["In-Game"], loc="lower left", ncol=5)
plt.title("Golden State Warriors Vs Toronto Raptors, June 2 2019")
plt.ylabel("Probability of Win")
plt.xlabel("Time")


plt.plot(df['t'], plt.plot(df['t'], p_funk(df['score_diff'], df['t'], over_under, 16*16)))

# Shotchart logic

logic_1 = (df['shot_type'] == '2-pointer') & df['made_shot']
logic_2 = (df['shot_type'] == '2-pointer') & np.logical_not(df['made_shot'])
plt.scatter(df[logic_1]['x'], df[logic_1]['y'], alpha=0.4)
plt.scatter(df[logic_2]['x'], df[logic_2]['y'], alpha=0.4, color='red')

