#!/bin/sh

source venv/bin/activate

rm -rf data

mkdir data
mkdir data/games
mkdir data/boxscore
mkdir data/pbp
mkdir data/shotchart

scrapy crawl games -a year=2019
scrapy crawl shotchart -a code="201810180WAS"
scrapy crawl pbp -a code="201810180WAS"
scrapy crawl boxscore -a code="201810180WAS"

