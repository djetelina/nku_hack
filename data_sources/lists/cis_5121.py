# -*- encoding: utf-8 -*-


import xml.etree.ElementTree
import gzip


SOURCE_FILE = "raw_data/CIS5121_CS.xml"
DEST_FILE = "dump/diseases.sql.gz"

TABLE_SQL = """
BEGIN;
CREATE TABLE disease (
  code varchar(3) PRIMARY KEY,
  name varchar(255)
);
"""


def parse_file(fname):
    root = xml.etree.ElementTree.parse(fname).getroot()
    translate = {}
    gzf = gzip.GzipFile(DEST_FILE, "w", compresslevel=9)
    gzf.write(bytes(TABLE_SQL, 'utf-8'))
    for item in root.iter("POLOZKA"):
        code = item.find("CHODNOTA").text
        name = item.find("TEXT").text
        translate[code] = name
        gzf.write(bytes("INSERT INTO disease VALUES ('{}', '{}');\n".format(code, name), 'utf-8'))
    gzf.write(b"COMMIT;\n")
    gzf.flush()
    gzf.close()


if __name__ == '__main__':
    parse_file(SOURCE_FILE)
