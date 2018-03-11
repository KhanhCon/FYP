import requests
import json
import time
import os

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


def get_commits(name, page, file='composer.json'):
    payload = {'path': file, 'per_page': '100', 'page': str(page)}
    request = s.get('https://api.github.com/repos/' + name + '/commits', params=payload)
    if request.status_code == 403:  # rate limit code
        print("limit")
        reset_core = requests.get("https://api.github.com/rate_limit").json()["resources"]["core"]["reset"]
        print(reset_core - time.time())
        time.sleep(reset_core - time.time())
        history = requests.get(
            'https://api.github.com/repos/' + name + '/commits', params=payload).json()
    else:
        history = request.json()
    return history
