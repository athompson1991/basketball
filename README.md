# Basketball Scraping Project

This is the python project that is used to scrape the data for a research project in the CFRM program. The website www.basketball-reference.com is the primary
target of this scrape. In particular, the play-by-play data is desired (i.e. [this page](https://www.basketball-reference.com/boxscores/pbp/201712020PHI.html), a random game between Detroit and Philadelphia).

## Install

Run these commands in an empty directory and it will download the codebase, install the required libraries, and _should_ download (with luck) all the data scraped so far:

```
git clone https://github.com/athompson1991/basketball.git
cd basketball
pip install -r requirements.txt
cd sports_reference
python download_script.py
```

There is a line in the script that controls just how much play-by-play data is pulled. This is important, as a full data pull can be
problematic. Also notice that the data is pushed into new directories that are created by the script. Each file has timestamp associated with
it as well, so if you run it 5 times you get 5 different files (5 times as much storage).

There is an important thing to note - the play-by-play data reads the game data to find which games to pull. How does it do this on the first run, when
a games file hasn't been downloaded yet? I default the value to a random game (200803010ORL). After the first time running the script, the script
can correctly find the file with all the game codes and will run as expected.