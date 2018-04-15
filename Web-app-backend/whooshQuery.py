from whoosh.analysis import StemmingAnalyzer
from whoosh.fields import Schema, TEXT
from whoosh.index import create_in
from whoosh.qparser import QueryParser
import whoosh.index
import Query

index = whoosh.index.open_dir("index_fullname")
schema = index.schema
qp = QueryParser("fullname", schema=schema)


def search(qstring):
    q = qp.parse(unicode(qstring))
    with index.searcher() as searcher:
        searchResult = searcher.search(q, limit=20)
        # result = {r["fullname"] for r in searchResult}
        ids = [r["id"] for r in searchResult]
        # ids = {r for r in searchResult}
        corrector = searcher.corrector("fullname")
        suggestions = corrector.suggest(qstring, limit=6)
        try:
            suggestions.remove(qstring)
        except ValueError:
            0
        # suggestionResults = {s["fullname"] for suggest in suggestions for s in searcher.search(qp.parse(unicode(suggest)), limit=5)}
        # result = result.union(suggestionResults)
        ids_suggestion = [s["id"] for suggest in suggestions for s in searcher.search(qp.parse(unicode(suggest)), limit=5)]
        # ids_suggestion = {s for suggest in suggestions for s in searcher.search(qp.parse(unicode(suggest)), limit=5)}
        ids = ids+ids_suggestion

    return {
            "ids": list(ids),
            "suggestions": suggestions}


if __name__ == "__main__":
    from pyArango.connection import *

    conn = Connection(username="root", password="root")
    db = conn["New"]
    # print(search("cms"))
    s = search("con")
    ids, searchSuggestions = s["ids"], s["suggestions"]
    result = Query.getUsages(db, ids)
    print result
    # Initialize index
    # index = whoosh.index.open_dir("index_fullname")
    # schema = index.schema
    #
    # qp = QueryParser("fullname", schema=schema)
    # q_string = "money"
    # q = qp.parse(unicode(q_string))
    #
    # search(q_string)

    # corrector = searcher.corrector("fullname")
    # corrected = searcher.correct_query(q, q_string)
    # if corrected.query != q:
    #     print("Did you mean:", corrected.string)
    #     print corrector.suggest(q_string, limit=5)
    # else:
    #     0
    # print corrector.suggest(q_string, limit=5)

    # for suggest in corrector.suggest(q_string, limit=5):
    #     result = searcher.search(qp.parse(unicode(suggest)))
    #     for r in result:
    #         print r.fields()
