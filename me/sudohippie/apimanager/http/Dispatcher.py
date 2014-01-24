import urllib
import urllib2

class Request:
    path = None
    url = None
    args = {}
    headers = {}
    body = ''
    method = None

class Response:
    status_code = None
    headers = None
    body = None

    def __init__(self, status_code, headers, body):
        self.status_code = status_code
        self.headers = headers
        self.body = body

class HTTPDispatcher:
    fwd_host = None
    fwd_port = None
    scheme = None

    def __init__(self, fwd_host=None, fwd_port=None, scheme=None):
        self.fwd_host = fwd_host
        self.fwd_port = fwd_port
        self.scheme = scheme

    def fetch(self, request):
        response = None

        try:
            # build urllib2 request object and make request
            res = urllib2.urlopen(self.create_request_object(request))

            if res is not None:
                response = Response(res.code, res.info().items(), res.read())
                res.close()

        except urllib2.HTTPError as e:
            response = Response(e.code, e.info().items(), e.read())
            e.close()

        return response

    def create_request_object(self, request):
        req = urllib2.Request(self.create_uri(request), request.body, request.headers)
        req.get_method = lambda: request.method
        return req

    def create_uri(self, request):
        query = ''
        if len(request.args) > 0:
            query = '?' + urllib.urlencode(request.args)
        port = ''
        if self.fwd_port is not None:
            port = ':' + str(self.fwd_port)

        return self.scheme + "://" + self.fwd_host + port + request.path + query


