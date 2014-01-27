__author__ = 'Raghav Sidhanti'

from flask import Flask
from flask import request
from werkzeug.routing import BaseConverter
from me.sudohippie.apimanager.http.Dispatcher import HTTPDispatcher, Request

app = Flask(__name__)

class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]

app.url_map.converters['regex'] = RegexConverter

#url = 'http://www.epa.gov/greenvehicles/download/all_alpha_10.txt'
host = 'localhost'
port = 8084
scheme = 'http'

@app.route('/<regex(".*"):path>')
def non_empty_path(path):
    dispatcher = HTTPDispatcher(host, port, scheme)
    res = dispatcher.fetch(get_request(request))
    return res.body, res.status_code, res.headers

def get_request(request):
    req = Request()
    req.url = request.url
    req.path = request.path
    req.args = request.args

    for x, y in request.headers:
        req.headers[x] = y
    req.headers['Content-Length'] = len(req.body)
    req.headers['Host'] = host

    req.body = request.data
    req.method = request.method

    return req

@app.route('/')
def empty_path():
    return non_empty_path("/")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
