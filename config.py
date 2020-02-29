import csv

output_directory = "/Users/alex/PycharmProjects/basketball/data"

with open(output_directory + "/games/games_2020-02-24_154443.csv", newline="") as csvfile:
    reader=csv.reader(csvfile)
    codes=[row[0] for row in reader]

codes = codes[1:]
