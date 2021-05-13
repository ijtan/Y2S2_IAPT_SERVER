import json
import os

_parsed_entries = None


def read_unesco_file(path=os.path.join('resources', 'jsonified_unesco_data.json')):
    entries = {}
    with open(path,encoding="utf-8") as json_file:
        data = json.load(json_file)
        for entry in data['row']:            
            entry_info = {}
            entry_info['title'] = entry['site']
            # entry_info['country'] = entry['states']
            entry_info['short_desc'] = f"A {entry['category'].lower()} site in {entry['location']}"
            entry_info['long_desc'] = entry['short_description']
            entry_info['lat'] = float(entry['latitude'])
            entry_info['lon'] = float(entry['longitude'])
            entry_info['imageurl'] = entry['image_url']
            # entry_info['rad'] = 20

            entries[(entry_info['lat'], entry_info['lon'])] = entry_info
    return entries


def read_council_file(path=os.path.join('resources', 'localCouncilData.json')):
    entries = {}
    data = []
    with open(path,encoding="utf-8") as json_file:
        data = json.load(json_file)
    for entry in data:
        entry_info = {}

        entry_info['lat'] = float(entry["Geolocation Coordinates"].split(',')[0])
        entry_info['lon'] = float(entry["Geolocation Coordinates"].split(',')[1])

        entry["Heritage Site Description"] = ''.join([i for i in entry["Heritage Site Description"] if i.isalpha()])
        entry_info['title'] = entry["Heritage Site Description"]
        entry_info['short_desc'] = f"A {entry['Type'].lower()} found in {entry['Location'].lower()}"
        entry_info['long_desc']  = entry_info['short_desc']
        entry_info['imageurl'] = ''

        entries[(entry_info['lat'], entry_info['lon'])] = entry_info
    return entries

        

def getData():
    global _parsed_entries
    if _parsed_entries is None:
        _parsed_entries = read_unesco_file()
        _parsed_entries.update(read_council_file())
        print(f'Externally retrieved {len(_parsed_entries)} entries')

    return _parsed_entries



if __name__ == '__main__':
    entries = getData()

    assets = {}
    for entry in getData().values():
        newentry = {'lat': entry['lat'], 'lon': entry['lon'], 'rad': 20, 'imageurl': '', 'display_name': entry['title'], 'short_desc': entry['short_desc'], 'long_desc': entry['long_desc'],'imageurl': entry['imageurl']}

        assets[entry['title'].lower()] = newentry
