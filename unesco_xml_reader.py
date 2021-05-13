import xml.etree.ElementTree as ET
import os


def read_file(path_to_xml=os.path.join('resources', 'UNESCO_WROLD_HERITAGE.xml')):

    tree = ET.parse(path_to_xml)
    root = tree.getroot()

    for row in root[:10]:
        for child in row:
            print(child.tag, child.attrib)


if __name__ == '__main__':
    read_file()