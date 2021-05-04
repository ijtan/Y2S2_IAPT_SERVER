from haversine import haversine

class device:
    lat = 0
    lon = 0
    uid = -1;


    def __init__(self,uid,lat=0,lon=0):
        self.uid = uid
        self.lat = lat
        self.lon = lon

    def updateLoc(self,lat,lon):
        self.lat = lat
        self.lon = lon

    def isNear(self,lat,lon,cutoff):
        point = (lat,lon)
        device = (self.lat,self.lon)
        distance = haversine(point, device, unit='m')
        print(f'(LT,LN) Device: {self.lat},{self.lon} - Landmark: {lat},{lon} - Distance is:', distance)
        return distance<=cutoff



def getDevice(devices,uid):
    if uid not in devices:
        devices[uid] = device(uid)
        return devices[uid]
    else:
        devices[uid].uid = uid
        return devices[uid]
