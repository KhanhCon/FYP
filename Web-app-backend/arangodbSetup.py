from pyArango.connection import *
from config import *

from pyArango.collection import Collection, Field, Edges
from pyArango.graph import Graph, EdgeDefinition

conn = Connection(username=ARANGODB_CONNECTION_CONFIG['username'], password=ARANGODB_CONNECTION_CONFIG['password'])
try:
    db = conn.createDatabase(name=ARANGODB_DATABASE['dbname'])
except CreationError:
    db = conn[ARANGODB_DATABASE['dbname']]

# db.createCollection(name=ARANGODB_DATABASE['document_libraries'], className='Collection', waitForSync=True)
# db.createCollection(name=ARANGODB_DATABASE['document_revisions'], className='Collection', waitForSync=True)
# db.createCollection(name=ARANGODB_DATABASE['edge_version'], className='Edges', waitForSync=True)
# db.createCollection(name=ARANGODB_DATABASE['edge_use'], className='Edges', waitForSync=True)


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
        EdgeDefinition(ARANGODB_DATABASE['edge_version'], fromCollections=[ARANGODB_DATABASE['document_libraries']],
                       toCollections=[ARANGODB_DATABASE['document_revisions']]),
        EdgeDefinition(ARANGODB_DATABASE['edge_use'], fromCollections=[ARANGODB_DATABASE['document_revisions']],
                       toCollections=[ARANGODB_DATABASE['document_libraries']])
        ]
    _orphanedCollections = []

db[ARANGODB_DATABASE['edge_version']].ensureHashIndex(["_from", "_to"], unique=True, sparse=False)
db[ARANGODB_DATABASE['edge_use']].ensureHashIndex(["_from", "_to"], unique=True, sparse=False)
db[ARANGODB_DATABASE['document_libraries']].ensureHashIndex(["github_fullname", "name"], unique=True, sparse=False)

if not db.hasGraph(name=ARANGODB_DATABASE['graph']):
    db.createGraph(ARANGODB_DATABASE['graph'])
theGraph = db.graphs["github"]