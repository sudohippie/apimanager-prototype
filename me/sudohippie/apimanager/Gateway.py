__author__ = 'Raghav Sidhanti'

from flask import Flask
from flask import request
from werkzeug.routing import BaseConverter

app = Flask(__name__)

class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]

app.url_map.converters['regex'] = RegexConverter

@app.route('/<regex(".*"):path>')
def non_empty_path(path):
    print request.headers
    return path

@app.route('/')
def empty_path():
    return non_empty_path("/")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
