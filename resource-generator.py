import base64
import requests
import os

url = 'https://api.github.com/repos/drewgxyz/public-resources/contents/1000-most-common-passwords.txt'
resourceFolder = '.\credentials'
common_usernames = []
common_passwords = []

if os.path.isdir(resourceFolder): #Checks to see if config folder exists (setup for later)
    print('Exists, no need to remake')
else:
    print("Doesn't exist, making directory..")
    os.mkdir(resourceFolder)



req = requests.get(url)
if req.status_code == requests.codes.ok:
    req = req.json()
    content = base64.b64decode(req['content'])
    #content = content.translate({ord('\n'): None}) #Removing chars we don't want from the 1 file so it is readable

else:
    print('Content was not found.')


common_usernames.extend([
    'admin', 'andrew', 'drew', 'bob', 'adriantheloser'
])
common_passwords.extend([content])

with open(str(resourceFolder + '/usernames.txt'), 'w+') as f:
    for item in common_usernames:
        f.write('%s\n' % item)

with open(str(resourceFolder + '/passwords1.txt'), 'w+') as f:
    for item in common_passwords:
        f.write('%s' % item)

with open(str(resourceFolder + '/passwords1.txt'), 'rt') as fin:
    with open(str(resourceFolder + '/passwords.txt'), 'w+') as fout:
        for line in fin:
            fout.write(line.replace('\\n', '\n'))


        
os.remove(str(resourceFolder + '/passwords1.txt'))