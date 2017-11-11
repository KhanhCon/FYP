from github import Github
import requests, json
import os

# g = Github()
# print(g.rate_limiting)
# repos = g.search_repositories('language:php',sort='stars')


##Function to download composer.json files. Using raw.githubusercontent.com
def downloadComposerJson(name):
    r = requests.get('https://raw.githubusercontent.com/' + name + '/master/composer.json')
    if r.status_code != 404:
        return r.json()
    else:
        return 404

## This funciton write all the composer.json file to a directory
def writeComposer(names,directory="composer"):
    if(not os.path.isdir(directory)):
        os.makedirs(directory)
    for name in names:
        composerFile = downloadComposerJson(name)
        if composerFile != 404:
            with open('composer/'+name.rsplit('/', 1)[-1]+".json", 'w') as outfile:
                json.dump(composerFile, outfile)
    print("Finished")


items = requests.get('https://api.github.com/search/repositories?q=language%3Aphp+sort%3Astars&per_page=100').json()["items"]
names = []
for item in items:
    names.append(item["full_name"])
writeComposer(names)


# with open('names.json') as data_file:
#     namesData = json.load(data_file)
