import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import validators
from bs4 import BeautifulSoup
import csv

csvPath='G:\MCA Project\data'

headers=[['Name','dress size','Breasts-Waist-Hips','Shoe/Feet','Bra size','Cup size','Height','Weight','Natural breasts or implants?']]

def init():
    filename=csvPath+'/'+'bodydata.csv'
    print filename
    with open(filename, 'w') as writeFile:
        writer = csv.writer(writeFile)
        lines = list(headers)
        writer.writerows(lines)
    writeFile.close()

def updateCsvFile(row):
    filename=csvPath+'/'+'bodydata.csv'
    with open(filename, 'a') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerow(row)
    csvFile.close()


def getData(url):
    try:
        res=validators.url(url)
        if res!='none':
            html =  r = requests.get(url)
            soup = BeautifulSoup(html.text, 'lxml')

            rows=soup.find_all('tr')
            list_rows = []
            for row in rows:
                cells = row.find_all('td')
                str_cells = str(cells)
                clean = re.compile('<.*?>')
                clean2 = (re.sub(clean, '',str_cells))
                list_rows.append(clean2)

            final=[]
            values=[]

            for i in list_rows[1:]:
                values.append(i.split(',')[1].split(']')[0])
            
            final.append(values)
            updateCsvFile(final)
        else:
            print "Invalid"
    except (IOError, SyntaxError) as e:
        print e


def parseFiles():
    for root, directories, filenames in os.walk('G:\MCA Project\celebrityImages\Dress'):
        for directory in directories:
            directory_path = os.path.join(root, directory)
        
        for filename in filenames:
            file_path = os.path.join(root,filename)
            if(os.path.isfile(file_path)):
                openFile=open(file_path,'r').readlines()
                for line in openFile:
                    line=line.rstrip()
                    getData(line)
            else:
                print "Not a file"



def main():
    init()
    parseFiles()

if __name__ == "__main__":
    main()



