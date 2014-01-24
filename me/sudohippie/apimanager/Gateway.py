__author__ = 'Raghav Sidhanti'

from flask import Flask
from flask import request
from werkzeug.routing import BaseConverter
from httplib import HTTPConnection

app = Flask(__name__)

class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]

app.url_map.converters['regex'] = RegexConverter

#url = 'http://www.epa.gov/greenvehicles/download/all_alpha_10.txt'
hostname = 'www.epa.gov'

@app.route('/<regex(".*"):path>')
def non_empty_path(path):
    return get_data(request, path)

@app.route('/')
def empty_path():
    return non_empty_path("/")

def get_data(request, path):
    print dict((str(x),  str(y)) for x, y in request.headers)
    conn = HTTPConnection(hostname)
    conn.request('GET', path, '', dict((str(x),  str(y)) for x, y in request.headers))
    response = conn.getresponse()
    print response.status, response.reason
    data = response.read()
    return data

def get_header_tuple(headers):
    header_list = {}
    for header in headers:
        header_list.append(header)
    return header_list


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
