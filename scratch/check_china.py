import json

with open('src/data/geojson/world-1939.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for feat in data.get('features', []):
    props = feat.get('properties', {})
    name = props.get('name', '')
    if 'Tiongkok' in name or 'Klik' in name or 'Xinjiang' in name:
        print(f"{name}: Leader={props.get('leader')}, Ideology={props.get('ideology')}, Alliance={props.get('alliance')}")
