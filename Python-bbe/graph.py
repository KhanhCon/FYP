from github import Github
import requests, json
import os, operator
from requests.auth import HTTPBasicAuth

from heapq import heappush, heappop
import heapq
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

    history = requests.get('https://api.github.com/repos/'+ name + '/commits?path='+ file + '&per_page=50').json()
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


def fetchDependencies(name, graph, SHA_number, commit_date):
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

        containDependency = contains(db["libraries"],dependency_name.replace('/','_').encode("ascii"))
        if not containDependency:
            dependency = graph.createVertex('libraries', {"_key":dependency_name.replace('/','_')})
        else:
            dependency = db["libraries"][dependency_name.replace('/','_')]
        if not containSHA or not containDependency:
            graph.link('uses', SHA, dependency, {"version": version})  #Need version

def getRepoNames():
    #For prototyping purpose
    items = requests.get(
        'https://api.github.com/search/repositories?q=language:php+stars:>500&per_page=50').json()["items"]
    for item in items:
        # names.append(item["full_name"])
        yield item["full_name"].encode('ascii')

# getDependencies('laravel/laravel', theGraph, "60de3a5670c4a3bf5fb96433828b6aadd7df0e53")
# for sha, date in getHistory('facebook/react', file='composer.json'):
#     getDependencies('facebook/react', theGraph, sha,date)



def fetchData(repoName,graph, fileName='composer.json'):
    for sha, date in getHistory(repoName, file=fileName):
        print sha
        print date
        fetchDependencies(repoName, graph, sha, date)

# getDependencies('domnikl/DesignPatternsPHP',theGraph,'620c9040a89fb2d5a58744f5c186872d9528a769','185020')

# for name in getRepoNames():
#     print(name)
#     fetchData(name, theGraph, fileName='composer.json')

# fetchData('laravel/laravel', theGraph, fileName='composer.json')

# json = downloadComposerJson('laravel/laravel')
# print(json["require"])

def getEarlierDate(date1, date2):
    if int(date1) <= int(date2):
        return date1
    else:
        return date2

def getVersion(edges, date):
    # date = edges[0]["date"]
    revision_date = 0
    sha = None
    for edge in edges:
        if int(edge["date"])<=int(date):
            if int(edge["date"]) >= int(revision_date):
                revision_date = int(edge["date"])
                sha = edge["_to"]
    return sha,revision_date

def getDependencies(document, date):
    revision, revision_date = getVersion(document.getOutEdges(db['version']), date)
    dependencies = {}
    if revision == None:
        return None
    for edge in db[revision.split('/')[0]][revision.split('/')[1]].getOutEdges(db['uses']):
        # print edge["_to"].split('/')[1]
        # print edge["version"]
        dependencies[edge["_to"].split('/')[1]] = edge["version"]
    return dependencies


def getUsage(name,date):
    sources = set()
    for edge in db['libraries'][name].getInEdges(db['uses']):
        revision = db['revisions'][edge["_from"].split('/')[1]]
        if int(revision["date"]) < int(date):
            try:
                sources.add(revision.getInEdges(db['version'])[0]['_from'])
            except IndexError:
                continue
    return len(sources)

def getTopTen(date):
    rank = []
    for library in db['libraries'].fetchAll():
        rank.append((getUsage(library._key, date), library._key.encode('ascii')))
    for l in heapq.nlargest(20, rank,key=lambda e:e[0]):
        print l

def getUsage2(name):
    aql_count = "LET count = ( FOR v, e IN 2 INBOUND 'libraries/"+name+"' GRAPH 'github_test' COLLECT usage = e._from RETURN usage ) RETURN LENGTH(count)"

    queryResult = db.AQLQuery(aql_count, rawResults=True, batchSize=100)
    return queryResult[0]

def getTop():
    rank = []
    for library in db['libraries'].fetchAll():
        rank.append((getUsage2(library._key), library._key.encode('ascii')))
    for l in heapq.nlargest(20, rank, key=lambda e: e[0]):
        print l

#fetch Data
# for name in getRepoNames():
#     print(name)
#     fetchData(name, theGraph, fileName='composer.json')

# print getDependencies(db['libraries']['laravel_laravel'],'180103') #IMPORTANT!!

# getTopTen('190201')
# print(getUsage('raven_raven','190101'))

aql = " FOR v, e IN 2 INBOUND 'libraries/php' GRAPH 'github_test' COLLECT usage = e._from RETURN usage"
aql_count = "LET count = ( FOR v, e IN 2 INBOUND 'libraries/php' GRAPH 'github_test' COLLECT usage = e._from RETURN usage ) RETURN LENGTH(count)"
aql_count = "LET count = ( FOR v IN 2 INBOUND 'libraries/php' GRAPH 'github_test' COLLECT usage = v._key RETURN usage ) RETURN LENGTH(count)"

aql_rank = "FOR library IN libraries LET count = LENGTH(( FOR v, e IN 2 INBOUND library GRAPH 'github_test' RETURN DISTINCT e._from )) SORT count DESC LIMIT 10 RETURN{ 'count': count, 'libary':library._key} "
queryResult = db.AQLQuery(aql_rank, rawResults=True, batchSize=20) #Batch size = top 20
# print(queryResult)
for key in queryResult:
    print(key)

# def foo():
#     aql_rank = "FOR library IN libraries LET count = LENGTH(( FOR v, e IN 2 INBOUND library GRAPH 'github_test' COLLECT usage = e._from SORT null RETURN usage )) SORT count  DESC LIMIT 20 RETURN{ 'count': count, 'libary':library._key} "
#     db.AQLQuery(aql_rank, rawResults=True, batchSize=20)
#
# import timeit
# t = timeit.Timer("foo()", "from graph import foo").timeit(10)
# print(t)
# print(getUsage2('php'))
# getTop()

# print getUsage('laravel_laravel','180202') #IMPORTANT!!

    # print revision_date
# for version in db['libraries']['laravel_laravel'].getOutEdges(db['version']):
#     print version["date"]
#     print version["_to"]
#
# print getVersion(db['libraries']['laravel_laravel'].getOutEdges(db['version']),'170201')

# print getEarlierDate('180103','180728')

# print getVersion(db['libraries']['laravel_laravel'].getOutEdges(db['version']))

# print getDependencies(db['libraries']['laravel_laravel'],'170804') #IMPORTANT!!


