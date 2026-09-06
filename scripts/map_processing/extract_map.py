import json
from shapely.geometry import shape, mapping, Polygon, MultiPolygon
from shapely.ops import unary_union

with open('data/world_1930.geojson', 'r', encoding='utf-8') as f:
    data_1930 = json.load(f)

with open('data/world_1938.geojson', 'r', encoding='utf-8') as f:
    data_1938 = json.load(f)

with open('data/world_modern.geojson', 'r', encoding='utf-8') as f:
    data_modern = json.load(f)

def get_feature(data, names):
    for f in data.get('features', []):
        name = f.get('properties', {}).get('NAME') or f.get('properties', {}).get('name')
        if name in names:
            return f
    return None

def get_features_list(data, names):
    result = []
    for f in data.get('features', []):
        name = f.get('properties', {}).get('NAME') or f.get('properties', {}).get('name')
        if name in names:
            result.append(f)
    return result

def extract_polygons(geom):
    if isinstance(geom, Polygon):
        return [geom]
    elif isinstance(geom, MultiPolygon):
        return list(geom.geoms)
    elif geom.geom_type == 'GeometryCollection':
        polys = []
        for g in geom.geoms:
            if isinstance(g, Polygon):
                polys.append(g)
            elif isinstance(g, MultiPolygon):
                polys.extend(g.geoms)
        return polys
    return []

def clean_geometry(geom):
    polys = extract_polygons(geom)
    if polys:
        return MultiPolygon(polys)
    return MultiPolygon()

ger_1930_f = get_feature(data_1930, ['Germany'])
east_prussia_1930_f = get_feature(data_1930, ['East Prussia'])
aus_1930_f = get_feature(data_1930, ['Austria'])
cz_1930_f = get_feature(data_1930, ['Czechoslovakia'])
poland_1930_f = get_feature(data_1930, ['Poland'])
mongolia_1930_f = get_feature(data_1930, ['Mongolia'])
yugoslavia_1930_f = get_feature(data_1930, ['Yugoslavia'])

# Fetch Turkey from modern dataset because 1930/1938 datasets use Treaty of Sevres borders
turkey_modern_f = get_feature(data_modern, ['Turkey'])
turkey_modern_geom = clean_geometry(shape(turkey_modern_f['geometry']))

ussr_parts = [
    get_feature(data_1930, ['White Russia']), 
    get_feature(data_1930, ['Far Eastern SSR']),
    get_feature(data_1930, ['Georgia']),
    get_feature(data_1930, ['Armenia']),
    get_feature(data_1930, ['Azerbaijan'])
]

ussr_geoms = []
for p in ussr_parts:
    if p:
        ussr_geoms.append(shape(p['geometry']))
ussr_1930_geom_raw = unary_union(ussr_geoms)

# Subtract modern Turkey from USSR to fix the overlaps
ussr_final_geom = clean_geometry(ussr_1930_geom_raw.buffer(0).difference(turkey_modern_geom.buffer(0)))

ger_1938_f = get_feature(data_1938, ['Germany'])

italy_1938_f = get_feature(data_1938, ['Italy'])
italy_protectorates_f = [get_feature(data_1938, ['Albania'])]
italy_colonies_f = [
    get_feature(data_1938, ['Libya']),
    get_feature(data_1938, ['Eritrea (Italy)']),
    get_feature(data_1938, ['Italian Somaliland'])
]
ethiopia_1938_f = get_feature(data_1938, ['Ethiopia (Italy)'])

france_core_f = get_features_list(data_1938, ['France', 'Algeria (France)'])
france_protectorates_f = get_features_list(data_1938, ['Morocco (France)', 'Tunisia', 'Syria (France)', 'Cambodia', 'Laos', 'French Indo-China', 'Cochin China'])
france_colonies_f = get_features_list(data_1938, [
    'French West Africa', 'French Equatorial Africa', 'Madagascar (France)', 
    'French Somaliland', 'French Guiana', 'Guadeloupe', 'Martinique', 
    'French Cameroons', 'Togo', 'New Caledonia', 
    'Saint Barthelemy', 'Saint Martin', 'Wallis and Futuna Islands', 'New Hebrides'
])

ger_main_1930_geom = shape(ger_1930_f['geometry'])
east_prussia_1930_geom = shape(east_prussia_1930_f['geometry'])
ger_1930_geom = unary_union([ger_main_1930_geom, east_prussia_1930_geom])
ger_1930_geom_clean = clean_geometry(ger_1930_geom)

aus_1930_geom = clean_geometry(shape(aus_1930_f['geometry']))
cz_1930_geom = shape(cz_1930_f['geometry'])
ger_1938_geom = shape(ger_1938_f['geometry'])
poland_1930_geom = clean_geometry(shape(poland_1930_f['geometry']))
mongolia_1930_geom = clean_geometry(shape(mongolia_1930_f['geometry']))
if yugoslavia_1930_f:
    yugoslavia_1930_geom = clean_geometry(shape(yugoslavia_1930_f['geometry']))
else:
    yugoslavia_1930_geom = MultiPolygon()

def merge_features_geom(features_list):
    geoms = [shape(f['geometry']) for f in features_list if f]
    return clean_geometry(unary_union(geoms)) if geoms else MultiPolygon()

italy_1938_geom = clean_geometry(shape(italy_1938_f['geometry'])) if italy_1938_f else MultiPolygon()
italy_protectorates_geom = merge_features_geom(italy_protectorates_f)
italy_colonies_geom = merge_features_geom(italy_colonies_f)

ethiopia_1938_geom = clean_geometry(shape(ethiopia_1938_f['geometry'])) if ethiopia_1938_f else MultiPolygon()

greece_1938_f = get_feature(data_1938, ['Greece'])
greece_1938_geom_raw = clean_geometry(shape(greece_1938_f['geometry'])) if greece_1938_f else MultiPolygon()
greece_1938_geom = clean_geometry(greece_1938_geom_raw.buffer(0).difference(turkey_modern_geom.buffer(0)))

france_core_geom = merge_features_geom(france_core_f)
france_protectorates_geom_raw = merge_features_geom(france_protectorates_f)
# Subtract modern Turkey from French Protectorates to fix Syria overlap
france_protectorates_geom = clean_geometry(france_protectorates_geom_raw.buffer(0).difference(turkey_modern_geom.buffer(0)))
france_colonies_geom = merge_features_geom(france_colonies_f)


sudetenland_geom = cz_1930_geom.buffer(0).intersection(ger_1938_geom.buffer(0))
sudetenland_geom_clean = clean_geometry(sudetenland_geom)

cz_rump_geom = cz_1930_geom.buffer(0).difference(ger_1938_geom.buffer(0))
cz_rump_geom_clean = clean_geometry(cz_rump_geom)

features = []

features.append({
    "type": "Feature",
    "properties": {
        "name": "Jerman Nazi (Pra-1938)",
        "alliance": "axis",
        "color": "#4a4a4a",
        "fillOpacity": 0.8
    },
    "geometry": mapping(ger_1930_geom_clean)
})

features.append({
    "type": "Feature",
    "properties": {
        "name": "Austria (Dianeksasi / Protektorat)",
        "alliance": "axis",
        "color": "#4a4a4a",
        "fillOpacity": 0.6
    },
    "geometry": mapping(aus_1930_geom)
})

features.append({
    "type": "Feature",
    "properties": {
        "name": "Sudetenland (Dianeksasi / Protektorat)",
        "alliance": "axis",
        "color": "#4a4a4a",
        "fillOpacity": 0.6
    },
    "geometry": mapping(sudetenland_geom_clean)
})

features.append({
    "type": "Feature",
    "properties": {
        "name": "Czechoslovakia",
        "alliance": "allies",
        "color": "#20B2AA",
        "fillOpacity": 0.8
    },
    "geometry": mapping(cz_rump_geom_clean)
})

features.append({
    "type": "Feature",
    "properties": {
        "name": "Polandia",
        "alliance": "allies",
        "color": "#c7546a",
        "fillOpacity": 0.8
    },
    "geometry": mapping(poland_1930_geom)
})

features.append({
    "type": "Feature",
    "properties": {
        "name": "Uni Soviet",
        "alliance": "comintern",
        "color": "#CC0000",
        "fillOpacity": 0.8
    },
    "geometry": mapping(ussr_final_geom)
})

features.append({
    "type": "Feature",
    "properties": {
        "name": "Mongolia (Negara Satelit USSR)",
        "alliance": "comintern",
        "color": "#990000",
        "fillOpacity": 0.8
    },
    "geometry": mapping(mongolia_1930_geom)
})

features.append({
    "type": "Feature",
    "properties": {
        "name": "Republik Turki",
        "alliance": "neutral",
        "color": "#B86B40",
        "fillOpacity": 0.8
    },
    "geometry": mapping(turkey_modern_geom)
})

if not yugoslavia_1930_geom.is_empty:
    features.append({
        "type": "Feature",
        "properties": {
            "name": "Kerajaan Yugoslavia",
            "alliance": "neutral",
            "color": "#a8a287",
            "fillOpacity": 0.8
        },
        "geometry": mapping(yugoslavia_1930_geom)
    })

if not italy_1938_geom.is_empty:
    features.append({
        "type": "Feature",
        "properties": {
            "name": "Kerajaan Italia (Inti)",
            "alliance": "axis",
            "color": "#2e7d32", # Green
            "fillOpacity": 0.8
        },
        "geometry": mapping(italy_1938_geom)
    })

if not italy_protectorates_geom.is_empty:
    features.append({
        "type": "Feature",
        "properties": {
            "name": "Protektorat Kerajaan Italia",
            "alliance": "axis",
            "color": "#2e7d32", # Green
            "fillOpacity": 0.6
        },
        "geometry": mapping(italy_protectorates_geom)
    })

if not italy_colonies_geom.is_empty:
    features.append({
        "type": "Feature",
        "properties": {
            "name": "Wilayah Koloni Italia",
            "alliance": "axis",
            "color": "#2e7d32", # Green but faded opacity
            "fillOpacity": 0.4
        },
        "geometry": mapping(italy_colonies_geom)
    })

if not ethiopia_1938_geom.is_empty:
    features.append({
        "type": "Feature",
        "properties": {
            "name": "Kekaisaran Ethiopia (Diinvasi Italia)",
            "alliance": "allies",
            "color": "#cd853f", # Different color to indicate independent/resistance
            "fillOpacity": 0.8
        },
        "geometry": mapping(ethiopia_1938_geom)
    })

if not france_core_geom.is_empty:
    features.append({
        "type": "Feature",
        "properties": {
            "name": "Prancis Metropolitan & Aljazair",
            "alliance": "allies",
            "color": "#0055A4",
            "fillOpacity": 0.8
        },
        "geometry": mapping(france_core_geom)
    })

if not france_protectorates_geom.is_empty:
    features.append({
        "type": "Feature",
        "properties": {
            "name": "Protektorat & Mandat Prancis",
            "alliance": "allies",
            "color": "#0055A4",
            "fillOpacity": 0.6
        },
        "geometry": mapping(france_protectorates_geom)
    })

if not france_colonies_geom.is_empty:
    features.append({
        "type": "Feature",
        "properties": {
            "name": "Wilayah Koloni Prancis",
            "alliance": "allies",
            "color": "#0055A4",
            "fillOpacity": 0.4
        },
        "geometry": mapping(france_colonies_geom)
    })

if not greece_1938_geom.is_empty:
    features.append({
        "type": "Feature",
        "properties": {
            "name": "Kerajaan Yunani",
            "alliance": "allies",
            "color": "#5ab4e5", # Lighter Blue to distinguish from France
            "fillOpacity": 0.8
        },
        "geometry": mapping(greece_1938_geom)
    })


out_data = {
    "type": "FeatureCollection",
    "features": features
}

with open('../../src/data/germany_1939.json', 'w', encoding='utf-8') as f:
    json.dump(out_data, f)
    
print("Successfully generated v12 map with modern Turkey and fixed USSR borders!")
