# from behave import given, when, then, step
# def getCurrentTopLibraries(db, graph, collection, numOfLibs):
#     # aql_count = "LET count = ( FOR v IN 2 INBOUND 'libraries/php' GRAPH 'github_test' COLLECT usage = v._key RETURN usage ) RETURN LENGTH(count)"
#
#     aql_rank = "FOR library IN @@collection " \
#                "LET count = LENGTH(( FOR v, e, p IN 2 INBOUND library GRAPH @graph RETURN DISTINCT v._key )) " \
#                "SORT count " \
#                "DESC LIMIT @numberOfLibraries " \
#                "RETURN{ 'count': count, 'library':library} "
#     bindVars = {"@collection": collection,
#                 "graph": graph,
#                 "numberOfLibraries": int(numOfLibs)}
#     queryResult = db.AQLQuery(aql_rank, bindVars=bindVars, rawResults=True)
#
#     return queryResult #Need jsontify from Flask
#
#
#
# @when(u'Query the most popular libraries at currently')
# def step_impl(context):
#     context.resultCE = 0
#     context.Current = getCurrentTopLibraries(context.db, graph=context.graph, collection='libraries', numOfLibs=6)
#
# @then('{library} has {usage:d} usage')
# def step_impl(context, library, usage):
#     context.resultCE = 0
#     for result in context.Current:
#         if result['library']['_key'] == library:
#             assert result['count'] == usage