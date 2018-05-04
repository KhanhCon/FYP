import json
import FYPComposer, FYPArangodb

def fetchProject(db, github_fullname):
    composer = FYPComposer.downloadComposerJson(github_fullname, 'master')
    if composer == None or 'name' not in composer:
        return False
    package = FYPComposer.getPackageFromPackagist(composer['name'])
    if package == None:  # continue to next project its not a Packagist project
        return False
    # print package
    package["type"] = "project"
    FYPArangodb.insert_lib(db, package)


def fetchInitialProjects(db):
    with open('data.json') as json_data:
        names = json.load(json_data)
    try:
        with open('state.json') as json_data:
            current_index = json.load(json_data)['current_index']
        for index, github_fullname in enumerate(names[current_index:]):
            # print github_fullname
            fetchProject(db, github_fullname)
    finally:
        with open('state.json', 'w') as outfile:
            json.dump({"current_index": index+current_index}, outfile)

if __name__ == "__main__":
    try:
        from pyArango.connection import *
        conn = Connection(username="root", password="root")
        db = conn["TEST"]
        fetchInitialProjects(db)
    finally:
        print("done")
