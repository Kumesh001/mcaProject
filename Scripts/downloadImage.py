# Scripts to download the images from the internet
import os
import requests
import validators
import urllib2
from PIL import Image
import sys
downloadCounter=0
downloadFailCounter=0

# Set the directory where you want to save your photos
save_path='G:\MCA Project\data\ImagesCollected\Skirt'
fileNotDownloadedPath='G:/MCA Project/data/ImagesCollected/Skirt/NotDownloaded'

def checkImageValid(filename):
    try:
        img = Image.open(filename) # open the image file
        img.verify() # verify that it is, in fact an image
        print "."
    except (IOError, SyntaxError) as e:
        print ("?")
        os.remove(filename)

def getDataFromUrl(url):
    try:
        res=validators.url(url)
        if res!='none':
            filename = url.split('/')[-1]
            r = requests.get(url, allow_redirects=True)
            if r.status_code==200:
                filePath=os.path.join(save_path,filename)   
                tempFile=open(filePath, 'wb')
                tempFile.write(r.content)
                global downloadCounter
                downloadCounter+=1
                print('Download Count %d and Download Fail Count is %d' %(downloadCounter, downloadFailCounter))
            else:
                global downloadFailCounter
                downloadFailCounter+=1
                filePath=fileNotDownloadedPath+'/notDownloadedPhotoUrls.txt'
                f=open(filePath,"a")
                message=save_path.split("\'")[-1]+',Url: '+url
                f.write(message+"\n")
                print "Unable to download"
        else:
            print "Invalid"
    except (IOError, SyntaxError) as e:
        print e
   

def printFileContent():
    # Change the dir path for each folder separately
    for root, directories, filenames in os.walk('G:\MCA Project\celebrityImages\TempFolder'):
        for directory in directories:
            directory_path = os.path.join(root, directory)
        
        for filename in filenames:
            print filename
            file_path = os.path.join(root,filename)
            print file_path
            if(os.path.isfile(file_path)):
                try:
                    openFile=open(file_path,'r').readlines()
                    for line in openFile:
                        line=line.split(",")[1].split(":")
                        line=line[1]+":"+line[2]
                        print line
                        # line=line.rstrip().split('?')[0]
                        getDataFromUrl(line)
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
    # print "Deleting the Corrupt Files"
    # deleteCorruptFiles()
    # print "Deleting the Duplicate Files"
    # deleteDuplicateFiles()
    # print "Process Done"
    
if __name__=="__main__":
    main()