import os
from datetime import timedelta, datetime

import jinja2
import pandas as pd
import psycopg2
import matplotlib.pyplot as plt
import numpy as np
from pandas.core.common import SettingWithCopyWarning
from scipy.stats import norm
from matplotlib.cm import get_cmap
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.decomposition import PCA, KernelPCA

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.manifold import LocallyLinearEmbedding, TSNE
from sklearn.metrics import confusion_matrix,  accuracy_score, precision_score, recall_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.svm import LinearSVC
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV

from core.settings import database_specs

import warnings


warnings.simplefilter(action='ignore', category=SettingWithCopyWarning)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


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


odds_query = """
with main as (
  select g.*, row_number() over (partition by g.home_team order by game_date) as game_num
  from games g
  order by home_team, game_date
),

line_moves as (
  select * from line_movements lm
),

shot_success as (
  select
    team, 
    code,
    sum(fg) as shots_made,
    sum(fga) as shots_attempted,
    (sum(fg) * 1.0000) / (sum(fga) * 1.0000) as shot_success,
    sum(orb) as offensive_rebound,
    sum(drb) as defensive_rebound,
    sum(stl) as steals,
    sum(pf) as personal_fouls,
    sum(blk) as blocks,
    sum(tov) as turnovers,
    sum(ast) as assists
  from boxscore
  group by
    team,
    code
  order by
    team
)

select 
  mn1.*,
  lm.home as money_line,
  ssh.shot_success as h_shot_success,
  ssh.offensive_rebound as h_offensive_rebound,
  ssh.defensive_rebound as h_defensive_rebound,
  ssh.steals as h_steals,
  ssh.personal_fouls as h_personal_fouls,
  ssh.blocks as h_blocks,
  ssh.turnovers as h_turnovers,
  ssh.assists as h_assists,
  ssa.shot_success as a_shot_success,
  ssa.offensive_rebound as a_offensive_rebound,
  ssa.defensive_rebound as a_defensive_rebound,
  ssa.steals as a_steals,
  ssa.personal_fouls as a_personal_fouls,
  ssa.blocks as a_blocks,
  ssa.turnovers as a_turnovers,
  ssa.assists as a_assists
from main mn1
  inner join main mn2 on mn1.game_num = mn2.game_num + 1 and mn1.home_team = mn2.home_team
  inner join shot_success ssh on ssh.code = mn2.code and ssh.team = mn2.home_code
  inner join shot_success ssa on ssa.code = mn2.code and ssa.team = mn2.visiting_code
  inner join line_moves lm on mn1.game_date = date_url and mn1.home_team = lm.home_team and mn1.visiting_team = lm.away_team
"""

sr_book_query = """
select
  e.*,
  home.paid,
  home.ap as home_ml,
  away.ap as away_ml
from events e
  inner join sr_money_lines home on e.eid=home.eid and e.home_partid = home.partid
  inner join sr_money_lines away on e.eid=away.eid and e.away_partid = away.partid and away.paid = home.paid
where
  home.paid not in (78, 18) or away.paid not in (78, 18)
"""

def to_infinity(x):
    return np.log(x/(1-x))

def get_implied_odds(ml):
    if ml > 0:
        return 100 / (ml + 100)
    else:
        return -ml / (-ml + 100)


class DataFrameSelector(BaseEstimator, TransformerMixin):
    def __init__(self, attribute_names):
        self.attribute_names = attribute_names
    def fit(self, X, y=None):
        return self
    def transform(self, X):
        return X[self.attribute_names].values

conn = psycopg2.connect(
    host="localhost",
    database="sports",
    user="postgres",
    password=open("core/password").read()
)

cursor = conn.cursor()
cursor.execute(odds_query)
games = pd.DataFrame(cursor.fetchall())
games.columns = [i[0] for i in cursor.description]
games["money_line"] = games["money_line"].astype(float)
games["money_line_prob"] = games["money_line"].apply(get_implied_odds)
games["money_line_inf"] = games["money_line_prob"].apply(to_infinity)
games["home_wins"] = np.where(games["winner"] == games["home_code"], 1, 0)
games["odds_prediction"] = np.where(games["money_line"] < 0, 1, 0)
games["h_shot_success"] = games["h_shot_success"].astype(float).apply(to_infinity)
games["a_shot_success"] = games["a_shot_success"].astype(float).apply(to_infinity)


accuracy_score(games["home_wins"], games["odds_prediction"])

X = games
y = np.array(games["home_wins"])
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

features = ['money_line_inf', 'h_shot_success', 'h_offensive_rebound', 'h_defensive_rebound', 'h_steals', 'h_personal_fouls', 'h_blocks',
            'h_turnovers', 'h_assists', 'a_shot_success', 'a_offensive_rebound', 'a_defensive_rebound', 'a_steals',
            'a_personal_fouls', 'a_blocks', 'a_turnovers', 'a_assists']

pipeline = Pipeline([
    ('filter', DataFrameSelector(features)),
    ('scale', StandardScaler()),
    ('poly', PolynomialFeatures(degree=3)),
    ('dim_reduce', KernelPCA()),
    ('rf', RandomForestClassifier())
])

param_grid = [
    {
        'poly__degree': [1, 2, 3],
        'dim_reduce__n_components': [2, 3],
        'dim_reduce__kernel': ['rbf', 'linear', 'sigmoid', 'cosine'],
        # 'logistic__C': [1, 3, 9]
        'rf__n_estimators': [100, 200, 500],
        'rf__max_leaf_nodes': [10, 16, 32, 40]
    }
]

grid_search = GridSearchCV(pipeline, param_grid, cv=5, scoring='accuracy')
grid_search.fit(X_train, y_train)
grid_search.best_params_
grid_search.best_score_
accuracy_score(y_train, X_train["odds_prediction"])


best = grid_search.best_estimator_.fit(X_train, y_train)
predictions = best.predict(X_test)
prediction_prob = best.predict_proba(X_test)[:, 1]
odds_prob = X_test["money_line_prob"]
odds_prediction = X_test["odds_prediction"]

accuracy_score(y_test, predictions)
accuracy_score(y_test, odds_prediction)

out = pd.DataFrame({
    'code': X_test['code'],
    'y': y_test,
    'money_line': X_test['money_line'],
    'odds_pred': odds_prediction,
    'odds_prob': odds_prob,
    'model_pred': predictions,
    'model_prob': prediction_prob
})

plt.scatter(out["odds_prob"], out["model_prob"], c=y_test)


