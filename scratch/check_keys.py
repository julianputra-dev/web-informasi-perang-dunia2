import json
import re

with open('src/components/map/InteractiveMap.tsx', 'r', encoding='utf-8') as f:
    map_code = f.read()

country_data_block = map_code.split('const countryData: Record<string, any> = {')[1].split('};')[0]
keys = re.findall(r"^\s*'([^']+)':", country_data_block, re.MULTILINE)

with open('src/data/geojson/world-1939.json', 'r', encoding='utf-8') as f:
    geojson = json.load(f)
geojson_names = set([feat.get('properties', {}).get('name') for feat in geojson.get('features', [])])

missing_in_geojson = [k for k in keys if k not in geojson_names]
print('Keys in InteractiveMap not found in GeoJSON:')
for k in missing_in_geojson:
    print(k)
