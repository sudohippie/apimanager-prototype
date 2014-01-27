__author__ = 'Raghav Sidhanti'

from flask import Flask
from flask import request
from werkzeug.routing import BaseConverter
from me.sudohippie.apimanager.http.Dispatcher import HTTPDispatcher, DispatcherRequest

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
    disp_response = dispatcher.fetch(get_dispatcher_request(request))
    return disp_response.body, disp_response.status_code, disp_response.headers

def get_dispatcher_request(disp_request):
    req = DispatcherRequest()
    req.url = disp_request.url
    req.path = disp_request.path
    req.args = disp_request.args

    for x, y in disp_request.headers:
        req.headers[x] = y
    req.headers['Content-Length'] = len(req.body)
    req.headers['Host'] = host

    req.body = disp_request.data
    req.method = disp_request.method

    return req

@app.route('/')
def empty_path():
    return non_empty_path("/")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
