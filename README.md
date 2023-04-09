# Wook-Scraper
A python web scrapper for work.pt that gets informations for a given book identifier

> This code might not be working because it depends on wook website structure

## How to run

1 - Create folders `/input`, `/output` 
2 - Create file `input.csv`. This file should be in the input folder and have only one column named isbn
3 - Create file watermark.png and save it to the utils folder if you want to have something on top of the right bottom corner that isn't just a triangle.
4 - Create file `proxies.txt` and populate it. This file should be in the `/utils` folder
5 - Create virtual environment `python -m venv venv`
6 - Install requirements `pip install -r requirements.txt`
7 - run `python main.py`


> You will have a folder named `/output` where a csv file will be created with the information about the book
> You will have a folder named `/images` where the book images will be downloaded to

## DISCLAIMER 
This code is harmless. 
You will be 100% responsible for the usage of the information you get.
