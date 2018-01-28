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

def downloadComposerJson(name):
    r = requests.get('https://raw.githubusercontent.com/' + name + '/master/composer.json')
    if r.status_code != 404:
        return r.json()
    else:
        return 404

def getDependencies(name, graph, SHA_number):

    json = downloadComposerJson(name)
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
            print("wrong")

    if not db["libraries"][name.replace('/','_')]: #Wrong. Check if already exists
        project = graph.createVertex('libraries', {"_key": name.replace('/','_')})  #Check if the name is valid
    SHA = db["revisions"][SHA_number]
    if not SHA:
        SHA = graph.createVertex('revisions', {"_key": SHA_number}) #Replace with SHA
        graph.link('version', project, SHA, {})

    for dependency_name, version in require.iteritems():
        dependency = db["libraries"][dependency_name.replace('/', '_')]
        if not dependency:
            dependency = graph.createVertex('libraries', {"_key":dependency_name.replace('/','_')})
        graph.link('uses', SHA, dependency, {"version": version})  #Need version

getDependencies('laravel/laravel', theGraph, "master_for_now")

# json = downloadComposerJson('laravel/laravel')
# print(json["require"])

