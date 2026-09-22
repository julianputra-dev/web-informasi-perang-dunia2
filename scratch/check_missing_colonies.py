import json
import re

with open('src/components/map/InteractiveMap.tsx', 'r', encoding='utf-8') as f:
    map_code = f.read()

country_data_block = map_code.split('const countryData: Record<string, any> = {')[1].split('};')[0]
keys = set(re.findall(r"^\s*'([^']+)':", country_data_block, re.MULTILINE))

with open('src/data/geojson/world-1939.json', 'r', encoding='utf-8') as f:
    geojson = json.load(f)

geojson_names = set([feat.get('properties', {}).get('name') for feat in geojson.get('features', []) if feat.get('properties', {}).get('name')])

print('=== GeoJSON features with colony-like names NOT IN countryData ===')
keywords = ['koloni', 'protektorat', 'mandat', 'teritori', 'boneka', 'dominion', 'jajahan', 'pengaruh']
for name in geojson_names:
    if name not in keys and any(k in name.lower() for k in keywords):
        print(name)

print('=== ALL OTHER GeoJSON features NOT IN countryData ===')
for name in geojson_names:
    if name not in keys and not any(k in name.lower() for k in keywords):
        print(name)
