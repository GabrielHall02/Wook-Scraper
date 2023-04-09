from scrapper import *
import pandas as pd
import asyncio
import time

DF = pd.read_csv('input/isbn.csv')

def get_proxies():
    proxies = {}
    with open('utils/proxies.txt', 'r') as f:
        for line in f:
            key = line.split(':')[0]
            value = line.split(':')[1]+':'+line.split(':')[2]
            proxies[key] = value
    return proxies

async def main():
    start = time.time()
    for index, row in DF.iterrows():
        await parse_info(row['isbn'], await get_book(row['isbn'], get_proxies()),get_proxies())
    end = time.time()
    print(f'Total time: {end-start}')

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())