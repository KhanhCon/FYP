import heapq
from pyArango.collection import Collection, Field, Edges
from pyArango.graph import Graph, EdgeDefinition


def getTopLibraries(db, graph, libraries, date, numOfLibs):
    # aql_count = "LET count = ( FOR v IN 2 INBOUND 'libraries/php' GRAPH 'github_test' COLLECT usage = v._key RETURN usage ) RETURN LENGTH(count)"

    aql_rank = "FOR library IN @@libraries " \
               "LET count = LENGTH(( FOR v, e, p IN 2 INBOUND library GRAPH @graph FILTER DATE_DIFF(p[0].date, @date, 'd', true) > 0 RETURN DISTINCT v )) " \
               "SORT count " \
               "DESC LIMIT @numberOfLibraries " \
               "RETURN{ 'count': count, 'library':library._key} "
    bindVars = {"@libraries": libraries,
                "graph": graph,
                "date": date,
                "numberOfLibraries": int(numOfLibs)}
    queryResult = db.AQLQuery(aql_rank, bindVars=bindVars, rawResults=True)

    return queryResult


def getDependencies(db, date):
    aql_dependencies = "FOR library IN libraries LET count = LENGTH(( FOR v, e IN 2 INBOUND library GRAPH 'github_test' FILTER DATE_DIFF(e.date," + date + ", 'd', true) > 0 RETURN DISTINCT v )) SORT count DESC LIMIT " + numberOfLibraries + " RETURN{ 'count': count, 'library':library._key} "
    queryResult = db.AQLQuery(aql_dependencies, bindVars={"id": 123, }, rawResults=True)

    return queryResult


if __name__ == "__main__":
    from pyArango.connection import *

    conn = Connection(username="root", password="root")
    db = conn["test_fetch"]

    print(getTopLibraries(db, graph='github_test', libraries='libraries', date='2016-10-27', numOfLibs=10))
