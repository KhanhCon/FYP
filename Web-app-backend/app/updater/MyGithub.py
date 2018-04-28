import requests
import json
import time
import os
import ast
# import config
import datetime

s = requests.Session()
s.auth = (os.getenv("ghusername"), os.getenv("ghpassword"))


def get_composerjson(name, SHA_number):
    r = requests.get('https://raw.githubusercontent.com/' + name + '/' + SHA_number + '/composer.json')
    if r.status_code != 404:
        try:
            return r.json()
        except ValueError:
            return 404
    else:
        return 404


# def get_commits(name, page, file='composer.json', since='2012-03-06T22:42:09Z'):
#     payload = {'path': file, 'per_page': '100', 'page': str(page), 'since':since}
#     request = s.get('https://api.github.com/repos/' + name + '/commits', params=payload)
#     if request.status_code == 404:
#         return []
#     if request.status_code == 403:  # rate limit code
#         print("limit")
#         reset_core = requests.get("https://api.github.com/rate_limit").json()["resources"]["core"]["reset"]
#         print(reset_core - time.time())
#         time.sleep(reset_core - time.time())
#         history = requests.get(
#             'https://api.github.com/repos/' + name + '/commits', params=payload).json()
#     elif request.status_code == 200:
#         history = request.json()
#     else:
#         return []
#     return history

def get_commit_at_page(name, page, file='composer.json', since="2012-03-06T22:42:09Z"):
    if since == "":
        since = '2012-03-06T22:42:09Z'

    payload = {'path': file, 'per_page': '100', 'page': str(page), 'since':since}
    request = s.get('https://api.github.com/repos/' + name + '/commits', params=payload)
    if request.status_code == 404:
        return []
    if request.status_code == 403:  # rate limit code
        print("limit")
        reset_core = requests.get("https://api.github.com/rate_limit").json()["resources"]["core"]["reset"]
        print(reset_core - time.time())
        time.sleep(reset_core - time.time())
        history = requests.get(
            'https://api.github.com/repos/' + name + '/commits', params=payload).json()
    elif request.status_code == 200:
        history = request.json()
    else:
        return []
    return history

def get_commits(name, file='composer.json', since='2012-03-06T22:42:09Z'):
    commits = []
    for page in range(1, 11):
        newCommits = get_commit_at_page(name,file=file, page=page, since=since)
        if len(newCommits) == 0:
            break
        commits = commits + newCommits
    if len(commits) == 0:
        return []
    commits.sort(key=lambda commit: commit['commit']['author']['date'])
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
    return validCommits

def continous_integration_status(name, SHA_number):
    request = s.get('https://api.github.com/repos/' + name + '/statuses/' + SHA_number)
    if request.status_code == 403:  # rate limit code
        print("limit")
        reset_core = requests.get("https://api.github.com/rate_limit").json()["resources"]["core"]["reset"]
        print(reset_core - time.time())
        time.sleep(reset_core - time.time())
        statuses = requests.get(
            'https://api.github.com/repos/' + name + '/statuses/' + SHA_number).json()
    else:
        statuses = request.json()

    if len(statuses)==0:
        return "none"
    else:
        for status in statuses:
            if status["state"] == "error" or status["state"] == "failure":
                return "fail"
    return "success"

if __name__ == "__main__":
    commits = []
    for i in range(1, 11):
        newCommits = get_commits("moneyphp/money", i)
        if len(newCommits) == 0:
            break
        commits = commits + newCommits
    commits.sort(key=lambda commit: commit['commit']['author']['date'])
    from datetime import datetime
    for commit in commits:
        print commit['commit']['author']['date']
    validCommits = []
    for index in range(1, len(commits)):
        date_format = "%Y-%m-%dT%H:%M:%SZ"
        a = datetime.strptime(commits[index-1]['commit']['author']['date'], date_format)
        b = datetime.strptime(commits[index]['commit']['author']['date'], date_format)
        delta = b - a
        if delta.days > 0:
            validCommits.append(commits[index-1])
    validCommits.append(commits[-1])
    print("_______")
    for i in validCommits:
        print i['commit']['author']['date']
