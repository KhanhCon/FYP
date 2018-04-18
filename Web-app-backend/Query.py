import heapq
from pyArango.collection import Collection, Field, Edges
from pyArango.graph import Graph, EdgeDefinition


def getTopLibraries(db, graph, collection, date, numOfLibs):
    # aql_count = "LET count = ( FOR v IN 2 INBOUND 'libraries/php' GRAPH 'github_test' COLLECT usage = v._key RETURN usage ) RETURN LENGTH(count)"

    aql_rank = "FOR library IN @@collection " \
               "LET count = LENGTH(( FOR v, e, p IN 2 INBOUND library GRAPH @graph FILTER DATE_DIFF(p.vertices[1].date, @date, 'd', true) > 0 RETURN DISTINCT v )) " \
               "SORT count " \
               "DESC LIMIT @numberOfLibraries " \
               "RETURN{ 'count': count, 'library':library} "
    bindVars = {"@collection": collection,
                "graph": graph,
                "date": date,
                "numberOfLibraries": int(numOfLibs)}
    queryResult = db.AQLQuery(aql_rank, bindVars=bindVars, rawResults=True)

    return queryResult #Need jsontify from Flask


def getCurrentTopLibraries(db, graph, collection, numOfLibs):
    # aql_count = "LET count = ( FOR v IN 2 INBOUND 'libraries/php' GRAPH 'github_test' COLLECT usage = v._key RETURN usage ) RETURN LENGTH(count)"

    aql_rank = "FOR library IN @@collection " \
               "LET count = LENGTH(( FOR v, e, p IN 2 INBOUND library GRAPH @graph RETURN DISTINCT v )) " \
               "SORT count " \
               "DESC LIMIT @numberOfLibraries " \
               "RETURN{ 'count': count, 'library':library} "
    bindVars = {"@collection": collection,
                "graph": graph,
                "numberOfLibraries": int(numOfLibs)}
    queryResult = db.AQLQuery(aql_rank, bindVars=bindVars, rawResults=True)

    return queryResult #Need jsontify from Flask

def getCurrentTopLibrariesCache(db, graph, collection, numOfLibs):
    # aql_count = "LET count = ( FOR v IN 2 INBOUND 'libraries/php' GRAPH 'github_test' COLLECT usage = v._key RETURN usage ) RETURN LENGTH(count)"

    aql_rank = "FOR library IN @@collection " \
               "LET count = LENGTH(( FOR v, e, p IN 2 INBOUND library GRAPH @graph RETURN DISTINCT v )) " \
               "SORT count " \
               "DESC LIMIT @numberOfLibraries " \
               "RETURN{ 'count': count, 'library':library} "
    bindVars = {"@collection": collection,
                "graph": graph,
                "numberOfLibraries": int(numOfLibs)}
    # queryResult = db.AQLQuery(aql_rank, bindVars=bindVars, rawResults=True)
    queryResult = db.aql.execute(aql_rank, bindVars=bindVars, rawResults=True)
    return queryResult #Need jsontify from Flask


def getUsages(db, documents):
    aql_rank = "FOR doc IN @documents LET " \
               "library = DOCUMENT(doc.id)" \
               "LET count = LENGTH(( FOR v, e, p IN 2 INBOUND library GRAPH @graph RETURN DISTINCT v )) " \
               "SORT doc.rank " \
               "LIMIT @numberOfLibraries " \
               "RETURN{ 'count': count, 'library':library} "
    bindVars = {"documents": documents,
                "graph": "github_test",
                "numberOfLibraries":  len(documents)}
    queryResult = db.AQLQuery(aql_rank, bindVars=bindVars, rawResults=True)

    return queryResult  # Need jsontify from Flask

def getDependencies(db, graph, document, date):
    aql_dependencies = "LET revision = (FOR v IN 1 OUTBOUND @document GRAPH @graph FILTER DATE_DIFF(v.date, @date, 'd', true) > 0 SORT v.date DESC RETURN v)[0] " \
                       "FOR library, use_edge " \
                       "IN 1 OUTBOUND " \
                       "revision " \
                       "GRAPH 'github_test' " \
                       "RETURN {'library':library._id, 'version':use_edge.version}"

    bindVars = {"document": document,
                "graph": graph,
                "date": date,}

    queryResult = db.AQLQuery(aql_dependencies, bindVars=bindVars, rawResults=True)

    return queryResult  #Need jsontify from Flask

def getUsageOverTime(db, document, date='2015-01-01'):
    aql_usage = "LET startDate = @date " \
                "LET diff = DATE_DIFF(startDate, DATE_NOW(), 'm') " \
                "LET dates = (FOR i IN 1..diff return DATE_ADD(startDate, i, 'm')) " \
                "FOR date IN dates LET count = LENGTH(( FOR v, e, p IN 2 INBOUND @document GRAPH 'github_test' FILTER DATE_DIFF(p.vertices[1].date, date, 'd', true) > 0 RETURN DISTINCT v ))  " \
                "SORT date " \
                "RETURN [DATE_TIMESTAMP(date), count] "

    bindVars = {"document": document,
                "date": date, }

    queryResult = db.AQLQuery(aql_usage, bindVars=bindVars, rawResults=True)
    return queryResult

def getRelevantLibrary(db, document):
    aql_relevant = "LET users =  (FOR v, e, p IN 2 INBOUND @document GRAPH 'github_test' RETURN DISTINCT v) " \
                   "FOR user IN users " \
                   "    LET revision = (FOR v IN 1 OUTBOUND user GRAPH 'github_test' SORT v.date DESC RETURN v)[0] " \
                   "    LET docs = (FOR library IN 1 OUTBOUND revision GRAPH 'github_test' FILTER library != DOCUMENT(@document)  RETURN library) " \
                   "FOR doc IN docs " \
                   "    COLLECT libs = doc WITH COUNT INTO numUsers " \
                   "    SORT numUsers DESC " \
                   "    LIMIT 10" \
                   "    RETURN {'library':libs, 'number_of_users' : numUsers}"
    bindVars = {"document": document}

    queryResult = db.AQLQuery(aql_relevant, bindVars=bindVars, rawResults=True)
    return queryResult


if __name__ == "__main__":
    from pyArango.connection import *
    conn = Connection(username="root", password="root")
    db = conn["New"]

    # for i in getDependencies(db, graph='github_test', document='libraries/laravel_laravel', date='2017-10-02'):
    #     print(i)
    # print(getTopLibraries(db, graph='github_test', collection='libraries', date='2014-10-27', numOfLibs=10))

    print(getUsageOverTime(db,'libraries/mockery_mockery'))
