import urllib
import urllib2
from endpoint import Host

class DispatcherRequest:
    path = None
    url = None
    args = {}
    headers = {}
    body = ''
    method = None

class DispatcherResponse:
    status_code = None
    headers = None
    body = None

    def __init__(self, status_code, headers, body):
        self.status_code = status_code
        self.headers = headers
        self.body = body

class HTTPDispatcher:
    def fetch(self, endpoint, request):
        response = None

        try:
            # build urllib2 request object and make request
            res = urllib2.urlopen(self.create_request_object(endpoint, request))

            if res is not None:
                response = DispatcherResponse(res.code, res.info().items(), res.read())
                res.close()

        except urllib2.HTTPError as e:
            response = DispatcherResponse(e.code, e.info().items(), e.read())
            e.close()

        return response

    def create_request_object(self, endpoint, request):
        req = urllib2.Request(self.create_uri(endpoint, request), request.body, request.headers)
        req.get_method = lambda: request.method
        return req

    def create_uri(self, endpoint, request):
        query = ''
        if len(request.args) > 0:
            query = '?' + urllib.urlencode(request.args)
        port = ''
        if endpoint.port != 0:
            port = ':' + str(endpoint.port)

        return endpoint.scheme + "://" + endpoint.host + port + request.path + query

if __name__ == '__main__':
    host = Host('localhost', 8084)

    disp_request = DispatcherRequest()
    disp_request.url = 'http://localhost:5000/oms-game-service/games/7056'
    disp_request.path = '/oms-game-service/games/7056'
    disp_request.args = {}
    disp_request.headers['Content-Length'] = 0
    disp_request.headers['Host'] = host.host
    disp_request.body = ''
    disp_request.method = 'GET'

    dispatcher = HTTPDispatcher()
    disp_response = dispatcher.fetch(host, disp_request)

    print disp_response.status_code
    print disp_response.headers
    print disp_response.body


