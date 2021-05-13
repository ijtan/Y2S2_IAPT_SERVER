import json
import os

_parsed_entries = None


def read_file(path_to_xml=os.path.join('resources', 'jsonified_unesco_data.json')):
    entries = {}
    with open(path_to_xml,encoding="utf-8") as json_file:
        data = json.load(json_file)
        for entry in data['row']:            
            entry_info = {}
            entry_info['title'] = entry['site']
            entry_info['country'] = entry['states']
            entry_info['short_desc'] = f"A {entry['category'].lower()} site in {entry['location']}"
            entry_info['long_desc'] = entry['short_description']
            entry_info['lat'] = float(entry['latitude'])
            entry_info['lon'] = float(entry['longitude'])
            entry_info['imageurl'] = entry['image_url']
            # entry_info['rad'] = 20

            entries[(entry_info['lat'], entry_info['lon'])] = entry_info
    return entries


def getData():
    global _parsed_entries
    if _parsed_entries is None:
        _parsed_entries = read_file()

    return _parsed_entries



if __name__ == '__main__':
    entries = getData()
    for coords,data in entries.items():
        if "malta" in data['country'].lower():
            print(data['title'])
            print(f'Key is {coords}')
