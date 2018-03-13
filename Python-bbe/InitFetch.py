import requests
import json
import time
from pyArango.collection import Collection, Field, Edges
from pyArango.graph import Graph, EdgeDefinition
import os
import MyGithub

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

def getNamesAvatar():
    names = {}
    for i in range(1, 11):
        items = requests.get(
            'https://api.github.com/search/repositories?q=language%3Aphp+fork%3Afalse&per_page=100&page=' + str(
                i)).json()["items"]
        # names[item["full_name"]] =
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


def getCommits(name, page, file='composer.json'):
    payload = {'path': file, 'per_page': '100', 'page': str(page)}
    request = requests.get('https://api.github.com/repos/' + name + '/commits', params=payload,
                           auth=(os.getenv("ghusername"), os.getenv("ghpassword")))
    if request.status_code == 403:  # rate limit code

        reset_core = requests.get("https://api.github.com/rate_limit",
                                  auth=(os.getenv("ghusername"), os.getenv("ghpassword"))).json()["resources"]["core"][
            "reset"]
        print"limit: %s" % (reset_core - time.time())
        time.sleep(reset_core - time.time())
        history = requests.get(
            'https://api.github.com/repos/' + name + '/commits', params=payload,
            auth=(os.getenv("ghusername"), os.getenv("ghpassword"))).json()
    else:
        history = request.json()
    return history


def insertJobs(db, library, sha, date):
    aql = "INSERT { " \
          "library: @library," \
          "_key: @sha, " \
          "date : @date" \
          "} IN jobs OPTIONS { ignoreErrors: true }"
    bindVars = {"library": library,
                "sha": sha,
                "date": date
                }
    db.AQLQuery(aql, bindVars=bindVars, rawResults=True)


def insert_lib(db, library, fullname ):
    aql = "UPSERT { _key: @library} " \
          "INSERT { _key: @library, fullname: @fullname }  " \
          "UPDATE { fullname: @fullname } IN libraries  " \
          "OPTIONS { waitForSync: true }" \
          "RETURN { doc: NEW, type: OLD ? 'update' : 'insert' }"
    # aql = "INSERT { _key: @library } IN libraries OPTIONS { ignoreErrors: true, waitForSync: true } RETURN NEW._id"
    bindVars = {"library": library,
                "fullname": fullname }
    db.AQLQuery(aql, bindVars=bindVars)
    return "libraries/" + library


def inser_revision(db, sha, commitDate):
    aql = "UPSERT { _key: @key, date: @date} " \
          "INSERT { _key: @key, date: @date }  " \
          "UPDATE { } IN revisions  " \
          "OPTIONS { waitForSync: true }" \
          "RETURN { doc: NEW, type: OLD ? 'update' : 'insert' }"
    # aql = "INSERT { _key: @key, date: @date } IN revisions OPTIONS { ignoreErrors: true, waitForSync: true } RETURN NEW._id"
    bindVars = {"key": sha,
                "date": commitDate}
    db.AQLQuery(aql, bindVars=bindVars)
    return "revisions/" + sha


def link_version(db, library, revision):
    aql = "UPSERT { _from: @library, _to : @revision} " \
          "INSERT { _from: @library, _to : @revision }  " \
          "UPDATE { } IN version  " \
          "OPTIONS { waitForSync: true }" \
          "RETURN { doc: NEW, type: OLD ? 'update' : 'insert' }"
    # aql = "INSERT { _from: @library, _to: @revision } IN version OPTIONS { ignoreErrors: true, waitForSync: true } RETURN NEW._id"
    bindVars = {"library": library,
                "revision": revision}
    return db.AQLQuery(aql, bindVars=bindVars, rawResults=True, batchSize=100)[0]


def link_use(db, revision, library, version):
    aql = "UPSERT { _from: @revision, _to : @library} " \
          "INSERT { _from: @revision, _to : @library,  version: @version }  " \
          "UPDATE { } IN uses  " \
          "OPTIONS { waitForSync: true }" \
          "RETURN { doc: NEW, type: OLD ? 'update' : 'insert' }"
    # aql = "INSERT { _from: @revision, _to: @library, version: @version } IN uses OPTIONS { ignoreErrors: true, waitForSync: true } RETURN NEW._id"
    bindVars = {"library": library,
                "revision": revision,
                "version": version}
    return db.AQLQuery(aql, bindVars=bindVars, rawResults=True, batchSize=100)[0]


def main():
    conn = Connection(username="root", password="root")
    db = conn["test_fetch"]
    # atexit.register(p)


    # print(time.time()-requests.get("https://api.github.com/rate_limit").json()["resources"]["core"]["reset"])
    with open('data.json') as data_file:
        projects = json.load(data_file)
    for project in projects:
        print(project)
        for i in range(1, 11):
            commits = MyGithub.get_commits(project, i)
            if len(commits) == 0:
                break
            for commit in commits:
                # try:
                #     insertJobs(db, project, commit["sha"], commit['commit']['author']['date'])
                # except Exception:
                #     continue
                insertJobs(db, project, commit["sha"], commit['commit']['author']['date'])


def fetchDependencies(db, name, SHA_number, commit_date):
    # commit_date yy-mm-dd

    json = downloadComposerJson(name, SHA_number)
    if json != 404:
        # print(name)
        if ("require-dev" in json and "require" in json):
            l1 = json["require"]
            require = json["require-dev"]
            require.update(l1)

        elif ("require" in json):
            require = json["require"]
        else:
            print("@@")
            return None
    else:
        print("@@")
        return None

    libID = insert_lib(db, library=name.replace('/', '_'), fullname=name)
    revisionID = inser_revision(db, sha=SHA_number, commitDate=commit_date)
    link_version(db, libID, revisionID)
    for dependency_name, version in require.iteritems():
        dependencyID = insert_lib(db, dependency_name.replace('/', '_'), fullname=dependency_name)
        link_use(db, revisionID, dependencyID, version=version)


if __name__ == "__main__":
    try:
        # main()
        conn = Connection(username="root", password="root")
        db_fetch = conn["test_fetch"]
        jobs = db_fetch.AQLQuery("FOR job IN jobs_test FILTER job.status == 'pending' RETURN job", rawResults=True, batchSize=100000)
        db_example = conn["example"]
        print(len(jobs))
        for job in jobs:
            print(job)
            # db_fetch.AQLQuery("LET doc = DOCUMENT(\"" + job["_id"] + "\") UPDATE doc WITH {status: processing) } IN jobs_test")
            fetchDependencies(db_example, job["library"], job["_key"], job["date"])
            db_fetch.AQLQuery("LET doc = DOCUMENT(@job)UPDATE doc WITH {status: 'done'} IN jobs_test", bindVars={"job":job["_id"]})
    finally:
        print("done")
