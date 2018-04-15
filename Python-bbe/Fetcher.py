import os
import time

from pyArango.connection import *

import MyGithub
# items = requests.get(
#     'https://api.github.com/search/repositories?q=language%3Aphp+fork%3Afalse+stars:%3E50+created:2013-03-01..2013-01-01&per_page=100&page=1').json()["items"]
from MyArangodb import insertJobs, insert_lib, insert_dependency, inser_revision, link_version, link_use
from MyComposer import downloadComposerJson, composerJson_validate
import os
import time

from pyArango.connection import *

import MyGithub
# items = requests.get(
#'https://api.github.com/search/repositories?q=language%3Aphp+fork%3Afalse+stars:%3E50+created:2013-03-01..2013-01-01&per_page=100&page=1').json()["items"]
from MyArangodb import insertJobs, insert_lib, insert_dependency, inser_revision, link_version, link_use
from MyComposer import downloadComposerJson, composerJson_validate


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


def fetchJobs(database):
    conn = Connection(username="root", password="root")
    db = conn[database]
    # atexit.register(p)
    # print(time.time()-requests.get("https://api.github.com/rate_limit").json()["resources"]["core"]["reset"])
    with open('data.json') as data_file:
        projects = json.load(data_file)
    for project in projects:
        print(project)
        commits = []
        for i in range(1, 11):
            newCommits = MyGithub.get_commits(project, i)
            if len(newCommits) == 0:
                break
            commits = commits + newCommits
        if len(commits)==0:
            continue
        #Remove commits on the same day. Take the last one
        commits.sort(key=lambda commit:commit['commit']['author']['date'])
        from datetime import datetime
        validCommits = []
        for index in range(1, len(commits)):
            date_format = "%Y-%m-%dT%H:%M:%SZ"
            a = datetime.strptime(commits[index - 1]['commit']['author']['date'], date_format)
            b = datetime.strptime(commits[index]['commit']['author']['date'], date_format)
            delta = b - a
            if delta.days > 0:
                validCommits.append(commits[index - 1])
        validCommits.append(commits[-1])

        for commit in validCommits:
            insertJobs(db, project, commit["sha"], commit['commit']['author']['date'], status="pending")


def fetchDependencies(databaseName, name, SHA_number, commit_date, language):
    conn = Connection(username="root", password="root")
    db = conn[databaseName]
    # commit_date yy-mm-dd
    print(name)
    status = MyGithub.continous_integration_status(name=name, SHA_number=SHA_number)
    if status == "fail":
        print("continous integration fail")
        return None
    elif status == "none":
        if composerJson_validate(name, SHA_number) == False:
            print("invalid composerJson")
            return None

    json = downloadComposerJson(name, SHA_number)
    # print json
    if json != 404 and json != None:
        # print(name)
        if ("require-dev" in json and "require" in json):
            l1 = json["require"]
            require = json["require-dev"]
            require.update(l1)

        elif ("require" in json):
            require = json["require"]
        elif ("require-dev" in json):
            require = json["require-dev"]
        else:
            print("@@")
            return None
    else:
        print("@@")
        return None

    libID = insert_lib(db, library=name.replace('/', '_'), fullname=name, updatedDate = commit_date, language=language)
    revisionID = inser_revision(db, sha=SHA_number, commitDate=commit_date)
    link_version(db, libID, revisionID)
    try:
        del require["php"]
    except KeyError:
        print("no php in require")
    for dependency_name, version in require.iteritems():
        # print dependency_name
        dependencyID = insert_dependency(db, dependency_name.replace('/', '_'), fullname=dependency_name, language=language)
        link_use(db, revisionID, dependencyID, version=version)
    print("Fetched " + name)

def fetchProjects(databaseName, jobs_collection):
    conn = Connection(username="root", password="root")
    db_fetch = conn[databaseName]
    jobs = db_fetch.AQLQuery("FOR job IN @@collection FILTER job.status == 'pending' SORT job.library, job.date RETURN job", bindVars={"@collection": jobs_collection}, rawResults=True,
                             batchSize=100000)
    print(len(jobs))
    for job in jobs:
        # print("library date", (job["library"], job["date"]))
        fetchDependencies(databaseName, job["library"], job["_key"], job["date"], job["language"])
        db_fetch.AQLQuery("LET doc = DOCUMENT(@job)UPDATE doc WITH {status: 'done'} IN @@collection",
                          bindVars={"job": job["_id"],
                          "@collection":jobs_collection})

if __name__ == "__main__":
    try:
        # fetchJobs("New")
        fetchProjects("New","jobs")
        # main()
        # conn = Connection(username="root", password="root")
        # db_fetch = conn["test_fetch"]
        # jobs = db_fetch.AQLQuery("FOR job IN jobs_test FILTER job.status == 'pending' RETURN job", rawResults=True, batchSize=100000)
        # db_example = conn["example"]
        # print(len(jobs))
        # for job in jobs:
        #     # print job
        #     # db_fetch.AQLQuery("LET doc = DOCUMENT(\"" + job["_id"] + "\") UPDATE doc WITH {status: processing) } IN jobs_test")
        #     fetchDependencies("example", job["library"], job["_key"], job["date"])
        #     db_fetch.AQLQuery("LET doc = DOCUMENT(@job)UPDATE doc WITH {status: 'done'} IN jobs_test", bindVars={"job":job["_id"]})
    finally:
        print("done")
