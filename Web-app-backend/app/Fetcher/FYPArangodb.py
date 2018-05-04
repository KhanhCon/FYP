

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


def link_use(db, revision, libraryID):
    aql = "UPSERT { _from: @revision, _to : @libraryID} " \
          "INSERT { _from: @revision, _to : @libraryID}  " \
          "UPDATE { } IN uses  " \
          "OPTIONS { waitForSync: true }" \
          "RETURN { doc: NEW, type: OLD ? 'update' : 'insert' }"
    # aql = "INSERT { _from: @revision, _to: @libraryID, version: @version } IN uses OPTIONS { ignoreErrors: true, waitForSync: true } RETURN NEW._id"
    bindVars = {"libraryID": libraryID,
                "revision": revision}
    return db.AQLQuery(aql, bindVars=bindVars, rawResults=True, batchSize=5)[0]

def insert_lib(db, package,latest_commit=""):
    aql = "UPSERT { github_fullname: @github_fullname, name:@name} " \
          "INSERT MERGE(@package, {latest_commit:@latest_commit " \
          "}) " \
          "UPDATE MERGE(@package," \
          "{ latest_commit: OLD.latest_commit < @latest_commit ? @latest_commit: OLD.latest_commit" \
          "  }) IN libraries  " \
          "OPTIONS { waitForSync: true }" \
          "RETURN { doc: NEW, type: OLD ? 'update' : 'insert' }"
    # aql = "INSERT { _key: @library } IN libraries OPTIONS { ignoreErrors: true, waitForSync: true } RETURN NEW._id"

    bindVars = {"github_fullname": package["github_fullname"],
                "name": package["name"],
                "package":package,
                "latest_commit": latest_commit,
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

def insertJob(db, library, sha, date, status):
    aql = "UPSERT { _key: @sha} " \
          "INSERT { library: @library, _key: @sha, date:@date, status:@status  }  " \
          "UPDATE {} IN jobs  " \
          "OPTIONS { waitForSync: true }" \
          "RETURN { doc: NEW, type: OLD ? 'update' : 'insert' }"
    print(library)
    bindVars = {"library": library,
                "sha": sha,
                "date": date,
                "status": status
                }

    aql_update_lib = "LET doc = DOCUMENT(@library)" \
          "UPDATE doc WITH {latest_commit: doc.latest_commit < @date ? @date: doc.latest_commit} IN libraries"

    db.AQLQuery(aql, bindVars=bindVars, rawResults=True)
    db.AQLQuery(aql_update_lib, bindVars={"library": library["_id"], "date": date}, rawResults=True)


if __name__ == "__main__":
    from pyArango.connection import *
    conn = Connection(username="root", password="root")
    db = conn["TEST"]
    # lib = insert_lib(db,{'name': u'phpunit/phpunit', 'github_fullname': u'sebastianbergmann/phpunit22', 'description': u'wtf', 'maintainers': [{u'name': u'sebastian', u'avatar_url': u'https://www.gravatar.com/avatar/62630b9e1b8b1c4da4a4d0ab180a6642?d=identicon'}]},latest_commit='2016-03-08T21:42:29Z' )
    revision = insert_revision(db, 'superSHA', '2015-03-08T21:42:29Z')
    print(revision)
    version = link_version(db, 'libraries/16054433', revision['doc']['_id'])
    print(version)
    version = link_use(db, revision['doc']['_id'], 'libraries/16054952')

    # print link_version(db, lib["doc"]["_id"], revision["doc"]["_id"])