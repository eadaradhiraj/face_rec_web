#!/usr/bin/env python3

from bottle import route, run, static_file, request, response
import re
import json
from io import BytesIO
import base64
import test


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
    prediction = test.predict(X_img_path=BytesIO(base64.b64decode(
        image_data)), model_path="static/data/knn_model.sav")
    response.content_type = 'application/json'
    return json.dumps(prediction)


@route(r'/static/css/<filename:re:.*\.css>')
def static_css(filename):
    return static_file(filename, root='static/css/')


@route('/')
def server_index():
    return static_file('index.html', root='.')


run(host='localhost', port=8080, debug=True)
