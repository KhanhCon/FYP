import heapq
from pyArango.collection import Collection, Field, Edges
from pyArango.graph import Graph, EdgeDefinition


def getTopLibraries(db, graph, collection, date, numOfLibs):
    # aql_count = "LET count = ( FOR v IN 2 INBOUND 'libraries/php' GRAPH 'github_test' COLLECT usage = v._key RETURN usage ) RETURN LENGTH(count)"

    aql_rank = "FOR library IN @@collection " \
               "LET count = LENGTH(( FOR v, e, p IN 2 INBOUND library GRAPH @graph FILTER DATE_DIFF(p.vertices[1].date, @date, 'd', true) > 0 RETURN DISTINCT v )) " \
               "SORT count " \
               "DESC LIMIT @numberOfLibraries " \
               "RETURN{ 'count': count, 'library':library.fullname} "
    bindVars = {"@collection": collection,
                "graph": graph,
                "date": date,
                "numberOfLibraries": int(numOfLibs)}
    queryResult = db.AQLQuery(aql_rank, bindVars=bindVars, rawResults=True)

    return queryResult #Need jsontify from Flask


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


if __name__ == "__main__":
    from pyArango.connection import *
    conn = Connection(username="root", password="root")
    db = conn["test_fetch"]

    for i in getDependencies(db, graph='github_test', document='libraries/laravel_laravel', date='2017-10-02'):
        print(i)
    print(getTopLibraries(db, graph='github_test', collection='libraries', date='2014-10-27', numOfLibs=10))
