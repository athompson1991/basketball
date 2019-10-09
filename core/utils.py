import re
import csv
from datetime import datetime
import os

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
