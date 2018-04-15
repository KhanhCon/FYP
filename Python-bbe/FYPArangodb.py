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
