import re
import pandas as pd
import numpy as np
from numpy import array
from numpy import argmax
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
import matplotlib.pyplot as plt
import requests
import validators
from bs4 import BeautifulSoup
import csv
import os
import sys

csvPath='D:\others\MCA\BodyMeasurementOutput'
dirPath='D:\others\MCA\Input'


# headers=[['Name','body Shape','dress size','Breasts-Waist-Hips(m)','Shoe/Feet','Bra size','Cup size','Height(m)','Weight(kg)','Natural breasts or implants?','Bust Circumference(m)','Waist Circumference(m)','Hip Circumference(m)','Bust/Hip','Waist/Hip','Bust/Waist','Bust-Hip(m)','Waist-Hip(m)','Bust-Waist(m)','BMI(kg/m2)','BSI']]
headers=[['Name','body Shape','dress size','Breasts-Waist-Hips(m)','Shoe/Feet','Bra size','Cup size','Height(m)','Weight(kg)','Natural breasts or implants?']]



def cmToM(val):
    res=float(val)/100
    g = float("{0:.3f}".format(res))
    return g

def inchesToM(val):
    res=(float(val)*2.54)/100
    g = float("{0:.3f}".format(res))
    return g
      
def poundsToKg(val):
    res=float(val)/2.2
    g = float("{0:.3f}".format(res))
    return g


def init():
    filename=csvPath+'/'+'testData.csv'
    with open(filename, 'w') as writeFile:
        writer = csv.writer(writeFile)
        lines = list(headers)
        writer.writerows(lines)
    writeFile.close()

def updateCsvFile(row):
    filename=csvPath+'/'+'testData.csv'
    try:
        with open(filename, 'a') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        csvFile.close()
    except IOError as e:
        print("I/O error({0}): {1}".format(e.errno, e.strerror))
    except: #handle other exceptions such as attribute errors
        print("Unexpected error:", sys.exc_info()[0])


def getData(url):
    try:
        res=validators.url(url)
        if res!='none':
            print("Requesting....")
            html =  r = requests.get(url)
            print("Response received")
            soup = BeautifulSoup(html.text, 'lxml')

            titles = soup.find_all('h1')
            name=titles[1].text
            # print name

            rows=soup.find_all('tr')
            list_rows = []
            values=[]
            for row in rows:
                cells = row.find_all('td')
                str_cells = str(cells)
                clean = re.compile('<.*?>')
                clean2 = (re.sub(clean, '',str_cells))
                list_rows.append(clean2)

            values.append(name)
            for i in list_rows[1:]:
                val=i.split(',')[0].split('[')[1].split(":")[0]
                if(val=='Height'):
                    try:
                        height=i.split(',')[1].split(']')[0].split('(')[1].split(' ')[0]
                        height=cmToM(height)
                        values.append(height)
                    except IndexError:
                        values.append("Null")
                        print("Out of index Error")
                elif(val=='Weight'):
                    try:
                        weight=i.split(',')[1].split(']')[0].split('(')[1].split(' ')[0]
                        # weight=poundsToKg(weight)
                        values.append(weight)
                    except IndexError:
                        values.append("Null")
                        print("Out of index Error")
                elif(val=='Breasts-Waist-Hips'):
                    try:
                        BWH=i.split(',')[1].split(']')[0].split('(')[1].split(' ')[0]
                        B=inchesToM(BWH.split('-')[0])
                        W=inchesToM(BWH.split('-')[1])
                        H=inchesToM(BWH.split('-')[2])
                        res=str(B).encode('utf-8')+'-'+str(W).encode('utf-8')+'-'+str(H).encode('utf-8')
                        values.append(res)
                    except IndexError:
                        values.append("Null")
                        print("Out of index Error")
                else:
                    try:
                      values.append(i.split(',')[1].split(']')[0].split('(')[0])
                    except IndexError:
                        values.append("Null")
                        print("Out of index Error")
            updateCsvFile(values)
        else:
            print("Invalid")
    except (IOError, SyntaxError) as e:
        print(e)


def parseFiles():
    root=dirPath
    for filename in os.listdir(dirPath):
        file_path = os.path.join(root,filename)
        if(os.path.isfile(file_path)):
            try:
                openFile=open(file_path,'r').readlines()
                for line in openFile:
                    line=line.rstrip()
                    getData(line)
            except IOError as e:
                print("I/O error({0}): {1}".format(e.errno, e.strerror))
            except: #handle other exceptions such as attribute errors
                print("Unexpected error:", sys.exc_info()[0])
        else:
            print("Not a file")

def main():
    init()
    print("Process Started")
    parseFiles()
    print("Process Ended")

if __name__ == "__main__":
    main()



