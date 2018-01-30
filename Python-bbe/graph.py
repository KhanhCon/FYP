from github import Github
import requests, json
import os, operator
from requests.auth import HTTPBasicAuth

from pyArango.collection import Collection, Field, Edges
from pyArango.graph import Graph, EdgeDefinition

from pyArango.connection import *
conn = Connection(username="root", password="root")
db = conn["example"]

class libraries(Collection):
    _fields = {}

class revisions(Collection):
    _fields = {
        "date": Field()
    }

class uses(Edges):
    _fields = {}

class version(Edges):
    _fields = {}

class github_test(Graph) :
    _edgeDefinitions = (EdgeDefinition("version", fromCollections=["libraries"], toCollections=["revisions"]),
                        EdgeDefinition("uses", fromCollections=["revisions"], toCollections=["libraries"]))
    _orphanedCollections = []

if not db.hasGraph(name="github_test"):
    db.createGraph("github_test")
theGraph = db.graphs["github_test"]

# creating documents
# h1 = theGraph.createVertex('libraries', {"_key": "laravel_laravel"})
# h2 = theGraph.createVertex('revisions', {"_key": "f4cba4f2b254456645036139129142df274a1ec1"})
#
# theGraph.link('version', h1, h2, {})


def getHistory(name, file='composer.json'):

    history = requests.get('https://api.github.com/repos/'+ name + '/commits?path='+ file).json()
    for h in history:
        yield h['sha'], h['commit']['author']['date'].split('T')[0].replace('-','')[-6:]

def downloadComposerJson(name, SHA_number):
    r = requests.get('https://raw.githubusercontent.com/' + name + '/' + SHA_number + '/composer.json')
    if r.status_code != 404:
        try:
            return r.json()
        except ValueError:
            return 404
    else:
        return 404


def getDependencies(name, graph, SHA_number, commit_date):
    #commit_date yy-mm-dd

    def contains(collection, key):
        """if doc in collection"""
        try:
            collection.fetchDocument(key, rawResults=False)
            return True
        except KeyError as e:
            return False

    def createVertex(collection,graph, key):
        """if doc in collection"""
        try:
            return collection.fetchDocument(key, rawResults=False)
        except KeyError as e:
            return graph

    json = downloadComposerJson(name,SHA_number)
    if json != 404:
        # print(name)
        if("require-dev" in json and "require" in json):
            # require = {**json["require"],**json["require-dev"]}
            l1 = json["require"]
            require = json["require-dev"]
            # require = list(set(l1 + l2))

            require.update(l1)

        elif("require" in json):
            require=json["require"]
        else:
            print("@@")
            return None
    else:
        print("@@")
        return None

    containLibrary = contains(db["libraries"],name.replace('/','_'))
    if not containLibrary: #Wrong. Check if already exists
        project = graph.createVertex('libraries', {"_key": name.replace('/','_')})  #Check if the name is valid
    else:
        project = db["libraries"][name.replace('/','_')]
    # if not contains(db["revisions"],SHA_number):

    containSHA = contains(db["revisions"],SHA_number)
    if not containSHA: #Wrong. Check if already exists
        SHA = graph.createVertex('revisions', {"_key": SHA_number, "date": commit_date})  # Replace with SHA
    else:
        SHA = db["revisions"][SHA_number]
    # SHA = graph.createVertex('revisions', {"_key": SHA_number}) #Replace with SHA
    if not containSHA or not containLibrary:
        graph.link('version', project, SHA, {"date": commit_date})

    for dependency_name, version in require.iteritems():

        containDependency = contains(db["libraries"],dependency_name.replace('/','_'))
        if not containDependency:
            dependency = graph.createVertex('libraries', {"_key":dependency_name.replace('/','_')})
        else:
            dependency = db["libraries"][dependency_name.replace('/','_')]
        if not containSHA or not containDependency:
            graph.link('uses', SHA, dependency, {"version": version})  #Need version

def getRepoNames():
    #For prototyping purpose
    items = requests.get(
        'https://api.github.com/search/repositories?q=language:php+stars:>500&per_page=10').json()["items"]
    for item in items:
        # names.append(item["full_name"])
        yield item["full_name"].encode('ascii')

# getDependencies('laravel/laravel', theGraph, "60de3a5670c4a3bf5fb96433828b6aadd7df0e53")
# for sha, date in getHistory('facebook/react', file='composer.json'):
#     getDependencies('facebook/react', theGraph, sha,date)



def fetchData(repoName,graph, fileName='composer.json'):
    for sha, date in getHistory(repoName, file=fileName):
        print sha
        getDependencies(repoName, graph, sha, date)

getDependencies('domnikl/DesignPatternsPHP',theGraph,'620c9040a89fb2d5a58744f5c186872d9528a769','185020')

for name in getRepoNames():
    print(name)
    fetchData(name, theGraph, fileName='composer.json')



# json = downloadComposerJson('laravel/laravel')
# print(json["require"])

# for version in  db['libraries']['laravel_laravel'].getOutEdges(db['version']):
#     print version["date"]

