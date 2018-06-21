"""
This is the server side for GreenPath
"""

from bottle import route, run, get, template, static_file, request, response, debug
import json
from src.user import User


@get("/")
def index():
    return template("index.html")


@route("/newroute", method='POST')
def handle_route_request():
    user_preferences = request.POST.get('userPreferences')
    user_preferences = json.loads(user_preferences)
    print (user_preferences['startLocation'])
    #user = User(user_preferences)
    reply = {}
    reply["STATUS"] = "SUCCESS"
    reply["WAYPOINTS"] = [{"latitude": 43.733, "longitude": -73.26}, {"latitude": 43.133, "longitude": -73.96}]
    return json.dumps(reply)


@route('/js/<filename:re:.*\.js>', method='GET')
def javascripts(filename):
    return static_file(filename, root='js')


@route('/css/<filename:re:.*\.css>', method='GET')
def stylesheets(filename):
    return static_file(filename, root='css')


@route('/images/<filename:re:.*\.(jpg|png|gif|ico)>', method='GET')
def images(filename):
    return static_file(filename, root='images')


def main():
    run(host="localhost", port=7000)


if __name__ == '__main__':
    main()
