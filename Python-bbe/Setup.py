from pyArango.connection import *

import MyGithub
from MyArangodb import insertJobs, insert_lib, insert_dependency, inser_revision, link_version, link_use
from MyComposer import downloadComposerJson, composerJson_validate



def fetchJobs(database):
    conn = Connection(username="root", password="root")
    db = conn[database]
    # atexit.register(p)
    # print(time.time()-requests.get("https://api.github.com/rate_limit").json()["resources"]["core"]["reset"])
    with open('data.json') as data_file:
        github_fullnames = json.load(data_file)
    for github_fullname in github_fullnames:
        print(github_fullname)
        commits = []
        for i in range(1, 11):
            newCommits = MyGithub.get_commits(github_fullname, i)
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
            insertJobs(db, github_fullname, commit["sha"], commit['commit']['author']['date'], status="pending")

