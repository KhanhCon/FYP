from whoosh.analysis import StemmingAnalyzer
from whoosh.fields import Schema, TEXT
from whoosh.index import create_in
from whoosh.qparser import QueryParser
import whoosh.index


if __name__ == "__main__":

    # Initialize index
    index = whoosh.index.open_dir("index_fullname")
    schema = index.schema

    qp = QueryParser("fullname", schema=schema)
    q_string = "money"
    q = qp.parse(unicode(q_string))

    with index.searcher() as searcher:

        result = searcher.search(q)
        for r in result:
            print r.fields()

        corrector = searcher.corrector("fullname")
        corrected = searcher.correct_query(q, q_string)
        if corrected.query != q:
            print("Did you mean:", corrected.string)
            print corrector.suggest(q_string, limit=5)
        # else:
        #     0
            # print corrector.suggest(q_string, limit=5)

            # for suggest in corrector.suggest(q_string, limit=5):
            #     result = searcher.search(qp.parse(unicode(suggest)))
            #     for r in result:
            #         print r.fields()