from app.Fetcher.Fetcher import fetchJobs, fetchGraph
from app.whooshIndexer.whooshIndexer import indexLibraries
import os, subprocess

if __name__ == "__main__":
    from pyArango.connection import *
    conn = Connection(username="root", password="root")
    db = conn["TEST"]

    try:
        print("Fetching jobs")
        fetchingGraph = False
        # fetchJobs(db)
        print("Fetching Graph")
        fetchingGraph = True
        fetchGraph(db)
    finally:
        if fetchingGraph == True:
            indexLibraries(db, index_field="name", index_folder="index_fullname")



            # indexLibraries(db, index_field="name", index_folder="index_fullname")