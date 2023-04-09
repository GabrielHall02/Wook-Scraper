import os
from datetime import datetime
import colorama
import json
from datetime import datetime
from bs4 import BeautifulSoup
import cfscrape
import pandas as pd
from watermark import *


colorama.init()

REQUESTS_MANAGER = cfscrape.CloudflareScraper()
GET = REQUESTS_MANAGER.get
POST = REQUESTS_MANAGER.post
JSON_TO_TABLE = json.loads
TABLE_TO_JSON = json.dumps
COLOR = colorama.Fore



LINKS = {"wook":"https://www.wook.pt"}

LOGGING_COLORS = {
    "INFO": COLOR.CYAN,
    "LOG": COLOR.BLUE,
    "WARNING": COLOR.YELLOW,
    "ERROR": COLOR.RED,
}

async def save_book(data):
    # Create a df in which the header = template.csv and the values will be set from content and some consts
    # Save the df to a csv file

    # Check if file output/output.csv exists
    if not os.path.isfile('output/output.csv'):
        # Create a new file
        df_header = pd.read_csv('utils/template.csv')
        df_header.to_csv('output/output.csv', index=False)

    # csv header = template.csv
    df = pd.read_csv('output/output.csv')
    # Get df size
    size = len(df.index)
    # Set the values
    df.loc[size,'Tipo'] = 'simple' 
    df.loc[size,'REF'] = data['isbn'] if 'isbn' in data.keys() else ''
    df.loc[size,'Nome'] = data['title'] if 'title' in data.keys() else ''
    df.loc[size,'Publicado'] = '1'
    df.loc[size,'Em destaque'] = '0'
    df.loc[size,'Visibilidade no catálogo'] = 'visible'
    df.loc[size,'Descrição'] = data['sinopse'] if 'sinopse' in data.keys() else ''
    df.loc[size,'Situação fiscal'] = 'taxable'
    df.loc[size,'Classe de imposto'] = 'iva-livros'
    df.loc[size,'Em stock?'] = '1'
    df.loc[size,'Comprimento (cm)'] = int(data['dimensões'].split('x')[0].strip())/10 if 'dimensões' in data.keys() else ''
    df.loc[size,'Largura (cm)'] = int(data['dimensões'].split('x')[1].strip())/10 if 'dimensões' in data.keys() else ''
    df.loc[size,'Altura (cm)'] = int(data['dimensões'].split('x')[2].strip('mm '))/10 if 'dimensões' in data.keys() else ''
    df.loc[size,'Preço normal']  = data['price'] if 'price' in data.keys() else ''
    df.loc[size,'Categorias'] = f"Livros, Livros > {data['classificação temática']}, Livros > Autor > {data['authors'][0]} > {data['authors']}, Livros > Editora > {data['editor']}" if 'classificação temática' in data.keys() and 'authors' in data.keys() and 'editor' in data.keys() else ''
    df.loc[size,'Etiquetas'] = f"{data['authors']}, {data['editor']}" if 'authors' in data.keys() and 'editor' in data.keys() else ''
    df.loc[size,'Imagens'] = f"https://www.livrariagigoeseanantes.pt/wp-content/uploads/{datetime.now().strftime('%Y')}/{datetime.now().strftime('%m')}/{data['isbn']}.jpg"
    df.loc[size,'Aumenta vendas'] = 'figabsno1,figabsno2,figabsno3'
    if 'authors' in data.keys():
        df.loc[size,'Atributo 1 nome'] = 'Autor'
        df.loc[size,'Atributo 1 valor(es)'] = data['authors']
        df.loc[size,'Atributo 1 visível'] = '1'
        df.loc[size,'Atributo 1 global'] = '1'
    if 'editor' in data.keys():
        df.loc[size,'Atributo 2 nome'] = 'Editora'
        df.loc[size,'Atributo 2 valor(es)'] = data['editor']
        df.loc[size,'Atributo 2 visível'] = '1'
        df.loc[size,'Atributo 2 global'] = '1'
    if 'encadernação' in data.keys():
        df.loc[size,'Atributo 3 nome'] = 'Encadernação'
        df.loc[size,'Atributo 3 valor(es)'] = data['encadernação']
        df.loc[size,'Atributo 3 visível'] = '1'
        df.loc[size,'Atributo 3 global'] = '1'
    if 'idioma' in data.keys():
        df.loc[size,'Atributo 4 nome'] = 'Idioma'
        df.loc[size,'Atributo 4 valor(es)'] = data['idioma']
        df.loc[size,'Atributo 4 visível'] = '1'
        df.loc[size,'Atributo 4 global'] = '1'
    if 'páginas' in data.keys():
        df.loc[size,'Atributo 5 nome'] = 'Páginas'
        df.loc[size,'Atributo 5 valor(es)'] = data['páginas']
        df.loc[size,'Atributo 5 visível'] = '1'
        df.loc[size,'Atributo 5 global'] = '1'
    if 'edição/reimpresão' in data.keys():
        df.loc[size,'Atributo 6 nome'] = 'ediçao/reimpressão'
        df.loc[size,'Atributo 6 valor(es)'] = data['edição/reimpressão']
        df.loc[size,'Atributo 6 visível'] = '1'
        df.loc[size,'Atributo 6 global'] = '1'


    df.to_csv(f"output/output.csv", index=False)




def log(logType, message, details):
    logDate = str(datetime.now())
    logFile = open('logs.log', 'a+')

    if len(details) == 0:
        logFile.write(logDate + ' [%s] ' % (logType) + message + '\n')
        print(logDate + LOGGING_COLORS[logType] + ' [%s] ' %
              (logType) + message + COLOR.RESET)
    else:
        logFile.write(logDate + ' [%s] ' % (logType) +
                      message + ' | ' + TABLE_TO_JSON(details) + '\n')
        print(logDate + LOGGING_COLORS[logType] + ' [%s] ' %
              (logType) + message + ' | ' + TABLE_TO_JSON(details) + COLOR.RESET)

    logFile.close()

    detailsString = ''

    for x in details:
        detailsString += '`%s = %s`\n' % (str(x), details[x])


async def get_book(isbn,proxies):
    #check if isbn is in db

    response = GET(LINKS["wook"]+f"/pesquisa/+{isbn}", proxies=proxies)
    if response.status_code == 200:
        log('LOG', f'Successfully retrieved search [{isbn}]', {'status_code': response.status_code})
        return response.content
    else:
        log('ERROR', 'Error while retrieving page', {'status_code': response.status_code})
        # Save isbn to txt file
        with open('output/failed.txt', 'a+') as f:
            f.write(f'{isbn}\n')
        return {'error': 'Invalid status_code', 'status_code_': response.status_code}

async def get_img(isbn, url, proxies):
     #check if direcory exists
    folder = "/Users/gabrielhall/Documents/Work/Livraria/site/BookCreator/images/"
    if not os.path.exists(folder):
        os.mkdir(f'/Users/gabrielhall/Documents/Work/Livraria/site/BookCreator/images/')
    
    #check if file exists
    if os.path.isfile(folder+str(isbn)+".jpg"):
        return
    else:
        with open(folder+str(isbn)+".jpg", "wb") as f:
            f.write(GET(url, proxies=proxies).content)
    return True

async def parse_info(isbn, content, proxies):
    if content != 400:
        data = {}
        bs = BeautifulSoup(content, 'html.parser')

        try:
            book_details = bs.find('div', {'id': 'details-toggle-collapse'})

            temp_detalis = bs.find('div', {'class': 'description-container'})
            title = temp_detalis.find('h1', {'class': 'title font-medium'})
            author_box = temp_detalis.find('h2', {'class': 'authors'})
            authors = author_box.find('a').text
            
            data['title'] = title.text.strip('\t\r\n ')
            data['authors'] = authors.strip('\t\r\n ')
            
            table = book_details.find('table')
            len_bookdata = len(table.find_all('tr'))
            
            for row in table.find_all('tr')[1:len_bookdata-1]:
                item = row.find_all('td')
                data[item[0].text.strip('\t\r\n :').lower()] = item[1].text.strip('\t\r\n ')
                if item[0].text.strip('\t\r\n :').lower() == "classificação temática":
                    classificacao = ' '.join(item[1].text.split())
                    data[item[0].text.strip('\t\r\n :').lower()] = classificacao
            
            try:
                sinopse = bs.find('div',{'id': 'synopsis-toggle-collapse'})
                data['sinopse'] = sinopse.text.strip()
            except:
                pass
            #need to check if sale price is available
            price_box = bs.find('div', {'class':'sale-container'})
            price = price_box.find('div', {'class':'wook-container'}).find_all('div')[0].find('label').text.split('i')[0].strip()
            
            img_box = bs.find('div', {'class':'image-container d-flex'})
            try:
                if img_box.find('div',{'class': 'image-not-available'}) == None:
                    raise Exception('Image available')
            except:

                urls = []
                for el in img_box.find_all('source', attrs = {'data-srcset' : True}):
                    urls.append(el['data-srcset'])
                url = urls[0].split(',')[-1].strip().split(' ')[0]
                await get_img(isbn, url, proxies)   
                await add_wm("/Users/gabrielhall/Documents/Work/Livraria/site/BookCreator/images",str(isbn)+".jpg")
                data['img'] = url


            
            #log success
            log('INFO', 'Data retreived', {'status_code': '200'})

            #save info
            await save_book(data)
            return 'success'
        except Exception as e:
            # Save isbn to txt file
            with open('output/failed.txt', 'a+') as f:
                f.write(f'{isbn}\n')

            log('ERROR', f'Error while parsing data: {e}', {'status_code': '500'})

            return 'error'


