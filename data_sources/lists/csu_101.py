# -*- encoding: utf-8 -*-
import pprint
import xml.etree.ElementTree


SOURCE_FILE = "raw_data/CIS0101_CS.xml"


def parse_file(fname):
    root = xml.etree.ElementTree.parse(fname).getroot()
    translate_ruian = {}
    translate_text = {}

    for item in root.iter("POLOZKA"):
        code = int(item.find("CHODNOTA").text)
        name = item.find("TEXT").text
        ruian = filter(lambda x: x.get("akronym") == "KOD_RUIAN", item.find("ATRIBUTY").findall("ATR"))[0].text
        if not ruian:
            continue
        ruian = int(ruian)
        translate_ruian[code] = ruian
        translate_text[code] = name

    pprint.pprint({
        'CSU_101_TO_RUIAN': translate_ruian,
        'CSU_101_TO_NAME': translate_text
    })


if __name__ == '__main__':
    parse_file(SOURCE_FILE)
