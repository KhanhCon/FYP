from flask import Flask, jsonify, request
from flask_caching import Cache
from flask_cors import CORS
import os

import arangodbQuery
from app.whooshIndexer import whooshQuery

app = Flask(__name__)
CORS(app)

dirname = os.path.dirname(os.path.abspath(__file__))
cache = Cache(app, config={'CACHE_TYPE': 'filesystem', 'CACHE_DIR':os.path.join(dirname, 'cached'), 'CACHE_DEFAULT_TIMEOUT':9000000,'CACHE_THRESHOLD': 20000})
# cache = Cache(app, config={'CACHE_TYPE': 'redis', 'CACHE_REDIS_HOST': '12121.0.0'})

from pyArango.connection import *

conn = Connection(username="root", password="root")
db = conn["TEST"]

arangograph = 'github'


@app.route('/top')
@cache.cached(query_string=True)
def topLibraries():
    # http://127.0.0.1:5000/top?date=2018-10-02&numberof_libraries=10&collection=libraries&graph=github_test
    query = request.args
    return jsonify(list(
        arangodbQuery.getTopLibraries(db, graph=arangograph, collection='libraries', date=query["date"],
                                          numOfLibs=query["numberof_libraries"])))


@app.route('/topcurrent')
@cache.cached(query_string=True)
def topLibrariesCurrent():
    # http://127.0.0.1:5000/top?date=2018-10-02&numberof_libraries=10&collection=libraries&graph=github_test
    query = request.args
    return jsonify(list(
        arangodbQuery.getCurrentTopLibraries(db, graph=arangograph, collection='libraries',
                                                 numOfLibs=query["numberof_libraries"])))


@app.route('/dependencies')
def getDependencies():
    # http://127.0.0.1:5000/dependencies?date=2018-10-02&document=libraries/bcit-ci_CodeIgniter&graph=github_test
    query = request.args
    return jsonify(
        list(
            arangodbQuery.getDependencies(db, graph=query['graph'], document=query['document'], date=query["date"])))


@app.route('/search')
def searchDocuments():
    # http://127.0.0.1:5000/dependencies?date=2018-10-02&document=libraries/bcit-ci_CodeIgniter&graph=github_test
    query = request.args
    s = whooshQuery.search(qstring=query['query'])
    ids, searchSuggestions = s["ids"], s["suggestions"]
    result = arangodbQuery.getUsages(db, ids,graph=arangograph)
    return jsonify({"result": list(result),
                    "suggestions": searchSuggestions})


@app.route('/compare')
def getCompare():
    # http://127.0.0.1:5000/dependencies?date=2018-10-02&document=libraries/bcit-ci_CodeIgniter&graph=github_test
    query = request.args
    json = { "name": query['name'],
            "id": "compare",
            "data": list(arangodbQuery.getUsageOverTime(db, document=query["library"]))}
    return jsonify(json)


@app.route('/usageovertime')
@cache.cached(query_string=True)
def getUsageOverTime():
    # http://127.0.0.1:5000/dependencies?date=2018-10-02&document=libraries/bcit-ci_CodeIgniter&graph=github_test
    query = request.args
    json = {"highstock": True, "chart": {"defaultSeriesType": "area", "backgroundColor": "transparent",
                                         "style": {"background-repeat": "no-repeat", "background-position": "50% 50%"},
                                         "marginLeft": 0},
            "plotOptions": {"series": {"cursor": "arrow", "dataGrouping": {"enabled": False}}, "type": {},
                            "area": {"stacking": "normal"}},
            "yAxis": {"min": 0, "endOnTick": False, "showLastLabel": True, "maxPadding": 0.25}, "xAxis": {
            "dateTimeLabelFormats": {"millisecond": "%Y", "tickInterval": 31557600000.0, "minPadding": 0.015,
                                     "maxPadding": 0.015}},
            "tooltip": {"xDateFormat": "%B %Y", "headerFormat": "{point.key}",
                        "style": {"padding": "12px"}},
            "navigator": {"series": {"type": "area"}, "xAxis": {"dateTimeLabelFormats": {"millisecond": "%Y"}},
                          "yAxis": {"min": 0}, "dataGrouping": {"enabled": False}, "enabled": False},
            "credits": {"enabled": False}, "exporting": {"enabled": False}, "title": "Total Lines",
            "series": [
                {
                    "name": "Usage",
                    "id": "usage",
                    "data": list(arangodbQuery.getUsageOverTime(db, document=query["library"]))
                }],
            "rangeSelector": {"inputEnabled": False, "buttons": [{"type": "year", "count": 1, "text": "1yr"},
                                                                 {"type": "year", "count": 3, "text": "3yr"},
                                                                 {"type": "year", "count": 5, "text": "5yr"},
                                                                 {"type": "year", "count": 10, "text": "10yr"},
                                                                 {"type": "all", "text": "All"}], "selected": 4,
                              "enabled": False}, "scrollbar": {"enabled": False},
            "legend": {"enabled": False, "layout": "horizontal", "align": "center", "verticalAlign": "bottom", "x": 0,
                       "y": 0, "floating": False, "backgroundColor": "#ffffff"}}

    return jsonify(json)

@app.route('/relevant')
def getRelevantLibraries():
    # http://127.0.0.1:5000/dependencies?date=2018-10-02&document=libraries/bcit-ci_CodeIgniter&graph=github_test
    query = request.args
    return jsonify(
        list(arangodbQuery.getRelevantLibrary(db, document=query['library'], graph=arangograph)))

@app.route('/firstShaDate')
@cache.cached(query_string=True)
def getFirstShaDate():
    return jsonify({'date' : arangodbQuery.getFirstShaDate(db)[0]})

@app.route('/getLibrary')
def getLibrary():
    query = request.args
    return jsonify(arangodbQuery.getLibrary(db, libraryID=(query['libraryID'])))

if __name__ == '__main__':
    # print(getUsageOverTime())
    # cache.clear()
    app.run(host='0.0.0.0',debug=False)
