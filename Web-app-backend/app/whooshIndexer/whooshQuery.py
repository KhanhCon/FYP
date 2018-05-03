import whoosh.index
import os
from whoosh.qparser import QueryParser,MultifieldParser, OrGroup
import app.flaskApp.arangodbQuery


dirname = os.path.dirname(os.path.abspath(__file__))

def search(qstring, index_folder = "index_fullname" ):
    index = whoosh.index.open_dir(os.path.join(dirname, index_folder))
    schema = index.schema
    qp = MultifieldParser(["fullname"], schema=schema)
    q = qp.parse(unicode(qstring))
    with index.searcher() as searcher:
        searchResult = searcher.search(q, limit=20)
        # result = {r["fullname"] for r in searchResult}
        ids = [{"rank": index_rank, "id": r["id"]} for index_rank, r in enumerate(searchResult)]
        # ids = {r for r in searchResult}
        corrector = searcher.corrector("fullname")
        suggestions = []
        if len(ids) == 0:
            suggestions = corrector.suggest(qstring, limit=6)
        # suggestionResults = {s["fullname"] for suggest in suggestions for s in searcher.search(qp.parse(unicode(suggest)), limit=5)}
        # result = result.union(suggestionResults)
        # ids_suggestion = [s["id"] for suggest in suggestions for s in searcher.search(qp.parse(unicode(suggest)), limit=5)]
        # ids_suggestion = {s for suggest in suggestions for s in searcher.search(qp.parse(unicode(suggest)), limit=5)}
        # ids = ids+ids_suggestion

    return {
            "ids": list(ids),
            "suggestions": suggestions}


if __name__ == "__main__":
    from pyArango.connection import *

    conn = Connection(username="root", password="root")
    db = conn["New"]
    # print(search("cms"))
    s = search("laravel")
    ids, searchSuggestions = s["ids"], s["suggestions"]
    # result = app.arangodbQuery.getUsages(db, ids)
    # print(result)
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
