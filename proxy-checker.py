import urllib.request , socket
from tkinter import Tk 
from tkinter.filedialog import askopenfilename
from tkinter import filedialog


socket.setdefaulttimeout(180)

checkerfolder = ".\checker-files"
Tk().withdraw() #Tkinter GUI draw function
proxyfile = str(filedialog.askopenfilename(initialdir=checkerfolder, title="Select your proxy file", #Selection of your file
        filetypes=[("Text Files", "*.txt")])) #Sorts files to show

#Empty lists to write to later
good_proxies = []
bad_proxies = []

print('With ', proxyfile, ' as the input file: ')
# read the list of proxy IPs in proxyList
with open(str(proxyfile), "r+") as file:
    proxyList = [line.strip() for line in file] #Strips line by line



def is_bad_proxy(pip):    
    try:        
        proxy_handler = urllib.request.ProxyHandler({'http': pip})        
        opener = urllib.request.build_opener(proxy_handler)
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        urllib.request.install_opener(opener)        
        sock=urllib.request.urlopen('http://www.google.com')
        #sock=urllib.urlopen(req)
    except urllib.error.HTTPError as e:        
        print('Error code: ', e.code)
        return e.code
    except Exception as detail:

        print( "ERROR:", detail)
        return 1
    return 0



for item in proxyList:
    if is_bad_proxy(item):
        print ("Bad Proxy", item)
        bad_proxies.append(item)
    else:
        print (item, "is working")
        good_proxies.append(item)

print('Finished iterating through txt file')

with open(checkerfolder+'/'+'good-proxies.txt', 'w+') as f:
    for item in good_proxies:
        f.write("%s\n" % item)
print('Finished loading into good-proxies.txt')

with open(checkerfolder+'/'+'bad-proxies.txt', 'w+') as f:
    for item in bad_proxies:
        f.write("%s\n" % item)
print('Finished loading into bad-proxies.txt')

file = open(str(proxyfile),"r+")
file.truncate(0)
file.close()

print('Emptied the proxytxt file')
