from github import Github
import requests, json
import os, operator
from requests.auth import HTTPBasicAuth
# g = Github()
# print(g.rate_limiting)
# repos = g.search_repositories('language:php',sort='stars')
from pyArango.connection import *
conn = Connection(username="root", password="root")

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

def getDependencies(pages=5):
    names = []
    data = {}
    # requests.get('https://api.github.com/users/whatever?client_id=a4c5922e2b8eaaa27512&client_secret=899f8eda14024b57a4d101aff2a7ef61af0d9807');
    print("Gathering data")
    for period in xrange(0,1):
        for i in xrange(1,pages+1):
            items = requests.get('https://api.github.com/search/repositories?q=language%3Aphp+fork%3Afalse+stars:%3E50+created:2013-0'+str(1+period*1)+'-01..2013-0'+str(2+period*1)+'-01&per_page=100&page='+str(i)).json()["items"]
            print(i)
            for item in items:
                names.append(item["full_name"])
        for name in names:
            json = downloadComposerJson(name)
            if json != 404:
                # print(name)
                if("require-dev" in json and "require" in json):
                    # require = {**json["require"],**json["require-dev"]}
                    l1 = json["require"].keys()
                    l2 = json["require-dev"].keys()
                    require = list(set(l1 + l2))
                elif("require" in json):
                    require=json["require"]
                else:
                    require=[]
                for dependency in require:
                    data[dependency.encode("ascii")] = 1 if dependency not in data else data[dependency] + 1
    return data

#Date range 2015-01-01..2016-01-01
# 'https://api.github.com/search/repositories?q=language:php+stars:%3E50+created:2013-01-01..2013-09-20'
# fork:false
# stars:>50
#todo: sort projects by created_at date



#Get the items array from the data
# items = requests.get('https://api.github.com/search/repositories?q=language%3Aphp+sort%3Astars&per_page=100&page=15').json()["items"]
# names = []
# for item in items:
#     names.append(item["full_name"])
# print(names)
# writeComposer(names)


db = conn["github"]
db.createGraph(name='github')



# require = getDependencies(2)
# with open('dependencies.json', 'w') as outfile:
#     json.dump(require, outfile)
#
# data = json.load(open('dependencies.json'))
# top = dict(sorted(data.items(), key=operator.itemgetter(1), reverse=True)[:101])
# top.__delitem__('php')
# print(top)

# print(range(0,2))