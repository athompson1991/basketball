# -*- coding: utf-8 -*-

BOT_NAME = 'basketballbot'

SPIDER_MODULES = ['core.spiders.scores_and_odds', 'core.spiders.sports_reference']
NEWSPIDER_MODULE = 'core.spiders'

ROBOTSTXT_OBEY = True
ITEM_PIPELINES = {
    # 'core.pipelines.CSVPipeline': 300,
    'core.pipelines.PostgresPipeline': 400
}

CODES_FILTER = '2019-04-01'

database_specs = {
    "host": "localhost",
    "database": "sports",
    "user": "postgres",
    "password": open("core/password").read(),
    'tables': {
        'games': {
            'code': {'dtype': 'character(12)', 'is_primary_key': True},
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
            'mp': {'dtype': ''},
            'fg': {'dtype': ''},
            'fga': {'dtype': ''},
            'fg_pct': {'dtype': ''},
            'fg3': {'dtype': ''},
            'fg3a': {'dtype': ''},
            'fg3_pct': {'dtype': ''},
            'ft': {'dtype': ''},
            'fta': {'dtype': ''},
            'ft_pct': {'dtype': ''},
            'orb': {'dtype': ''},
            'drb': {'dtype': ''},
            'trb': {'dtype': ''},
            'ast': {'dtype': ''},
            'stl': {'dtype': ''},
            'blk': {'dtype': ''},
            'tov': {'dtype': ''},
            'pf': {'dtype': ''},
            'pts': {'dtype': ''},
            'plus_minus': {'dtype': ''},
            'reason': {'dtype': ''}
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
            'play': {'dtype': 'varchar(200)'}
        }
    }
}
