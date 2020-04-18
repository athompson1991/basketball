#!/bin/sh

source venv/bin/activate

mkdir data
mkdir data/games

echo Scraping Games
scrapy crawl games
