import json
import os
from shapely.geometry import shape, mapping

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
dest_path = os.path.join(BASE_DIR, 'src', 'data', 'geojson', 'world-1939.json')
modern_path = os.path.join(BASE_DIR, 'scripts', 'map-processing', 'data', 'world_modern.geojson')

with open(dest_path, 'r', encoding='utf-8') as f:
    dest_data = json.load(f)

with open(modern_path, 'r', encoding='utf-8') as f:
    modern_data = json.load(f)

# 1. Get Modern Lebanon
lebanon_geom = None
for f in modern_data['features']:
    if str(f.get('properties', {}).get('NAME', '')).lower() == 'lebanon':
        lebanon_geom = shape(f['geometry']).buffer(0)
        break

# 2. Collect Spanish Colonies geometries to subtract from Morocco
spanish_geoms = []
for f in dest_data['features']:
    name = f.get('properties', {}).get('name', '')
    if name in ['Sahara Spanyol (Koloni)', 'Rio De Oro (Koloni)', 'Ifni (Koloni)']:
        spanish_geoms.append(shape(f['geometry']).buffer(0))

new_features = []
for f in dest_data['features']:
    name = f.get('properties', {}).get('name', '')
    
    # Clean up ANY extra Guianas
    name_lower = name.lower()
    if 'guiana' in name_lower or 'guyana' in name_lower:
        if name != 'Guyana Prancis (Koloni)' and name != 'Guyana (Koloni Inggris)':
            # Found a rogue Guiana, skip it!
            continue
            
    # Subtract Spanish Sahara from Morocco
    if name == 'Maroko (Protektorat Prancis)':
        morocco_geom = shape(f['geometry']).buffer(0)
        for sp_geom in spanish_geoms:
            morocco_geom = morocco_geom.difference(sp_geom)
        f['geometry'] = mapping(morocco_geom)
        
    new_features.append(f)

# Add Lebanon
if lebanon_geom:
    new_features.append({
        'type': 'Feature',
        'properties': {
            'name': 'Mandat Suriah & Lebanon (Prancis)',
            'alliance': 'allies',
            'color': '#0055A4',
            'fillOpacity': 0.6
        },
        'geometry': mapping(lebanon_geom)
    })

dest_data['features'] = new_features

with open(dest_path, 'w', encoding='utf-8') as f:
    json.dump(dest_data, f, separators=(',', ':'))

print("Fixed Lebanon, Guiana dupes, and Morocco/Spain overlap.")
