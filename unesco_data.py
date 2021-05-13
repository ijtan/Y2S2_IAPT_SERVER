import json
import os

_parsed_entries = None

def read_file(path_to_xml=os.path.join('resources', 'world-heritage-unesco-list.json')):
    entries = {}
    with open(path_to_xml,encoding="utf-8") as json_file:
        data = json.load(json_file)
        for entry in data:            
            entry_info = {}
            entry_info['title'] = entry['fields']['name_en']
            entry_info['country'] = entry['fields']['country_en']
            entry_info['desc'] = entry['fields']['short_description_en']
            entry_info['lat'] = entry['fields']['latitude']
            entry_info['lon'] = entry['fields']['longitude']
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
