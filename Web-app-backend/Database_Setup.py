from IMPORT_DATA import arango_setup
from app.whooshIndexer.whooshIndexer import indexLibraries
from pyArango.connection import *
conn = Connection(username="root", password="root")
db = conn["TEST"]

arango_setup.setup()
indexLibraries(db, index_field="name", index_folder="index_fullname")
