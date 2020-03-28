# -*- coding: utf-8 -*-

BOT_NAME = 'basketballbot'

SPIDER_MODULES = ['core.spiders.scores_and_odds', 'core.spiders.sports_reference']
NEWSPIDER_MODULE = 'core.spiders'

ROBOTSTXT_OBEY = True
ITEM_PIPELINES = {
    # 'core.pipelines.CSVPipeline': 300,
    'core.pipelines.PostgresPipeline': 400
}

SEASONS = list(range(2000, 2020))
CODES_FILTER = '2010-01-01'

database_specs = {
    "host": "localhost",
    "database": "sports",
    "user": "alex",
    "password": open("core/password").read(),
    'tables': {
        'games': {
            'code': {'dtype': 'character(12)', 'is_primary_key': True},
            'season': {'dtype': 'integer'},
            'game_date': {'dtype': 'date'},
            'start_time': {'dtype': 'time'},
            'home_team': {'dtype': 'varchar(50)'},
            'home_code': {'dtype': 'varchar(10)'},
            'home_points': {'dtype': 'integer'},
            'visiting_team': {'dtype': 'varchar(50)'},
            'visiting_code': {'dtype': 'varchar(10)'},
            'visitor_points': {'dtype': 'integer'},
            'has_ot': {'dtype': 'boolean'},
            'attendance': {'dtype': 'integer'},
            'winner': {'dtype': 'varchar(10)'}
        },
        'boxscore': {
            'code': {'dtype': 'character(12)', 'is_primary_key': True},
            'team': {'dtype': 'varchar(50)'},
            'player_code': {'dtype': 'varchar(15)'},
            'player': {'dtype': 'varchar(50)'},
            'mp': {'dtype': 'varchar(6)'},
            'fg': {'dtype': 'integer'},
            'fga': {'dtype': 'integer'},
            'fg_pct': {'dtype': 'varchar(5)'},
            'fg3': {'dtype': 'integer'},
            'fg3a': {'dtype': 'integer'},
            'fg3_pct': {'dtype': 'varchar(5)'},
            'ft': {'dtype': 'integer'},
            'fta': {'dtype': 'integer'},
            'ft_pct': {'dtype': 'varchar(5)'},
            'orb': {'dtype': 'integer'},
            'drb': {'dtype': 'integer'},
            'trb': {'dtype': 'integer'},
            'ast': {'dtype': 'integer'},
            'stl': {'dtype': 'integer'},
            'blk': {'dtype': 'integer'},
            'tov': {'dtype': 'integer'},
            'pf': {'dtype': 'integer'},
            'pts': {'dtype': 'integer'},
            'plus_minus': {'dtype': 'varchar(5)'}
        },
        'pbp': {
            'code': {'dtype': 'character(12)'},
            'quarter': {'dtype': 'integer'},
            'time': {'dtype': 'time'},
            'seconds_into_game': {'dtype': 'integer'},
            'team': {'dtype': 'varchar(5)'},
            'player_1': {'dtype': 'varchar(9)'},
            'player_2': {'dtype': 'varchar(9)'},
            'player_1_name': {'dtype': 'varchar(50)'},
            'player_2_name': {'dtype': 'varchar(50)'},
            'score': {'dtype': 'varchar(20)'},
            'home_score': {'dtype': 'integer'},
            'away_score': {'dtype': 'integer'},
            'score_diff': {'dtype': 'integer'},
            'play': {'dtype': 'varchar(200)'},
            'score_change': {'dtype': 'integer'},
            'scoring_team': {'dtype': 'varchar(10)'}
        },
        'shotchart': {
            'code': {'dtype': 'character(12)'},
            'player_code': {'dtype': 'varchar(9)'},
            'team': {'dtype': 'varchar(10)'},
            'team_type': {'dtype': 'varchar(20)'},
            'shot_location': {'dtype': 'varchar(50)'},
            'x': {'dtype': 'integer'},
            'y': {'dtype': 'integer'},
            'shot_type': {'dtype': 'varchar(9)'},
            'made_shot': {'dtype': 'boolean'},
            'tip': {'dtype': 'varchar(200)'},
            'quarter': {'dtype': 'integer'},
            'time_left': {'dtype': 'time'}
        }
    }
}
