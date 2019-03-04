import re
import csv
from datetime import datetime
import os

def get_most_recent_scrape():
    regex_pattern = '%Y-%m-%d_%H%M%S'
    regex = re.compile(r'\.csv')
    files = os.listdir("games")
    csv_files = list(filter(regex.search, files))
    dates = [datetime.strptime(f, "games_" + regex_pattern + ".csv") for f in csv_files]
    mdate = max(dates)
    not_max = list(filter(lambda x: x != mdate, dates))
    if len(not_max) > 0:
        out = "games_" + max(not_max).strftime("%Y-%m-%d_%H%M%S") + ".csv"
    else:
        out = "NA"
    return out


def get_codes():
    most_recent_scrape = get_most_recent_scrape()
    if most_recent_scrape != "NA":
        with open("./games/" + most_recent_scrape, 'r', newline='') as f:
            reader = csv.DictReader(f)
            out = [row['code'] for row in reader]
    else:
        out = ["200803010ORL"]
    return out
