import pandas as pd

import config

pbp_location = config.output_directory + "/pbp/pbp_2020-02-24_174249.csv"
game_location = config.output_directory + "/games/games_2020-02-24_154443.csv"

df = pd.read_csv(pbp_location)
games = pd.read_csv(game_location)
