from bs4 import BeautifulSoup as bs
from shutil import copy
import time
import requests
import datetime
import os

ipfile = None
portfile = None
endfile = None
#Empty variables which we call later for storing dyanmic file names in

time_now  = datetime.datetime.now().strftime('%m_%d_%Y_%H_%M_%S') 
#Setting time and date for later

def proxyScrape():

    response = requests.get("https://api.proxyscrape.com?request=displayproxies&proxytype=http&timeout=7000&country=DE&anonymity=elite&ssl=no") # Calls proxyscrape API
    responseString = response.text #String copies over ^ output so we can strip the output
    printText = "\n".join([ll.rstrip() for ll in responseString.splitlines() if ll.strip()]) # Strips all garbage from output
    length = printText.count('\n') + 1 # Calculates lines in file +1 for accuracy
    file = open('PROXYSCRAPE-list-'+time_now+'.txt', "w+") #Makes file with time and date stamp in name
    file.write(printText) # Writes requests to file
    print('Total number of proxies scraped to '+'"'+file.name+'"'+' = '+str(length)) # Prints to terminal amount of proxies downloaded
    file.close() # Closes out file
    print('run proxyScrape()') # Runs when function is finished

def freeproxylistsIPS():

    r = requests.get('https://free-proxy-list.net/')
    soup = bs(r.content, 'lxml')
    ips = [item.text for item in soup.select('table[width] td:nth-of-type(1)')] # Navigates to first column, puts result as ips str

    file = open('FREEPROXYLIST-list-ips-'+time_now+'.txt', "w+")
    file.write(str(ips))
    global ipfile # Import of global var to write dynamic file name too
    ipfile = file.name # Write ipfile global var from IO

    with open(file.name, 'r') as file, open('myfile.txt', 'w+') as out:
        for line in file:
            line = line.replace("'", '\n').replace(",", '').replace("[", '').replace("]", '').rstrip()
            out.write(line)
# By default the output is to a csv format.. so this is removing the ugly syntax, formatting etc to make it understandable by the checker

    with open('myfile.txt', 'r', encoding='utf-8') as inFile,\
     open('FREEPROXYLIST-list-ips-'+time_now+'.txt', 'w+', encoding='utf-8') as outFile:
        for line in inFile:
            if line.strip():
                outFile.write(line) # More sanitization
    os.remove("myfile.txt") # Removing the temp file produced
    file.close() # Closing off file to prevent IO errors


def freeproxylistsPORTS():
#Repeat IP function, but for the ports column
    r = requests.get('https://free-proxy-list.net/')
    soup = bs(r.content, 'lxml') # Setting the type field
    ports = [item.text for item in soup.select('table[width] td:nth-of-type(2)')] # Relates to the 2nd column..

    file = open('FREEPROXYLIST-list-ports-'+time_now+'.txt', "w+")
    file.write(str(ports))
    global portfile
    portfile = file.name

    with open(file.name, 'r') as file, open('myfile2.txt', 'w+') as out:
        for line in file:
            line = line.replace("'", '\n').replace(",", '').replace("[", '').replace("]", '').rstrip()
            out.write(line)

    with open('myfile2.txt', 'r', encoding='utf-8') as inFile,\
     open('FREEPROXYLIST-list-ports-'+time_now+'.txt', 'w+', encoding='utf-8') as outFile:
        for line in inFile:
            if line.strip():
                outFile.write(line)
    os.remove("myfile2.txt")
    file.close()
    # Same process as IP..

def combineipandport():
    global portfile
    global ipfile
    global endfile

    with open(portfile) as p1: # Loads in port file from global..
        with open(ipfile) as i1: # Same for ipfile
            with open('FREEPROXYLIST-list-'+time_now+'.txt', "w+") as o1: # Dynamic file name setting
                endfile = o1.name
                plines = p1.readlines()
                ilines = i1.readlines()
                # Loads lines from both ip + port file
                for i in range(len(plines)):
                    line = ilines[i].strip() + ':' + plines[i] # : Split for readable IP:Port format
                    o1.write(line) # Interates through each entire file, combining line by line with a : divider

def cleanupdir():

    global portfile
    global ipfile
    
    os.remove(ipfile)
    time.sleep(2.4)
    os.remove(portfile)

    # Basic cleanup of junk files

def checkerSetup():
    global endfile
    print(endfile)

    folder = ('checker-files') # Setting new dir name
    name = ('proxyfile') # Name of file to go into 'checker-files'

    if os.path.isdir(folder):
        print("Exists, no need to remake")
    else:
        print("Doesn't exist, making directory..")
        os.mkdir(folder) # Checks if 'checker-files' exists, and handles accordingly

    copy(endfile, folder+'/'+name+' '+time_now+'.txt') # Places file with correct name in correct directory




freeproxylistsIPS()
freeproxylistsPORTS()
combineipandport()
cleanupdir()
time.sleep(2.4)
print('Sleeping until checkerSetup()...')
checkerSetup()

