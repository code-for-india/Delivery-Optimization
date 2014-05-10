__author__ = 'Animesh'

from flask import *
import sqlite3
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
    if route_id is None:
        abort(404)
    else:
        return return_response(route_id)

def return_response(route_id):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()

    command = ("SELECT * FROM SCHOOLS WHERE route_code = '%s'" % route_id)
    rows = c.execute(command).fetchall()

    routes = []
    for each_row in rows:
        location = {}
        location['Name'] = each_row[1]
        location['latitude'] = each_row[3]
        location['longitude'] = each_row[4]
        routes.append(location)

    '''
    params = dict(
        origins="13.045227,77.489358",
        destinations= "13.008345,77.611350|13.008860,77.610882",
        sensor="false"
    )
    url = "http://maps.googleapis.com/maps/api/distancematrix/"
    resp = requests.get(url=url, params=params)
    data = json.loads(resp.content)
    print data'''
    return jsonify({ 'routes': routes })


if __name__ == '__main__':
    app.run(debug = True)

