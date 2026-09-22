import json
import re
import os

# 1. Get flags from InteractiveMap.tsx
with open('src/components/map/InteractiveMap.tsx', 'r', encoding='utf-8') as f:
    map_code = f.read()

country_data_block = map_code.split('const countryData: Record<string, any> = {')[1].split('};')[0]
flag_urls = re.findall(r"flagUrl:\s*'([^']+)'", country_data_block)
expected_flags = set([url.replace('/flags/', '') for url in flag_urls])

# 2. Get flags from world-1939.json for injected properties
with open('src/data/geojson/world-1939.json', 'r', encoding='utf-8') as f:
    geojson = json.load(f)

for feat in geojson.get('features', []):
    props = feat.get('properties', {})
    if 'leader' in props and 'name' in props:
        name = props['name'].lower().replace(' ', '_')
        expected_flags.add(f'{name}.jpeg')

# 3. Read actual flags (case insensitive matching)
actual_flags_raw = os.listdir('public/flags')
actual_flags = set([f.lower() for f in actual_flags_raw])

# Print missing
missing = []
for expected in expected_flags:
    if expected.lower() not in actual_flags:
        missing.append(expected)

print("MISSING_FLAGS:")
for m in sorted(missing):
    print(m)
