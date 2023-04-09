# Wook-Scraper
A python web scrapper for work.pt that gets informations for a given book identifier

> This code might not be working because it depends on wook website structure

## How to run

- Create folders `/input`, `/output` 
- Create file `input.csv`. This file should be in the input folder and have only one column named isbn
- Create file watermark.png and save it to the utils folder if you want to have something on top of the right bottom corner that isn't just a triangle.
- Create file `proxies.txt` and populate it. This file should be in the `/utils` folder
- Create virtual environment `python -m venv venv`
- Install requirements `pip install -r requirements.txt`
- run `python main.py`


> You will have a folder named `/output` where a csv file will be created with the information about the book.

> You will have a folder named `/images` where the book images will be downloaded to.

## DISCLAIMER 
This code is harmless. 
You will be 100% responsible for the usage of the information you get.
