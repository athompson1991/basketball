import scrapy

class GameItem(scrapy.Item):
    code = scrapy.Field()
    game_date = scrapy.Field()
    start_time = scrapy.Field()
    home_team = scrapy.Field()
    home_code = scrapy.Field()
    home_points = scrapy.Field()
    visiting_team = scrapy.Field()
    visiting_code = scrapy.Field()
    visitor_points = scrapy.Field()
    has_ot = scrapy.Field()
    attendance = scrapy.Field()
    winner = scrapy.Field()

class PlaybyplayItem(scrapy.Item):
    code = scrapy.Field()
    quarter = scrapy.Field()
    time = scrapy.Field()
    team = scrapy.Field()
    player_codes = scrapy.Field()
    player_names = scrapy.Field()
    score = scrapy.Field()
    play = scrapy.Field()

class BoxscoreItem(scrapy.Item):
    code = scrapy.Field(default="NA")
    team = scrapy.Field(default="NA")
    player = scrapy.Field(default="NA")
    mp = scrapy.Field(default="NA")
    fg = scrapy.Field(default="NA")
    fga = scrapy.Field(default="NA")
    fg_pct = scrapy.Field(default="NA")
    fg3 = scrapy.Field(default="NA")
    fg3a = scrapy.Field(default="NA")
    fg3_pct = scrapy.Field(default="NA")
    ft = scrapy.Field(default="NA")
    fta = scrapy.Field(default="NA")
    ft_pct = scrapy.Field(default="NA")
    orb = scrapy.Field(default="NA")
    drb = scrapy.Field(default="NA")
    trb = scrapy.Field(default="NA")
    ast = scrapy.Field(default="NA")
    stl = scrapy.Field(default="NA")
    blk = scrapy.Field(default="NA")
    tov = scrapy.Field(default="NA")
    pf = scrapy.Field(default="NA")
    pts = scrapy.Field(default="NA")
    plus_minus = scrapy.Field(default="NA")
    reason = scrapy.Field(default="NA")

class ShotChartItem(scrapy.Item):
    code = scrapy.Field(default="NA")
    team = scrapy.Field(default="NA")
    team_type = scrapy.Field(default="NA")
    shot_location = scrapy.Field(default="NA")
    x = scrapy.Field(default="NA")
    y = scrapy.Field(default="NA")
    made_shot = scrapy.Field(default="NA")
    tip = scrapy.Field(default="NA")
    player_code = scrapy.Field(default="NA")
    quarter = scrapy.Field(default="NA")
    time_left = scrapy.Field(default="NA")

