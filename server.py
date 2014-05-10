__author__ = 'Animesh'

from flask import *
import sqlite3
import json, requests
app = Flask(__name__)

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
        location['latitude'] = each_row[3]
        location['longitude'] = each_row[4]
        routes.append(location)
    params = dict(
        origins="13.045227,77.489358",
        destinations= "13.008345,77.611350|13.008860,77.610882",
        sensor="false"
    )
    url = "http://maps.googleapis.com/maps/api/distancematrix/"
    resp = requests.get(url=url, params=params)
    data = json.loads(resp.content)
    print data
    return jsonify({ 'routes': routes })


if __name__ == '__main__':
    app.run(debug = True)

