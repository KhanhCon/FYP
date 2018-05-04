from pyArango.connection import *
from pyArango.collection import Collection, Field, Edges
from pyArango.graph import Graph, EdgeDefinition

conn = Connection(username="root", password="root")
dbname = "TEST"

if not conn.hasDatabase(dbname):
    db = conn.createDatabase(dbname)
else:
    db = conn[dbname]

collections = [{"name": "jobs", "className": "Collection"},
               {"name": "libraries", "className": "Collection"},
               {"name": "revisions", "className": "Collection"},
               {"name": "version", "className": "Edges"},
               {"name": "uses", "className": "Edges"}, ]


for collection in collections:
    if not db.hasCollection(collection["name"]):
        db.createCollection(className=collection["className"], name=collection["name"])

db["libraries"].ensureHashIndex(fields=["github_fullname", "name"], unique=True, sparse=False)
db["version"].ensureHashIndex(fields=["_from", "_to"], unique=True, sparse=False)
db["uses"].ensureHashIndex(fields=["_from", "_to"], unique=True, sparse=False)

class libraries(Collection):
    pass
class revisions(Collection):
    pass
class uses(Edges):
    pass
class version(Edges):
    pass

class github(Graph):
    _edgeDefinitions = [
        EdgeDefinition("version", fromCollections=["libraries"],
                       toCollections=["revisions"]),
        EdgeDefinition("uses", fromCollections=["revisions"],
                       toCollections=["libraries"])
        ]
    _orphanedCollections = []



if not db.hasGraph(name="github"):
    db.createGraph("github")

for collection in collections:
    with open(collection["name"] + ".json") as f:
        data = f.read()
        url = "%s/import" % (db.URL)
        r = conn.session.post(url, params={"collection": collection["name"], "type": "auto"}, data=data)

from app.whooshIndexer.whooshIndexer import indexLibraries
indexLibraries(db, index_field="name", index_folder="index_fullname")
