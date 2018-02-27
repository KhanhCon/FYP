from flask import Flask, jsonify, request
import Query
app = Flask(__name__)

from pyArango.connection import *
conn = Connection(username="root", password="root")
db = conn["test_fetch"]

@app.route('/top')
def topLibraries():
    #http://127.0.0.1:5000/top?date=2018-10-02&numberof_libraries=10&collection=libraries&graph=github_test
    query = request.args
    return jsonify(list(Query.getTopLibraries(db,graph=query['graph'], collection=query['collection'], date=query["date"], numOfLibs=query["numberof_libraries"])))

@app.route('/dependencies')
def getDependencies():
    #http://127.0.0.1:5000/dependencies?date=2018-10-02&document=libraries/bcit-ci_CodeIgniter&graph=github_test
    query = request.args
    return jsonify(list(Query.getDependencies(db,graph=query['graph'], document=query['document'], date=query["date"])))

if __name__ == '__main__':
    app.run()
