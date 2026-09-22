import json
import os

with open('src/data/geojson/world-1939.json', 'r', encoding='utf-8') as f:
    geojson = json.load(f)

expected_flags = set()
for feat in geojson.get('features', []):
    props = feat.get('properties', {})
    if 'flagUrl' in props:
        flag = props['flagUrl'].replace('/flags/', '')
        expected_flags.add(flag)

actual_flags_raw = os.listdir('public/flags')
actual_flags = set([f.lower() for f in actual_flags_raw])

missing = []
for expected in expected_flags:
    if expected.lower() not in actual_flags:
        missing.append(expected)

print("MISSING_FLAGS:")
for m in sorted(missing):
    print(m)
