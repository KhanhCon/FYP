import heapq
from pyArango.collection import Collection, Field, Edges
from pyArango.graph import Graph, EdgeDefinition




def getTopLibraries(db, date, numberOfLibraries):
    # aql_count = "LET count = ( FOR v IN 2 INBOUND 'libraries/php' GRAPH 'github_test' COLLECT usage = v._key RETURN usage ) RETURN LENGTH(count)"

    aql_rank = "FOR library IN libraries LET count = LENGTH(( FOR v, e IN 2 INBOUND library GRAPH 'github_test' FILTER DATE_DIFF(e._to.date,"+date+", 'd', true) > 0 RETURN DISTINCT v )) SORT count DESC LIMIT "+ str(numberOfLibraries) + " RETURN{ 'count': count, 'library':library._key} "
    queryResult = db.AQLQuery(aql_rank, rawResults=True, batchSize=20)  # Batch size = top 20

    return queryResult

if __name__ == "__main__":
    from pyArango.connection import *

    conn = Connection(username="root", password="root")
    db = conn["test_fetch"]

    print(getTopLibraries(db, date = "'2013-10-01'", numberOfLibraries=10))