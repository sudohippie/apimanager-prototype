__author__ = 'Raghav Sidhanti'

from flask import Flask
from flask import request
from werkzeug.routing import BaseConverter
import http.dispatcher
import http.endpoint
import http.loadbalancer

app = Flask(__name__)

class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]

app.url_map.converters['regex'] = RegexConverter
endpoints = http.endpoint.get_endpoints()
lb = http.loadbalancer.ConsistentHashLoadBalancer(endpoints)

@app.route('/')
def empty_path():
    return non_empty_path("/")

@app.route('/<regex(".*"):path>')
def non_empty_path(path):
    disp_response = process(request)
    return disp_response.body, disp_response.status_code, disp_response.headers

def process(request):
    # load balancer
    endpoint = lb.balance_load(request.path)

    # make request
    dispatcher = http.dispatcher.HTTPDispatcher()
    disp_resp = dispatcher.fetch(endpoint, build_dispatcher_request(endpoint, request))

    return disp_resp

def build_dispatcher_request(endpoint, request):
    disp_request = http.dispatcher.DispatcherRequest()
    disp_request.path = request.path
    disp_request.args = request.args

    for x, y in request.headers:
        disp_request.headers[x] = y
    disp_request.headers['Content-Length'] = len(disp_request.body)
    disp_request.headers['Host'] = endpoint.host

    disp_request.body = request.data
    disp_request.method = request.method

    return disp_request

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
