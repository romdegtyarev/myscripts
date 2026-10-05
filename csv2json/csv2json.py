#!/usr/bin/env python3

import csv
import json

with open('test.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    rows = list(reader)

with open('test.json', 'w', encoding='utf-8') as jsonfile:
    json.dump(rows, jsonfile, indent=4, ensure_ascii=False)

