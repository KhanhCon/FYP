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
ana = StemmingAnalyzer()
schema = Schema(fullname=TEXT(analyzer=ana, spelling=True, stored=True), id=TEXT(stored=True))

# # Create index dir if it does not exists.
# if not os.path.exists("index"):
#     os.mkdir("index")
#
# # Initialize index
# index = create_in("index", schema)

st = FileStorage("index_fullname").create()
index = st.create_index(schema)

# Initiate db connection
# connection = Connection('localhost', 27017)
# db = connection["cozy-home"]
# posts = db.posts
conn = Connection(username="root", password="root")
db = conn["New"]
aql_getLibraries = "FOR library in libraries RETURN library"

posts = db.AQLQuery(aql_getLibraries, rawResults=True, batchSize=10000)
# print(len(posts))
# Fill index with posts from DB
writer = index.writer()
for post in posts:
    writer.update_document(fullname=post["fullname"],id=post["_id"])
# writer.update_document(fullname=u"con")
writer.commit()

# Search inside index for post containing "test", then it displays
# results.
if __name__ == "__main__":
    from whoosh.qparser import QueryParser

    qp = QueryParser("fullname", schema=schema)
    q = qp.parse(u"laravel")

    with index.searcher() as searcher:
        result = searcher.search(q)
        # post = posts.find_one(ObjectId(result["laravel"]))
        for r in result:
            print(r["id"])
        corrector = searcher.corrector("fullname")
        corrected = searcher.correct_query(q, "con")
        if corrected.query != q:
            print("Did you mean:", corrected.string)

            # print post["fullname"]