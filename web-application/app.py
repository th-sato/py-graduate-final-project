from flask import Flask, request, render_template
from flask_cors import CORS, cross_origin
from env import *
import logging
import redis

app = Flask(__name__)
r = redis.Redis(host=REDIS_IP, port=REDIS_PORT, db=0)
CORS(app, support_credentials=True)
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/redis-image', methods=['GET', 'POST'])
# @cross_origin(supports_credentials=True)
def image():
    if request.method == 'GET':
        img = r.get(REDIS_KEY_IMAGE)
        if img is not None:
            return HTML_IMAGE_HEADER + img, 200
        else:
            return "", 200
    elif request.method == 'POST':
        json = request.get_json()
        r.set(REDIS_KEY_IMAGE, json['image'])
        return "OK", 200
    else:
        return "Method not found", 404


# @app.route('/calibration', methods=['POST'])
# def teste():
#     json = request.get_json()
#     print json['wheel']
#     print json['action']
#     return "OK", 200


if __name__ == "__main__":
    # app.run(host=HOST, port=PORT, debug=False)
    app.run(host=FLASK_HOST, port=FLASK_PORT, debug=True)
