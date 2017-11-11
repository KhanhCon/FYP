from github import Github
import requests, json

g = Github()
print(g.rate_limiting)


def getComposerJson(name):
    r = requests.get('https://raw.githubusercontent.com/' + name + '/master/composer.json')
    if r.status_code != 404:
        return r.json()
    else:
        return 404

with open('names.json') as data_file:
    namesData = json.load(data_file)

noComposer = []
for name in namesData:
    composerFile = getComposerJson(name)
    if composerFile != 404:
        # with open('composer/'+name.rsplit('/', 1)[-1]+".json", 'w') as outfile:
        #     json.dump(composerFile, outfile)
        0
    else:
        noComposer.append(name.rsplit('/', 1)[-1])
print(noComposer)
