__author__ = 'Animesh'

from flask import *
import sqlite3
import flask
import urllib2
import json, requests
app = Flask(__name__)

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
    conn2 = sqlite3.connect()
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

