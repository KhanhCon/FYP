def insertJobs(db, library, sha, date, status):
    aql = "INSERT { " \
          "library: @library," \
          "_key: @sha, " \
          "date : @date, " \
          "status: @status" \
          "} IN jobs OPTIONS { ignoreErrors: true }"
    bindVars = {"library": library,
                "sha": sha,
                "date": date,
                "status": status
                }
    db.AQLQuery(aql, bindVars=bindVars, rawResults=True)


def insert_lib(db, library, fullname, updatedDate, language ):
    aql = "UPSERT { _key: @library} " \
          "INSERT { _key: @library, fullname: @fullname, updated_date:@updated_date, language:@language }  " \
          "UPDATE { updated_date:@updated_date } IN libraries  " \
          "OPTIONS { waitForSync: true }" \
          "RETURN { doc: NEW, type: OLD ? 'update' : 'insert' }"
    # aql = "INSERT { _key: @library } IN libraries OPTIONS { ignoreErrors: true, waitForSync: true } RETURN NEW._id"
    bindVars = {"library": library,
                "fullname": fullname,
                "updated_date":updatedDate,
                "language": language}
    db.AQLQuery(aql, bindVars=bindVars)
    return "libraries/" + library


def insert_dependency(db, library, fullname, language ):
    aql = "UPSERT { _key: @library} " \
          "INSERT { _key: @library, fullname: @fullname, updated_date:'', language:@language}  " \
          "UPDATE {} IN libraries  " \
          "OPTIONS { waitForSync: true }" \
          "RETURN { doc: NEW, type: OLD ? 'update' : 'insert' }"
    # aql = "INSERT { _key: @library } IN libraries OPTIONS { ignoreErrors: true, waitForSync: true } RETURN NEW._id"
    bindVars = {"library": library,
                "fullname": fullname,
                "language":language}
    db.AQLQuery(aql, bindVars=bindVars)
    return "libraries/" + library


def inser_revision(db, sha, commitDate):
    aql = "UPSERT { _key: @key} " \
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
    aql = "UPSERT { _key: @key} " \
          "INSERT { _from: @library, _to : @revision, _key: @key  }  " \
          "UPDATE { } IN version  " \
          "OPTIONS { waitForSync: true }" \
          "RETURN { doc: NEW, type: OLD ? 'update' : 'insert' }"
    # aql = "INSERT { _from: @library, _to: @revision } IN version OPTIONS { ignoreErrors: true, waitForSync: true } RETURN NEW._id"
    bindVars = {"library": library,
                "revision": revision,
                "key":revision.split('/')[1]}
    return db.AQLQuery(aql, bindVars=bindVars, rawResults=True, batchSize=100)[0]


def link_use(db, revision, library, version):
    aql = "UPSERT { _key:@key} " \
          "INSERT { _from: @revision, _to : @library,  version: @version, _key:@key }  " \
          "UPDATE { } IN uses  " \
          "OPTIONS { waitForSync: true }" \
          "RETURN { doc: NEW, type: OLD ? 'update' : 'insert' }"
    # aql = "INSERT { _from: @revision, _to: @library, version: @version } IN uses OPTIONS { ignoreErrors: true, waitForSync: true } RETURN NEW._id"
    bindVars = {"library": library,
                "revision": revision,
                "version": version,
                "key": revision.split('/')[1]+library.split('/')[1]}
    return db.AQLQuery(aql, bindVars=bindVars, rawResults=True, batchSize=100)[0]