#!/usr/bin/env python3

import json
import sys

# open the input file and parse the correct informations
with open(sys.argv[1]) as in_file:
    in_json = json.load(in_file)

# append the informations to the output file
with open(sys.argv[2]) as out_file:
    out_json = json.load(out_file)

for k, v in in_json["_via_img_metadata"].items():
    out_json[k] = v

with open(sys.argv[2], "w") as f:
    json.dump(out_json, f, indent=4)