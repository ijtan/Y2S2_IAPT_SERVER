from flask import Flask, jsonify, request
import json
import os
from flask.helpers import send_from_directory
import numpy as numpy
import device

import external_data


assets = {
    'history museum': {'lat': 35.883511, 'lon': 14.394178, 'rad': 15, 'imageurl': ['https://www.freeiconspng.com/uploads/art-history-museum-icon--4.png', 'https://icon-library.com/images/museum-icon-png/museum-icon-png-0.jpg'], 'display_name': 'History Museum', 'short_desc': 'The National History Museum of Malta!',
    'long_desc': 'This museum was estabilished in 1918, and it contains some of the most iconic findings in the history of this island. This is one of the hottest attrcations in mdina, as it contextualizes the whole country.'},
    # 'starbucks': {'lat': 35.883791, 'lon': 14.394039, 'rad': 5, 'imageurl': [''], 'display_name': 'Starbucks', 'short_desc': 'Grab a coffee at Starbucks!', 'long_desc': ''},
    'north pole': {'lat': 90, 'lon': 0, 'rad': 5, 'imageurl': [''], 'display_name': 'North Pole!', 'short_desc': 'Chill!', 'long_desc': ''}
}

# newEntries = []
for entry in external_data.getData().values():
    newentry = {'lat': entry['lat'], 'lon': entry['lon'], 'rad': 20, 'imageurl': '', 'display_name': entry['title'],
                'short_desc': entry['short_desc'], 'long_desc': entry['long_desc'], 'imageurl': entry['imageurl']}

    assets[entry['title'].lower()] = newentry
# assets.update()

app = Flask(__name__)
UPLOAD_FOLDER = 'resources/Android/'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


devices = {}


@app.route('/')
def root():
    return jsonify('Welcome to Ethan\'s IAPT Project!')


@app.route('/getFullNear')
def getAllNear():
    toRet = []

    args = request.args
    uid = args.get('uid')
    for key, data in assets.items():
        distance = device.getDevice(devices, uid).getDist(
            data['lat'], data['lon'])
        if distance <= ((3)*1000) or key =='north pole':

            isNear = False
            if key in assets and device.getDevice(devices, uid).isNear(data['lat'], data['lon'], data['rad']):
                isNear = True

            resp = {
                'near': isNear,
                'locX': data['lat'],
                'locY': data['lon'],
                'title': data['display_name'],
                'short_description': data['short_desc'],
                'long_description': data['long_desc'],
                'image_urls': data['imageurl'],
                'id':key

            }
            toRet.append(resp)
    # toRet = toRet[:1]
    return jsonify({'landmarks': toRet})


@app.route('/getKeys')
def getKeys():
    keys = []

    args = request.args
    uid = args.get('uid')
    for key, data in assets.items():
        distance = device.getDevice(devices, uid).getDist(data['lat'], data['lon'])
        if distance <= ((3)*1000):
            keys.append(key)
    # print(f'Returning {len(keys)} keys to device: {uid} at {device.getDevice(devices, uid).lat} {device.getDevice(devices, uid).lon}')

    # keys = list(assets.keys())[:5]
    keys.append('north pole')

    return jsonify({'landmarks': keys})


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
    isNear = False
    if loc in assets and device.getDevice(devices, uid).isNear(assets[loc]['lat'], assets[loc]['lon'], assets[loc]['rad']):
        isNear = True
    # isNear = True
    # isNear = False
    resp = {
        'near': isNear,
        'locX': assets[loc]['lat'],
        'locY': assets[loc]['lon'],
        'title': assets[loc]['display_name'],
        'short_description': assets[loc]['short_desc'],
        'long_description': assets[loc]['long_desc'],
        'image_url': assets[loc]['imageurl']

    }
    # print('Returning', resp)
    return jsonify(resp)


@app.route('/Android/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    uploads = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
    return send_from_directory(directory=uploads, filename=filename)


def run():
    app.run(debug=True, host='0.0.0.0')


if __name__ == '__main__':
    run()
