from behave import given, when, then, step


def getCurrentTopLibraries(db, graph, collection, numOfLibs):
    # aql_count = "LET count = ( FOR v IN 2 INBOUND 'libraries/php' GRAPH 'github_test' COLLECT usage = v._key RETURN usage ) RETURN LENGTH(count)"

    aql_rank = "FOR library IN @@collection " \
               "LET count = LENGTH(( FOR v, e, p IN 2 INBOUND library GRAPH @graph RETURN DISTINCT v._key )) " \
               "SORT count " \
               "DESC LIMIT @numberOfLibraries " \
               "RETURN{ 'count': count, 'library':library} "
    bindVars = {"@collection": collection,
                "graph": graph,
                "numberOfLibraries": int(numOfLibs)}
    queryResult = db.AQLQuery(aql_rank, bindVars=bindVars, rawResults=True)

    return queryResult #Need jsontify from Flask
def getTopLibraries(db, graph, collection, date, numOfLibs):
    # aql_count = "LET count = ( FOR v IN 2 INBOUND 'libraries/php' GRAPH 'github_test' COLLECT usage = v._key RETURN usage ) RETURN LENGTH(count)"

    aql_rank = "FOR library IN @@collection " \
               "LET count = LENGTH(( FOR v, e, p IN 2 INBOUND library GRAPH @graph FILTER DATE_DIFF(p.vertices[1].date, @date, 'd', true) >= 0 RETURN DISTINCT v )) " \
               "SORT count " \
               "DESC LIMIT @numberOfLibraries " \
               "RETURN{ 'count': count, 'library':library} "

    bindVars = {"@collection": collection,
                "graph": graph,
                "date": date,
                "numberOfLibraries": int(numOfLibs)}
    queryResult = db.AQLQuery(aql_rank, bindVars=bindVars, rawResults=True)

    return queryResult #Need jsontify from Flask




@given('Database and graph')
def step_impl(context):
    from pyArango.connection import *
    conn = Connection(username="root", password="root")
    db = conn["CS3270_TESTING"]
    context.db = db
    context.graph = 'github'

# @when('Query the top {numberOfLibraries:d} most popular libraries currently')
# def step_impl(context, numberOfLibraries):
#     context.numberOfLibraries = numberOfLibraries
#     queryResult = getCurrentTopLibraries(context.db, graph=context.graph, collection='libraries', numOfLibs=context.numberOfLibraries)
#     context.result = queryResult
#
# @then('We get {numberOfResults:d} results')
# def step_impl(context, numberOfResults):
#     assert numberOfResults == context.numberOfLibraries
#     assert len(context.result) == numberOfResults
#
# @then('C has {usageC:d} usage, E has {usageE:d} usage, F has {usageF:d} usage currently')
# def step_impl(context, usageC, usageE, usageF):
#     for result in context.result:
#         if result['library']['_key'] == 'C':
#             assert result['count'] == usageC
#         if result['library']['_key'] == 'E':
#             assert result['count'] == usageE
#         if result['library']['_key'] == 'F':
#             assert result['count'] == usageF
#
# @when('Query the most popular libraries at 2018-01-01')
# def step_impl(context):
#     queryResult = getTopLibraries(context.db, graph=context.graph, collection='libraries', date="2018-01-01",
#                                   numOfLibs=6)
#     context.resultAt20180101 = queryResult
#
# @then('C has {usageC:d} usage, E has {usageE:d} usage, F has {usageF:d} usage at 2018-01-01')
# def step_impl(context, usageC, usageE, usageF):
#     for result in context.resultAt20180101:
#         if result['library']['_key'] == 'C':
#             assert result['count'] == usageC
#         if result['library']['_key'] == 'E':
#             assert result['count'] == usageE
#         if result['library']['_key'] == 'F':
#             assert result['count'] == usageF


@when('Query the most popular libraries at "{date}"')
def step_impl(context, date):
    queryResult = getTopLibraries(context.db, graph=context.graph, collection='libraries', date=date,
                                  numOfLibs=6)
    context.resultCE = queryResult

@then('C has {usageC:d} usage')
def step_impl(context, usageC):
    for result in context.resultCE:
        if result['library']['_key'] == u'C':
            assert result['count'] == usageC

@then('E has {usageE:d} usage')
def step_impl(context, usageE):
    for result in context.resultCE:
        if result['library']['_key'] == u'E':
            assert result['count'] == usageE
