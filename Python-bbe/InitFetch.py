import requests
import json
import time
from pyArango.collection import Collection, Field, Edges
from pyArango.graph import Graph, EdgeDefinition

from pyArango.connection import *


# items = requests.get(
#     'https://api.github.com/search/repositories?q=language%3Aphp+fork%3Afalse+stars:%3E50+created:2013-03-01..2013-01-01&per_page=100&page=1').json()["items"]

def getNames():
    names = []
    for i in range(1, 11):
        items = requests.get(
            'https://api.github.com/search/repositories?q=language%3Aphp+fork%3Afalse&per_page=100&page=' + str(
                i)).json()["items"]
        names += [item["full_name"] for item in items]
        print(i)
    with open('data.json', 'w') as outfile:
        json.dump(names, outfile)


def downloadComposerJson(name, SHA_number):
    r = requests.get('https://raw.githubusercontent.com/' + name + '/' + SHA_number + '/composer.json')
    if r.status_code != 404:
        try:
            return r.json()
        except ValueError:
            return 404
    else:
        return 404


def getHistory(name, page, file='composer.json'):
    request = requests.get(
        'https://api.github.com/repos/' + name + '/commits?path=' + file + '&per_page=100&page=' + str(page))

    if request.status_code == 403:  # rate limit code
        print("limit")
        reset_core = requests.get("https://api.github.com/rate_limit").json()["resources"]["core"]["reset"]
        print(reset_core - time.time())
        time.sleep(reset_core - time.time())
        history = requests.get(
            'https://api.github.com/repos/' + name + '/commits?path=' + file + '&per_page=100&page=' + str(page)).json()
    else:
        history = request.json()
    return history


def insertJobs(db, library, sha):
    aql = "INSERT { " \
          "library: @library," \
          "_key: @sha" \
          "} IN jobs"
    bindVars = {"library": library,
                "sha": sha
                }
    db.AQLQuery(aql, bindVars=bindVars, rawResults=True)


if __name__ == "__main__":
    conn = Connection(username="root", password="root")
    db = conn["test_fetch"]
    # print(time.time()-requests.get("https://api.github.com/rate_limit").json()["resources"]["core"]["reset"])
    with open('data.json') as data_file:
        projects = json.load(data_file)
    for project in projects:
        print(project)
        for i in range(1, 11):
            commits = getHistory(project, i)
            if len(commits) == 0:
                break
            for commit in commits:
                try:
                    insertJobs(db, project, commit["sha"])
                except Exception:
                    continue


                    # insertJobs(db,"li","sha")

                    # print(len(projects))
