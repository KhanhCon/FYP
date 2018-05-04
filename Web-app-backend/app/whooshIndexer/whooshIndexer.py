import os

from whoosh.fields import Schema, ID, KEYWORD, TEXT
from whoosh.filedb.filestore import FileStorage
from whoosh.index import create_in
from whoosh.query import Term
from whoosh.analysis import StemmingAnalyzer
from pyArango.connection import *


from bson.objectid import ObjectId

# Set index, we index title and content as texts and tags as keywords.
# We store inside index only titles and ids.


# # Create index dir if it does not exists.
# if not os.path.exists("index"):
#     os.mkdir("index")
#
# # Initialize index
# index = create_in("index", schema)
# conn = Connection(username="root", password="root")
# db = conn["TEST"]


def indexLibraries(db,index_field="name", index_folder = "index_fullname"):
    schema = Schema(fullname=TEXT(analyzer=StemmingAnalyzer(), spelling=True), id=TEXT(stored=True))
    dirname = os.path.dirname(os.path.abspath(__file__))
    st = FileStorage(os.path.join(dirname, index_folder)).create()
    index = st.create_index(schema)
    posts = db.AQLQuery("FOR library in libraries RETURN library", rawResults=True, batchSize=10000)

    writer = index.writer()
    for post in posts:
        writer.update_document(fullname=post[index_field], id=post["_id"])
    writer.commit()

# Search inside index for post containing "test", then it displays
# results.
if __name__ == "__main__":

    from pyArango.connection import *
    conn = Connection(username="root", password="root")
    db = conn["TEST"]
    indexLibraries(db, index_field="name", index_folder="index_fullname")

    # from whoosh.qparser import QueryParser
    #
    # qp = QueryParser("fullname", schema=schema)
    # q = qp.parse(u"laravel")
    #
    # with index.searcher() as searcher:
    #     result = searcher.search(q)
    #     # post = posts.find_one(ObjectId(result["laravel"]))
    #     for r in result:
    #         print(r["id"])
    #     corrector = searcher.corrector("fullname")
    #     corrected = searcher.correct_query(q, "con")
    #     if corrected.query != q:
    #         print("Did you mean:", corrected.string)

            # print post["fullname"]