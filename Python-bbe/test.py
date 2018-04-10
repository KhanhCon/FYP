import os
import json, requests

# print(os.system("composer validate --strict"))


def composerJson_validate(name, SHA_number):
    import urllib
    testfile = urllib.URLopener()
    file = SHA_number + "composer.json"
    testfile.retrieve('https://raw.githubusercontent.com/' + name + '/' + SHA_number + '/composer.json', file)
    import os
    code = os.system("composer validate " + file + " --strict > NUL 2>&1")
    os.remove(file)
    if code != 0:
        return False
    return True

# print os.system("composer validate composer.json ")
# print composerJson_validate("moneyphp/money", "866e0f1b7857561efe94a3320c2f6cbe8f3a2965")

# d = {"php":"1"}
# try:
#     del d['java']
# except:
#     0
# print "lol"

def downloadComposerJson(name):
    r = requests.get('https://raw.githubusercontent.com/' + name + '/master/composer.json')
    if r.status_code != 404:
        return r.json()
    else:
        return 404

with open('data.json') as data_file:
    projects = json.load(data_file)

for project in projects:
    json = downloadComposerJson(project)
    if json != 404:
        try:
            not json["name"]
        except KeyError:
            print project


