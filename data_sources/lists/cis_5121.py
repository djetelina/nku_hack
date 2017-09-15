# -*- encoding: utf-8 -*-
import pprint
import xml.etree.ElementTree


SOURCE_FILE = "raw_data/CIS5121_CS.xml"


def parse_file(fname):
    root = xml.etree.ElementTree.parse(fname).getroot()
    translate = {}
    for item in root.iter("POLOZKA"):
        code = item.find("CHODNOTA").text
        name = item.find("TEXT").text
        translate[code] = name
    print(len(translate))


if __name__ == '__main__':
    parse_file(SOURCE_FILE)
