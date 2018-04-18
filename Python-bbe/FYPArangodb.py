from pyArango.connection import *

def link_version(db, libraryID, revisionID):
    aql = "UPSERT { _from: @library, _to : @revision} " \
          "INSERT { _from: @library, _to : @revision  }  " \
          "UPDATE { } IN version  " \
          "OPTIONS { waitForSync: true }" \
          "RETURN { doc: NEW, type: OLD ? 'update' : 'insert' }"
    # aql = "INSERT { _from: @library, _to: @revision } IN version OPTIONS { ignoreErrors: true, waitForSync: true } RETURN NEW._id"
    bindVars = {"library": libraryID,
                "revision": revisionID}
    return db.AQLQuery(aql, bindVars=bindVars, rawResults=True, batchSize=5)[0]


def link_use(db, revision, library, version):
    aql = "UPSERT { _from: @revision, _to : @library} " \
          "INSERT { _from: @revision, _to : @library,  version: @version}  " \
          "UPDATE { } IN uses  " \
          "OPTIONS { waitForSync: true }" \
          "RETURN { doc: NEW, type: OLD ? 'update' : 'insert' }"
    # aql = "INSERT { _from: @revision, _to: @library, version: @version } IN uses OPTIONS { ignoreErrors: true, waitForSync: true } RETURN NEW._id"
    bindVars = {"library": library,
                "revision": revision,
                "version": version}
    return db.AQLQuery(aql, bindVars=bindVars, rawResults=True, batchSize=5)[0]

def insert_lib(db,latest_commit, package):
    aql = "UPSERT { github_fullname: @github_fullname, name:@name} " \
          "INSERT { github_fullname: @github_fullname, name:@name, " \
          "description:@description , type:@type , latest_commit:@latest_commit," \
          "maintainers:@maintainers}  " \
          "UPDATE { latest_commit: OLD.latest_commit < @latest_commit ? @latest_commit: OLD.latest_commit } IN libraries  " \
          "OPTIONS { waitForSync: true }" \
          "RETURN { doc: NEW, type: OLD ? 'update' : 'insert' }"
    # aql = "INSERT { _key: @library } IN libraries OPTIONS { ignoreErrors: true, waitForSync: true } RETURN NEW._id"
    bindVars = {"github_fullname": package["github_fullname"],
                "name": package["name"],
                "type":package["type"],
                "description": package["description"],
                "maintainers": package["maintainers"],
                "latest_commit": latest_commit
                }

    return db.AQLQuery(aql, bindVars=bindVars, rawResults=True, batchSize=5)[0]

def insert_revision(db, sha, commitDate):
    aql = "UPSERT { _key: @key} " \
          "INSERT { _key: @key, date: @date }  " \
          "UPDATE { } IN revisions  " \
          "OPTIONS { waitForSync: true }" \
          "RETURN { doc: NEW, type: OLD ? 'update' : 'insert' }"
    # aql = "INSERT { _key: @key, date: @date } IN revisions OPTIONS { ignoreErrors: true, waitForSync: true } RETURN NEW._id"
    bindVars = {"key": sha,
                "date": commitDate}

    return db.AQLQuery(aql, bindVars=bindVars, rawResults=True, batchSize=5)[0]

if __name__ == "__main__":
    conn = Connection(username="root", password="root")
    db = conn["TEST"]
    lib = insert_lib(db,'2015-03-08T21:42:29Z',{'name': u'phpunit/phpunit', 'description': u'The PHP Unit Testing framework.', 'maintainers': [{u'name': u'sebastian', u'avatar_url': u'https://www.gravatar.com/avatar/62630b9e1b8b1c4da4a4d0ab180a6642?d=identicon'}], 'github_fullname': u'sebastianbergmann/phpunit', 'type': u'library'} )
    revision = insert_revision(db, 'superSHA', '2015-03-08T21:42:29Z')
    print link_version(db, lib["doc"]["_id"], revision["doc"]["_id"])