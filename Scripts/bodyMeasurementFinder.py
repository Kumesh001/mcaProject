import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import validators
from bs4 import BeautifulSoup
import csv
import os

csvPath='G:\MCA Project\data'
dirPath='G:/MCA Project/bodyMeasurements'

headers=[['Name','dress size','Breasts-Waist-Hips(m)','Shoe/Feet','Bra size','Cup size','Height(m)','Weight(kg)','Natural breasts or implants?','Bust Circumference(m)','Waist Circumference(m)','Hip Circumference(m)','Bust/Hip','Waist/Hip','Bust/Waist','Bust-Hip(m)','Waist-Hip(m)','Bust-Waist(m)','BMI(kg/m2)','BSI']]

def cmToM(val):
    return int(val)/100

def inchesToM(val):
    return int(val)*0.0254

def poundsToKg(val):
    return int(val)*0.453592

def calculateBMI(bodyWeight,height):
    heightSq=height*height
    bmi=bodyWeight/heightSq
    return bmi

def calculateRatio(val1,val2):
    return int(val1)/int(val2)

def calculateDifference(val1,val2):
    return val1-val2

def calculateBSI():
    print "To be done"

def init():
    filename=csvPath+'/'+'bodydata.csv'
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

            values=[]
            values.append("TempName")
            for i in list_rows[1:]:
                val=i.split(',')[0].split('[')[1].split(":")[0]
                print val
                height=0
                BWH=0
                if(val=='Height'):
                    height=i.split(',')[1].split(']')[0].split('(')[1].split(' ')[0]
                    height=cmToM(height)
                    values.append(height)
                if(val=='Weight'):
                    weight=i.split(',')[1].split(']')[0].split('(')[1].split(' ')[0]
                    weight=poundsToKg(weight)
                    values.append(weight)
                else:
                    values.append(i.split(',')[1].split(']')[0].split('(')[0])
            print values
            updateCsvFile(values)

        else:
            print "Invalid"
    except (IOError, SyntaxError) as e:
        print e


def parseFiles():
    root=dirPath
    for filename in os.listdir(dirPath):
        file_path = os.path.join(root,filename)
        if(os.path.isfile(file_path)):
            openFile=open(file_path,'r').readlines()
            for line in openFile:
                print line
                line=line.rstrip()
                getData(line)
        else:
            print "Not a file"

    # for root, directories, filenames in os.walk(dirPath):
    #     print root
    #     print directories
    #     print filename
    #     for directory in directories:
    #         directory_path = os.path.join(root, directory)
        
    #     for filename in filenames:
    #         print filename
    #         file_path = os.path.join(root,filename)
    #         if(os.path.isfile(file_path)):
    #             openFile=open(file_path,'r').readlines()
    #             for line in openFile:
    #                 line=line.rstrip()
    #                 getData(line)
    #         else:
    #             print "Not a file"



def main():
    init()
    parseFiles()

if __name__ == "__main__":
    main()



