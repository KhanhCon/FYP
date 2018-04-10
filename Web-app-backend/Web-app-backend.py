from flask import Flask, jsonify, request
from flask_cors import CORS
import Query
import whooshQuery

app = Flask(__name__)
CORS(app)

from pyArango.connection import *

conn = Connection(username="root", password="root")
db = conn["New"]


@app.route('/top')
def topLibraries():
    # http://127.0.0.1:5000/top?date=2018-10-02&numberof_libraries=10&collection=libraries&graph=github_test
    query = request.args
    return jsonify(list(
        Query.getTopLibraries(db, graph='github_test', collection='libraries', date=query["date"],
                              numOfLibs=query["numberof_libraries"])))


@app.route('/topcurrent')
def topLibrariesCurrent():
    # http://127.0.0.1:5000/top?date=2018-10-02&numberof_libraries=10&collection=libraries&graph=github_test
    query = request.args
    return jsonify(list(
        Query.getCurrentTopLibraries(db, graph='github_test', collection='libraries',
                                     numOfLibs=query["numberof_libraries"])))


@app.route('/dependencies')
def getDependencies():
    # http://127.0.0.1:5000/dependencies?date=2018-10-02&document=libraries/bcit-ci_CodeIgniter&graph=github_test
    query = request.args
    return jsonify(
        list(Query.getDependencies(db, graph=query['graph'], document=query['document'], date=query["date"])))


@app.route('/search')
def searchDocuments():
    # http://127.0.0.1:5000/dependencies?date=2018-10-02&document=libraries/bcit-ci_CodeIgniter&graph=github_test
    query = request.args
    s = whooshQuery.search(qstring=query['query'])
    ids, searchSuggestions = s["ids"], s["suggestions"]
    result = Query.getUsages(db, ids)
    return jsonify({"result": list(result),
                    "suggestions": searchSuggestions})


@app.route('/usageovertime')
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
                    "data": list(Query.getUsageOverTime(db, document=query["library"]))
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
        list(Query.getRelevantLibrary(db, document=query['library'])))


if __name__ == '__main__':
    # print(getUsageOverTime())
    app.run()
