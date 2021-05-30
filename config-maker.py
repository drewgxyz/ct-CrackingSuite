import json, os

fileConfigName = ''
localConfigName = ''
url = ''
loginField = ''
passwordField = ''
data = {}
data['config'] = []

def main():

    def nameDefines():
        global fileConfigName, localConfigName, url

        #Writing to global vars so that it can be dumped later to JSON
        fileConfigName = input('Enter the file output config name (NO .json END BIT NEEDED): ')
        print('Set local config file name as:', fileConfigName)
        localConfigName = input('Enter the config name to set: ')
        print('Set local configuration name as:', localConfigName)
        url = input('Enter the URL to set:')
        print('Config name set too: ', localConfigName, ', URL set as: ', url)

    def variableDefines():
        global loginField, passwordField

        #Writing to global vars so that it can be dumped later to JSON
        loginField = input('Enter the attribute name of the login box: ')
        passwordField = input('Enter the attribute name of the password box: ')
        print('Login + Password box names are:', loginField, passwordField)
    
    #Runs 2 above functions
    nameDefines()
    variableDefines()

    folder = ('configs') # Setting new dir name

    if os.path.isdir(folder): #Checks to see if config folder exists (setup for later)
        print("Exists, no need to remake")
    else:
        print("Doesn't exist, making directory..")
        os.mkdir(folder)

    data['config'].append({ #Appends to empty list, naming JSON 'config', data we produced earlier
        'Config name': localConfigName,
        'url': url,
        'Login field attribute name': loginField,
        'Password field attribute name': passwordField
    })

    with open (str(folder + '/' + fileConfigName + '.json'), 'w+') as outfile:
        json.dump(data, outfile, indent=2) #Writes to JSON with correct file path and data, with indent so it's easier for us to read
    
main()