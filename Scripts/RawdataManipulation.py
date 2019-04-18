import csv
import os
import sys
import math
import urllib
import pandas as pd
from numpy import array
from numpy import argmax
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import LabelBinarizer

inputFilePath='G:/MCA Project/mcaProject/data/bodydata.csv'
outputFilePath='G:/MCA Project/mcaProject/data'

#Breast type (Natural or Implant)
headers=[['Name','Height','Mass','Bust Circumference','Waist Circumference','Hip Circumference','B:W:H','B:H','W:H','B:W','B-H','W-H','B-W','BMI','BSI','Feet','AA','A','B','C','D','DD','E','DDD','F','DDDD','G','H','I','J','K','L','M','N','O','P','Q','R','FF','30A','32A','34A','36A','38A','40A','30B','32B','34B','36B','38B','40B','30C','32C','34C','36C','38C','40C','30D','32D','34D','36D','38D','40D','34DD','32AA','36DD','32DD','38DDD','40DD','34FF','36E','38E','32F','38F','30G','Naturals or Implants']]
# <   (in Inches) 
differenceBustAndBand=[1,1,	2,	3,	4,	5,	6,	7,	8,	9,	10,	11,	12,	13,	14,	15,	16,	17,	18]

# Length 19
cupSizeUS=["AA","A","B","C","D","DD","E","DDD","F","DDDD","G","H","I","J","K","L","M","N","O","P","Q","R","FF"]

# Length 20
braSizeUS=["30A","32A","34A","36A","38A","40A","30B","32B","34B","36B","38B","40B","30C","32C","34C","36C","38C","40C","30D","32D","34D","36D","38D","40D","34DD","32AA","36DD","32DD","38DDD","40DD","34FF","36E","38E","32F","38F","30G"]
# length 2
breastType=["Natural","Implants"]

cupSizeMapping={}
braSizeMapping={}
breastMapping={}

def calculateBMI(bodyWeight,height):
    height=float(height)
    mass=float(bodyWeight)
    bmi=mass/height
    return round(bmi,4)

def calculateRatio(val_1,val_2):
    ratio=float(val_1)/float(val_2)
    return round(ratio,4)

def calculateDifference(val_1,val_2):
    return round(float(val_1)-float(val_2),4)

def calculateBSI(wc,bmi,height):
    bsi=round(float(wc)/(math.pow(float(bmi),2/3)*math.pow(float(height),1/2)),4)
    return bsi

def oneHotEncoding(data):    
    label_binarizer =LabelBinarizer()
    training_mat = label_binarizer.fit_transform(data)
    i=0
    dist={}
    for item in training_mat:
        dist['\''+data[i]+'\'']=item
        i=i+1
    return dist

cupSizeMapping=oneHotEncoding(cupSizeUS)
braSizeMapping=oneHotEncoding(braSizeUS)
breastMapping=oneHotEncoding(breastType)

def init():
    filename=outputFilePath+'/'+'output.csv'
    with open(filename, 'w') as writeFile:
        writer = csv.writer(writeFile)
        lines = list(headers)
        writer.writerows(lines)
    writeFile.close()

def updateCsvFile(row):
    filename=outputFilePath+'/'+'output.csv'
    try:
        with open(filename, 'a') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        csvFile.close()
    except IOError as e:
        print("I/O error({0}): {1}".format(e.errno, e.strerror))
    except: #handle other exceptions such as attribute errors
        print("Unexpected error:", sys.exc_info()[0])

#Columns to consider
def parseRow(row):
    print("Hello")
    rawList=[]

    #Name
    name=row[0]
    rawList.append(name)
    print(rawList)
    # Height
    height=float(row[7])
    rawList.append(height)

    #Body Mass
    mass=float(row[8])
    rawList.append(mass)
    print(rawList)

    BWHRatio=row[3].split('-')
    breast=float(BWHRatio[0])
    waist=float(BWHRatio[1])
    hip=float(BWHRatio[2])
    
    #Breast
    rawList.append(breast)
    
    #Waist
    rawList.append(waist)
    
    #Hip
    rawList.append(hip)
    
    #B:W:H
    BW=calculateRatio(breast,waist)
    BWH=calculateRatio(BW,hip)
    rawList.append(BWH)
    print("BWH")
    print(rawList)

    #B:W
    BW=calculateRatio(breast,waist)
    rawList.append(BW)
   
    #W:H
    rawList.append(calculateRatio(waist,hip))

    #B:H
    rawList.append(calculateRatio(breast,hip))

    #B-W
    rawList.append(calculateDifference(breast,waist))

    #W-H
    rawList.append(calculateDifference(waist,hip))
    #B-H
    rawList.append(calculateDifference(breast,hip))

    #BMI
    bmi=calculateBMI(mass,height)
    rawList.append(bmi)

    #BSI
    bsi=calculateBSI(waist,bmi,height)
    rawList.append(bsi)

    #Feet
    print("Feet")
    rawList.append(float(row[4]))
    print(rawList)
   
    #Cup Size
    value=row[6]
    value='\''+value.strip()+'\''
    cupSize=cupSizeMapping.get(value)
    if cupSize is None:
        for k in [0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]:
            rawList.append(k)
    else:
        for i in cupSize:
            rawList.append(int(i))
    print(rawList)

    #Bra Size
    value=row[5]
    value='\''+value.strip()+'\''
    braSize=braSizeMapping.get(value)
    if braSize is None:
        for a in [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]:
            rawList.append(a)
    else:
        for j in braSize:
            rawList.append(int(j))
            
    #Breast Type
    value=row[9]
    value='\''+value.strip()+'\''
    breastType=breastMapping.get(value)
    if breastType is None:
        rawList.append(0)
    else:
        for z in breastType:
            rawList.append(int(z))
    print(rawList)
    updateCsvFile(rawList)
    

def parseInputDatafile():
    try:
        print(inputFilePath)
        with open(inputFilePath) as f:
            reader = csv.reader(f)
            # first_row = next(reader)
            for row in reader:
                print(row)
                if len(row[0])!=0:
                    parseRow(row)
    except IOError as e:
        print("I/O error({0}): {1}".format(e.errno, e.strerror))
    except: #handle other exceptions such as attribute errors
        print("Unexpected error:", sys.exc_info()[0])

init()
parseInputDatafile()
print("Done")



