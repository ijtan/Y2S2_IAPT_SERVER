from flask import Flask, jsonify, request
import json
import os
from flask.helpers import send_from_directory
import numpy as numpy
import device


app = Flask(__name__)
UPLOAD_FOLDER = 'resources/Android/'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


devices = {}


@app.route('/')
def root():
    return jsonify('Welcome to Ethan\'s IAPT Project!')


@app.route('/getNear')
def getNear():
    args = request.args
    lat = float(args.get('lat'))
    lon = float(args.get('lon'))
    uid = args.get('uid')

    if args is None or lat is None or uid is None:
        return jsonify('Error whilst parsing args')

    print(f'Updating location of device {uid} to: lat {lat} lon {lon} ')

    device.getDevice(devices, uid).updateLoc(lat, lon)

    return jsonify('Updated Device!')

# valid = ['sphere ad']


# assets = {
#     'geographic museum': {'lat': 35.883511, 'lon': 14.394178, 'rad': 15, 'desc': 'Earth spinnng shpere'},
#     'starbucks': {'lat': 35.883791, 'lon': 14.394039, 'rad': 5, 'desc': 'Starbucks!'}
# }

assets = {
    'geographic museum': {'lat': 35.883511, 'lon': 14.394178, 'rad': 15, 'desc': 'Earth spinnng shpere', 'imageurl': '', 'display_name': ''},
    'starbucks': {'lat': 35.883791, 'lon': 14.394039, 'rad': 5, 'desc': 'Starbucks!', 'imageurl': '', 'display_name': ''}
}


@app.route('/isNear')
def isNear():
    # resp = {'near': False, 'distance': 99}
    # print('Returning', resp)
    # return jsonify(resp)
    args = request.args
    loc = args.get('loc').split('/')[-1].split('.')[0].lower()
    uid = args.get('uid')
    if loc is None or uid is None:
        return jsonify('Error whilst parsing args')

    print(f'Got Request for asset check: \'{loc}\'')
    distance = device.getDevice(devices, uid).getDist(
        assets[loc]['lat'], assets[loc]['lon'])
    # distance = 5
    isNear = False;
    if loc in assets and device.getDevice(devices, uid).isNear(assets[loc]['lat'], assets[loc]['lon'], assets[loc]['rad']):
        isNear=True

    resp = {
        'near': isNear,        
        'locX': assets[loc]['lat'],
        'locY': assets[loc]['lon'],
        'title': assets[loc]['display_name'],
        'description': assets[loc]['desc'],
        'image_url': assets[loc]['imageurl']

    }
    print('Returning', resp)
    return jsonify(resp)


@app.route('/Android/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    uploads = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
    return send_from_directory(directory=uploads, filename=filename)


def run():
    app.run(debug=True, host='0.0.0.0')


if __name__ == '__main__':
    run()
