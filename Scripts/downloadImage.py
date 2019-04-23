# Scripts to download the images from the internet
import os
import requests
import validators
import urllib2
import urllib
from PIL import Image
import sys
downloadCounter=0
downloadFailCounter=0

# Set the directory where you want to save your photos
save_path='D:/others/MCA/Top'
fileName="Brie_Larson"
walkDir='D:/others/MCA/TopToDownloads'
fileNotDownloadedPath='D:/others/MCA/Pants/Gwen Stefani/Images/NotDownloaded'

def checkImageValid(filename):
    try:
        img = Image.open(filename) # open the image file
        img.verify() # verify that it is, in fact an image
        print "."
    except (IOError, SyntaxError) as e:
        print ("?")
        os.remove(filename)

def getDataFromUrl(url,foldername):
    try:
        res=validators.url(url)
        if res!='none':
            filename = url.split('/')[-1]
            global downloadCounter
            downloadCounter+=1
            try:
                filePath=os.path.join(save_path+'/'+foldername,str(foldername)+"_"+str(downloadCounter)+".jpg") 
                urllib.urlretrieve(url, filePath)
                print("Image Saved")
            except Exception as e:
                print e
        else:
            print "Invalid"
    except (IOError, SyntaxError) as e:
        print e
   

def printFileContent():
    # Change the dir path for each folder separately
    for root, directories, filenames in os.walk(walkDir):
        for directory in directories:
            directory_path = os.path.join(root, directory)
        
        for filename in filenames:
            currentDir=os.getcwd()
            file_path = os.path.join(root,filename)
            if(os.path.isfile(file_path)):
                try:
                    dirname=file_path.split('/')[-1].split('\\')[1]
                    openFile=open(file_path,'r').readlines()
                    if os.path.exists(save_path):
                        os.mkdir(save_path+'/'+dirname)
                        print("Created Folder")
                    else:
                        print("Failed creating Folder")
                    # print dirname
                    for line in openFile:
                        getDataFromUrl(line,dirname)
                except IOError as e:
                    print "I/O error({0}): {1}".format(e.errno, e.strerror)
            else:
                print "Not a file"


def findDup(parentFolder):
    # Dups in format {hash:[names]}
    dups = {}
    for dirName, subdirs, fileList in os.walk(parentFolder):
        print('Scanning %s...' % dirName)
        for filename in fileList:
            # Get the path to the file
            path = os.path.join(dirName, filename)
            # Calculate hash
            file_hash = hashfile(path)
            # Add or append the file path
            if file_hash in dups:
                dups[file_hash].append(path)
            else:
                dups[file_hash] = [path]
    return dups

def hashfile(path, blocksize = 65536):
    afile = open(path, 'rb')
    hasher = hashlib.md5()
    buf = afile.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(blocksize)
    afile.close()
    return hasher.hexdigest()


def deleteCorruptFiles():
    path=os.listdir(save_path)
    for file in path:
        checkImageValid(save_path+'/'+file)

def deleteDuplicateFiles():
    duplicates=findDup(save_path)
    if len(duplicates)>0:
        for item in duplicates:
            os.remove(item)  

def main():
    printFileContent()
    print "Download Completed"
    print "Deleting the Corrupt Files"
    deleteCorruptFiles()
    print "Deleting the Duplicate Files"
    deleteDuplicateFiles()
    print "Process Done"
    
if __name__=="__main__":
    main()