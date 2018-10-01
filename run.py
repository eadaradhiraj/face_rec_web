#!/usr/bin/env python3

from bottle import route, run, static_file, request
from PIL import Image
import re
from io import BytesIO
import base64


@route('/node_modules/tracking/build/tracking-min.js')
def tracking_js():
    return static_file('tracking-min.js', root='node_modules/tracking/build/')


@route('/node_modules/tracking/build/data/face-min.js')
def serve_face_min():
    return static_file('face-min.js', root='node_modules/tracking/build/data/')


@route('/node_modules/jquery/dist/jquery.min.js')
def jquery_js():
    return static_file('jquery.min.js', root='node_modules/jquery/dist/')


@route(r'/static/js/<filename:re:.*\.js>')
def static_js(filename):
    return static_file(filename, root='static/js/')


@route('/test', method='POST')
def serve_image():
    image_data = re.sub('^data:image/.+;base64,', '', request.forms['data'])
    image = Image.open(BytesIO(base64.b64decode(image_data)))
    image.show()


@route(r'/static/css/<filename:re:.*\.css>')
def static_css(filename):
    return static_file(filename, root='static/css/')


@route('/')
def server_index():
    return static_file('index.html', root='.')


run(host='localhost', port=8080, debug=True)
