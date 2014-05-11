__author__ = 'Animesh'

from flask import *
import sqlite3
import flask
import urllib2
import json, requests
app = Flask(__name__)

@app.before_request
def option_autoreply():
    """ Always reply 200 on OPTIONS request """

    if request.method == 'OPTIONS':
        resp = app.make_default_options_response()

        headers = None
        if 'ACCESS_CONTROL_REQUEST_HEADERS' in request.headers:
            headers = request.headers['ACCESS_CONTROL_REQUEST_HEADERS']

        h = resp.headers

        # Allow the origin which made the XHR
        h['Access-Control-Allow-Origin'] = request.headers['Origin']
        # Allow the actual method
        h['Access-Control-Allow-Methods'] = request.headers['Access-Control-Request-Method']
        # Allow for 10 seconds
        h['Access-Control-Max-Age'] = "10"

        # We also keep current headers
        if headers is not None:
            h['Access-Control-Allow-Headers'] = headers

        return resp


@app.after_request
def set_allow_origin(resp):
    """ Set origin for GET, POST, PUT, DELETE requests """

    h = resp.headers

    # Allow crossdomain for other HTTP Verbs
    if request.method != 'OPTIONS' and 'Origin' in request.headers:
        h['Access-Control-Allow-Origin'] = request.headers['Origin']


    return resp

@app.route('/')
def parse_request():
    route_id = request.args.get('r', None)
    kitchen_id = request.args.get('k', None)
    if route_id is None:
        abort(404)
    else:
        return return_response(route_id, kitchen_id)

def return_response(route_id, kitchen_id):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()



    command = ("SELECT * FROM SCHOOLS WHERE route_code = '%s' AND kitchen_location = '%s'" % (route_id, kitchen_id))
    rows = c.execute(command).fetchall()
    print rows
    routes = []
    for each_row in rows:
        print each_row
        location = {}
        location['name'] = each_row[1]
        location['latitude'] = each_row[3]
        location['longitude'] = each_row[4]
        routes.append(location)
    conn.commit()
    c.close()
    conn.close()

    bus_routes = {}
    bus_routes['routes']=routes

    conn2 = sqlite3.connect('kitchens.db')
    c2 = conn2.cursor()
    


    command = ("SELECT * FROM Kitchens WHERE Name = '%s'" % kitchen_id)
    row = c2.execute(command).fetchall()
    #print row
    bus_routes['kitchen'] = {'latitude':row[0][2], 'longitude':row[0][3]}
    conn2.commit()
    c2.close()
    conn2.close()

    return flask.jsonify(**bus_routes)

if __name__ == '__main__':
    app.run(debug = True)

