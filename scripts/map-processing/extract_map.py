import json
from shapely.geometry import shape, mapping, Polygon, MultiPolygon, box
from shapely.ops import unary_union

with open('data/world_1930.geojson', 'r', encoding='utf-8') as f:
    data_1930 = json.load(f)

with open('data/world_1938.geojson', 'r', encoding='utf-8') as f:
    data_1938 = json.load(f)

with open('data/world_modern.geojson', 'r', encoding='utf-8') as f:
    data_modern = json.load(f)

with open('data/china_provinces.geojson', 'r', encoding='utf-8') as f:
    data_china_prov = json.load(f)

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
russia_modern_f = get_feature(data_modern, ['Russia', 'Russian Federation'])
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
# Add North Sakhalin which is missing in 1930 data
# Sakhalin was divided at the 50th parallel. We use modern Russia and a bounding box above 50.0 latitude
russia_modern_geom = clean_geometry(shape(russia_modern_f['geometry'])) if russia_modern_f else MultiPolygon()
n_sakhalin_box = box(141.0, 50.0, 145.0, 55.0)
north_sakhalin_geom = russia_modern_geom.intersection(n_sakhalin_box)

ussr_final_geom = clean_geometry(ussr_1930_geom_raw.buffer(0).difference(turkey_modern_geom.buffer(0)).union(north_sakhalin_geom.buffer(0)))

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
    'French West Africa', 'French Equatorial Africa', 'Congo (France)', 'Madagascar (France)', 
    'French Somaliland', 'French Guiana', 'Guadeloupe', 'Martinique', 
    'French Cameroons', 'Togo', 'New Caledonia', 
    'Saint Barthelemy', 'Saint Martin', 'Wallis and Futuna Islands', 'New Hebrides'
])

uk_core_f = get_features_list(data_1938, ['United Kingdom'])
uk_dominions_f = get_features_list(data_1938, [
    'Canada', 'Australia', 'New Zealand', 'Union of South Africa', 
    'Dominion of Newfoundland', 'Walbis Bay'
])
uk_protectorates_f = get_features_list(data_1938, [
    'Oman (British Raj)', 'Egypt', 
    'Mandatory Palestine (GB)', 'Jordan', 'Mesopotamia (GB)', 
    'Yemen (UK)', 'Sudan', 'Kuwait', 'Qatar', 'Trucial Oman', 'Muscat and Oman'
])
uk_colonies_f = get_features_list(data_1938, [
    'Anguilla', 'Antigua and Barbuda', 'Bahamas', 'Barbados', 'Belize',
    'British Somaliland', 'Ceylon', 'Dominica', 'Fiji',
    'Gambia, The', 'Gilbert and Elice Islands', 'Gold Coast', 'Grenada',
    'Guyana', 'Hong Kong', 'Jamaica', 'Kenya', 'Lesotho', 'Malawi',
    'Montserrat', 'Nigeria', 'Northern Rhodesia', 
    'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Vincent and the Grenadines',
    'Sierra Leone', 'Southern Rhodesia', 'Swaziland', 'Tanzania, United Republic of',
    'Trinidad', 'Turks and Caicos Islands', 'Uganda', 'Botswana', 'Niue', 
    'Samoa', 'Tonga'
])

japan_1938_f = get_feature(data_1938, ['Empire of Japan'])
manchuria_1930_f = get_feature(data_1930, ['Manchuria'])
saipan_1938_f = get_feature(data_1938, ['Saipan'])

us_core_f = get_features_list(data_1938, ['United States'])
us_commonwealth_f = get_features_list(data_modern, ['Philippines'])
us_territories_f = get_features_list(data_1938, ['Puerto Rico', 'Guam', 'American Samoa', 'United States Virgin Islands'])

nl_core_f = get_features_list(data_1938, ['Netherlands'])
nl_colonies_f = get_features_list(data_1938, ['Suriname', 'Netherlands Antilles'])

bel_core_f = get_features_list(data_1938, ['Belgium'])
bel_colonies_f = get_features_list(data_1938, ['Belgian Congo', 'Burundi', 'Rwanda (Belgium)'])

spain_core_f = get_features_list(data_1938, ['Spain'])
spain_colonies_f = get_features_list(data_1938, ['Spanish Sahara', 'Rio De Oro', 'Equatorial Guinea'])

portugal_core_f = get_features_list(data_1938, ['Portugal'])
portugal_colonies_f = get_features_list(data_1938, ['Angola (Portugal)', 'Mozambique (Portugal)', 'Guinea-Bissau'])

italy_core_f = get_features_list(data_1938, ['Italy'])
italy_protectorates_f = get_features_list(data_1938, ['Albania'])
italy_colonies_f = get_features_list(data_1938, ['Libya', 'Italian Somaliland', 'Eritrea (Italy)', 'Ethiopia (Italy)'])

estonia_f = get_feature(data_1930, ['Estonia'])
latvia_f = get_feature(data_1930, ['Latvia'])
lithuania_f = get_feature(data_1930, ['Lithuania'])

switzerland_f = get_feature(data_modern, ['Switzerland'])
lux_f = get_feature(data_modern, ['Luxembourg'])
malta_f = get_feature(data_modern, ['Malta'])
ireland_f = get_feature(data_modern, ['Ireland'])
hungary_f = get_feature(data_1930, ['Hungary'])
romania_f = get_feature(data_1930, ['Romania'])
bulgaria_f = get_feature(data_1930, ['Bulgaria'])

norway_f = get_feature(data_modern, ['Norway'])
sweden_f = get_feature(data_modern, ['Sweden'])
finland_f = get_feature(data_1930, ['Finland'])

denmark_core_f = get_features_list(data_modern, ['Denmark'])
iceland_f = get_features_list(data_modern, ['Iceland'])
greenland_f = get_features_list(data_modern, ['Greenland', 'Faroe Islands'])

china_f = get_feature(data_1938, ['Chinese warlords'])
xinjiang_f = get_feature(data_1938, ['Xinjiang'])
tibet_f = get_feature(data_1938, ['Tibet'])
hongkong_f = get_feature(data_1938, ['Hong Kong'])
siam_f = get_feature(data_modern, ['Thailand'])
nepal_f = get_feature(data_modern, ['Nepal'])
bhutan_f = get_feature(data_modern, ['Bhutan'])

saudi_f = get_feature(data_1938, ['Saudi Arabia'])
yemen_f = get_feature(data_1938, ['Yemen'])
iran_f = get_feature(data_1938, ['Iran'])
afghan_f = get_feature(data_1938, ['Afghanistan'])

liberia_f = get_feature(data_1938, ['Liberia'])

indonesia_modern_f = get_features_list(data_modern, ['Indonesia'])
malaysia_modern_f = get_features_list(data_modern, ['Malaysia', 'Brunei', 'Singapore'])
east_timor_modern_f = get_features_list(data_modern, ['East Timor'])
british_raj_modern_f = get_features_list(data_modern, ['India', 'Pakistan', 'Bangladesh', 'Myanmar'])

ger_main_1930_geom = shape(ger_1930_f['geometry'])
east_prussia_1930_geom = shape(east_prussia_1930_f['geometry'])
ger_1930_geom = unary_union([ger_main_1930_geom, east_prussia_1930_geom])
ger_1930_geom_clean = clean_geometry(ger_1930_geom)

aus_1930_geom = clean_geometry(shape(aus_1930_f['geometry']))
cz_1930_geom = shape(cz_1930_f['geometry'])
ger_1938_geom = shape(ger_1938_f['geometry'])
poland_1930_geom = clean_geometry(shape(poland_1930_f['geometry']))

# Saar was acquired by Germany in 1935. It is in 1938 Germany but not 1930.
saar_geom = clean_geometry(ger_1938_geom.buffer(0).difference(ger_1930_geom_clean.buffer(0)).difference(aus_1930_geom.buffer(0)).difference(cz_1930_geom.buffer(0)).difference(poland_1930_geom.buffer(0)))

ger_final_geom = clean_geometry(ger_1930_geom_clean.buffer(0).union(east_prussia_1930_geom.buffer(0)).union(saar_geom.buffer(0)))
if yugoslavia_1930_f:
    yugoslavia_1930_geom = clean_geometry(shape(yugoslavia_1930_f['geometry']))
else:
    yugoslavia_1930_geom = MultiPolygon()

mongolia_1930_geom = clean_geometry(shape(mongolia_1930_f['geometry']))

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

uk_core_geom = merge_features_geom(uk_core_f)
uk_dominions_geom = merge_features_geom(uk_dominions_f)
british_raj_modern_geom = merge_features_geom(british_raj_modern_f)
uk_protectorates_geom = clean_geometry(merge_features_geom(uk_protectorates_f).buffer(0).union(british_raj_modern_geom.buffer(0)))

malta_geom = clean_geometry(shape(malta_f['geometry'])) if malta_f else MultiPolygon()
uk_colonies_geom = clean_geometry(merge_features_geom(uk_colonies_f).buffer(0).union(merge_features_geom(malaysia_modern_f).buffer(0)).union(malta_geom.buffer(0)))

japan_1938_geom_raw = clean_geometry(shape(japan_1938_f['geometry'])) if japan_1938_f else MultiPolygon()
manchuria_1930_geom = clean_geometry(shape(manchuria_1930_f['geometry'])) if manchuria_1930_f else MultiPolygon()
saipan_1938_geom = clean_geometry(shape(saipan_1938_f['geometry'])) if saipan_1938_f else MultiPolygon()
# Subtract Manchuria from Japan core
japan_core_geom = clean_geometry(japan_1938_geom_raw.buffer(0).difference(manchuria_1930_geom.buffer(0)))

us_core_geom = merge_features_geom(us_core_f)
us_commonwealth_geom = merge_features_geom(us_commonwealth_f)
us_territories_geom = merge_features_geom(us_territories_f)

nl_core_geom = merge_features_geom(nl_core_f)
nl_colonies_geom = clean_geometry(merge_features_geom(nl_colonies_f).buffer(0).union(merge_features_geom(indonesia_modern_f).buffer(0)))

bel_core_geom = merge_features_geom(bel_core_f)
bel_colonies_geom = merge_features_geom(bel_colonies_f)

spain_core_geom = merge_features_geom(spain_core_f)
spain_colonies_geom = merge_features_geom(spain_colonies_f)

portugal_core_geom = merge_features_geom(portugal_core_f)
portugal_colonies_geom = clean_geometry(merge_features_geom(portugal_colonies_f).buffer(0).union(merge_features_geom(east_timor_modern_f).buffer(0)))

italy_core_geom = merge_features_geom(italy_core_f)
italy_protectorates_geom = merge_features_geom(italy_protectorates_f)
italy_colonies_geom = merge_features_geom(italy_colonies_f)

estonia_geom = clean_geometry(shape(estonia_f['geometry'])) if estonia_f else MultiPolygon()
latvia_geom = clean_geometry(shape(latvia_f['geometry'])) if latvia_f else MultiPolygon()
lithuania_geom = clean_geometry(shape(lithuania_f['geometry'])) if lithuania_f else MultiPolygon()

swiss_raw_geom = clean_geometry(shape(switzerland_f['geometry'])) if switzerland_f else MultiPolygon()
swiss_geom = clean_geometry(swiss_raw_geom.buffer(0).difference(france_core_geom.buffer(0)).difference(ger_1930_geom_clean.buffer(0)).difference(italy_core_geom.buffer(0)))

lux_raw_geom = clean_geometry(shape(lux_f['geometry'])) if lux_f else MultiPolygon()
lux_geom = clean_geometry(lux_raw_geom.buffer(0).difference(france_core_geom.buffer(0)).difference(bel_core_geom.buffer(0)).difference(ger_1930_geom_clean.buffer(0)))

ireland_geom = clean_geometry(shape(ireland_f['geometry'])) if ireland_f else MultiPolygon()
liberia_geom = clean_geometry(shape(liberia_f['geometry'])) if liberia_f else MultiPolygon()
hungary_geom = clean_geometry(shape(hungary_f['geometry'])) if hungary_f else MultiPolygon()
romania_geom = clean_geometry(shape(romania_f['geometry'])) if romania_f else MultiPolygon()
bulgaria_geom = clean_geometry(shape(bulgaria_f['geometry'])) if bulgaria_f else MultiPolygon()

norway_raw_geom = clean_geometry(shape(norway_f['geometry'])) if norway_f else MultiPolygon()
sweden_raw_geom = clean_geometry(shape(sweden_f['geometry'])) if sweden_f else MultiPolygon()
finland_geom = clean_geometry(shape(finland_f['geometry'])) if finland_f else MultiPolygon()

norway_geom = clean_geometry(norway_raw_geom.buffer(0).difference(finland_geom.buffer(0)))
sweden_geom = clean_geometry(sweden_raw_geom.buffer(0).difference(finland_geom.buffer(0)))

denmark_core_geom = merge_features_geom(denmark_core_f)
iceland_geom = merge_features_geom(iceland_f)
greenland_geom = merge_features_geom(greenland_f)

china_geom = clean_geometry(shape(china_f['geometry'])) if china_f else MultiPolygon()
xinjiang_geom = clean_geometry(shape(xinjiang_f['geometry'])) if xinjiang_f else MultiPolygon()
hongkong_geom = clean_geometry(shape(hongkong_f['geometry'])) if hongkong_f else MultiPolygon()
siam_geom = clean_geometry(shape(siam_f['geometry'])) if siam_f else MultiPolygon()
nepal_geom = clean_geometry(shape(nepal_f['geometry'])) if nepal_f else MultiPolygon()
bhutan_geom = clean_geometry(shape(bhutan_f['geometry'])) if bhutan_f else MultiPolygon()

saudi_geom = clean_geometry(shape(saudi_f['geometry'])) if saudi_f else MultiPolygon()
yemen_geom = clean_geometry(shape(yemen_f['geometry'])) if yemen_f else MultiPolygon()
iran_raw_geom = clean_geometry(shape(iran_f['geometry'])) if iran_f else MultiPolygon()
afghan_raw_geom = clean_geometry(shape(afghan_f['geometry'])) if afghan_f else MultiPolygon()

# Fix borders against modern and 1930 datasets to avoid overlaps
iran_geom = clean_geometry(iran_raw_geom.buffer(0).difference(turkey_modern_geom.buffer(0)).difference(british_raj_modern_geom.buffer(0)).difference(ussr_final_geom.buffer(0)))
afghan_geom = clean_geometry(afghan_raw_geom.buffer(0).difference(british_raj_modern_geom.buffer(0)).difference(ussr_final_geom.buffer(0)))

# --- Chinese Factions Processing ---
ma_provs = ['青海省', '甘肃省', '宁夏回族自治区']
shanxi_provs = ['山西省']
communist_provs = ['陕西省']
sichuan_provs = ['四川省', '重庆市']
yunnan_provs = ['云南省']
guangxi_provs = ['广西壮族自治区']
mengjiang_provs = ['内蒙古自治区']
nat_provs = ['湖南省', '湖北省', '江西省', '福建省', '浙江省', '安徽省', '江苏省', '河南省', '山东省', '河北省', '贵州省', '广东省', '海南省', '北京市', '天津市', '上海市', '辽宁省', '吉林省', '黑龙江省', '台湾省']

def get_prov_geom(prov_names):
    feats = get_features_list(data_china_prov, prov_names)
    return merge_features_geom(feats)

tibet_raw_geom = clean_geometry(get_prov_geom(['西藏自治区']))
tibet_geom = clean_geometry(tibet_raw_geom.buffer(0).difference(nepal_geom.buffer(0)).difference(bhutan_geom.buffer(0)).difference(british_raj_modern_geom.buffer(0)))

ma_geom_raw = clean_geometry(get_prov_geom(ma_provs).buffer(0).intersection(china_geom.buffer(0)))
shanxi_geom_raw = clean_geometry(get_prov_geom(shanxi_provs).buffer(0).intersection(china_geom.buffer(0)))
communist_geom_raw = clean_geometry(get_prov_geom(communist_provs).buffer(0).intersection(china_geom.buffer(0)))
sichuan_geom_raw = clean_geometry(get_prov_geom(sichuan_provs).buffer(0).intersection(china_geom.buffer(0)))
yunnan_geom_raw = clean_geometry(get_prov_geom(yunnan_provs).buffer(0).intersection(china_geom.buffer(0)))
guangxi_geom_raw = clean_geometry(get_prov_geom(guangxi_provs).buffer(0).intersection(china_geom.buffer(0)))
mengjiang_geom_raw = clean_geometry(get_prov_geom(mengjiang_provs).buffer(0).intersection(china_geom.buffer(0)))
nat_geom_raw = clean_geometry(get_prov_geom(nat_provs).buffer(0).intersection(china_geom.buffer(0)))

# Fix inner overlaps among Chinese factions by subtracting each from a progressive union
def fix_overlaps(geom_list):
    fixed = []
    union_so_far = MultiPolygon()
    for g in geom_list:
        diff_g = clean_geometry(g.buffer(0).difference(union_so_far.buffer(0)))
        fixed.append(diff_g)
        union_so_far = clean_geometry(union_so_far.buffer(0).union(diff_g.buffer(0)))
    return fixed

# Order matters for precedence. We give smaller cliques priority over Nationalist China
factions_ordered = [
    communist_geom_raw, shanxi_geom_raw, ma_geom_raw, 
    mengjiang_geom_raw, yunnan_geom_raw, guangxi_geom_raw, 
    sichuan_geom_raw, nat_geom_raw
]
fixed_factions = fix_overlaps(factions_ordered)

communist_geom, shanxi_geom, ma_geom, mengjiang_geom, yunnan_geom, guangxi_geom, sichuan_geom, nat_geom = fixed_factions
# -----------------------------------


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
        "color": "#CC0000",
        "fillOpacity": 0.6
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

if not uk_core_geom.is_empty:
    features.append({
        "type": "Feature",
        "properties": {
            "name": "Britania Raya (Inti)",
            "alliance": "allies",
            "color": "#D81B60", # British Pink/Red
            "fillOpacity": 0.8
        },
        "geometry": mapping(uk_core_geom)
    })

if not uk_dominions_geom.is_empty:
    features.append({
        "type": "Feature",
        "properties": {
            "name": "Dominion Persemakmuran Inggris",
            "alliance": "allies",
            "color": "#D81B60",
            "fillOpacity": 0.65
        },
        "geometry": mapping(uk_dominions_geom)
    })

if not uk_protectorates_geom.is_empty:
    features.append({
        "type": "Feature",
        "properties": {
            "name": "Protektorat/Mandat Inggris (Termasuk Aden/Yaman Selatan)",
            "alliance": "allies",
            "color": "#D81B60", # Same British Pink/Red as core
            "fillOpacity": 0.5
        },
        "geometry": mapping(uk_protectorates_geom)
    })

if not uk_colonies_geom.is_empty:
    features.append({
        "type": "Feature",
        "properties": {
            "name": "Koloni Mahkota Inggris",
            "alliance": "allies",
            "color": "#D81B60",
            "fillOpacity": 0.35
        },
        "geometry": mapping(uk_colonies_geom)
    })

if not hongkong_geom.is_empty:
    features.append({
        "type": "Feature",
        "properties": {
            "name": "Hong Kong (Inggris)",
            "alliance": "allies",
            "color": "#D81B60",
            "fillOpacity": 0.35
        },
        "geometry": mapping(hongkong_geom)
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

if not japan_core_geom.is_empty:
    features.append({
        "type": "Feature",
        "properties": {
            "name": "Kekaisaran Jepang (Inti & Pendudukan)",
            "alliance": "axis",
            "color": "#D84315", # Burnt Orange
            "fillOpacity": 0.8
        },
        "geometry": mapping(japan_core_geom)
    })

if not manchuria_1930_geom.is_empty:
    features.append({
        "type": "Feature",
        "properties": {
            "name": "Negara Boneka Manchukuo",
            "alliance": "axis",
            "color": "#D84315",
            "fillOpacity": 0.6
        },
        "geometry": mapping(manchuria_1930_geom)
    })

if not saipan_1938_geom.is_empty:
    features.append({
        "type": "Feature",
        "properties": {
            "name": "Mandat Pasifik Selatan (Jepang)",
            "alliance": "axis",
            "color": "#D84315",
            "fillOpacity": 0.4
        },
        "geometry": mapping(saipan_1938_geom)
    })

if not us_core_geom.is_empty:
    features.append({
        "type": "Feature",
        "properties": {
            "name": "Amerika Serikat (Inti)",
            "alliance": "allies",
            "color": "#00838F", # Teal / Dark Cyan to distinguish from France
            "fillOpacity": 0.8
        },
        "geometry": mapping(us_core_geom)
    })

if not us_commonwealth_geom.is_empty:
    features.append({
        "type": "Feature",
        "properties": {
            "name": "Persemakmuran Filipina (AS)",
            "alliance": "allies",
            "color": "#00838F",
            "fillOpacity": 0.6
        },
        "geometry": mapping(us_commonwealth_geom)
    })

if not us_territories_geom.is_empty:
    features.append({
        "type": "Feature",
        "properties": {
            "name": "Teritori Amerika Serikat",
            "alliance": "allies",
            "color": "#00838F",
            "fillOpacity": 0.4
        },
        "geometry": mapping(us_territories_geom)
    })

if not nl_core_geom.is_empty:
    features.append({
        "type": "Feature",
        "properties": {
            "name": "Belanda (Inti)",
            "alliance": "allies",
            "color": "#D35400", # Orange
            "fillOpacity": 0.8
        },
        "geometry": mapping(nl_core_geom)
    })

if not nl_colonies_geom.is_empty:
    features.append({
        "type": "Feature",
        "properties": {
            "name": "Koloni Kerajaan Belanda",
            "alliance": "allies",
            "color": "#D35400",
            "fillOpacity": 0.4
        },
        "geometry": mapping(nl_colonies_geom)
    })

if not bel_core_geom.is_empty:
    features.append({
        "type": "Feature",
        "properties": {
            "name": "Belgia (Inti)",
            "alliance": "allies",
            "color": "#D4AC0D", # Golden Yellow
            "fillOpacity": 0.8
        },
        "geometry": mapping(bel_core_geom)
    })

if not bel_colonies_geom.is_empty:
    features.append({
        "type": "Feature",
        "properties": {
            "name": "Koloni & Mandat Belgia",
            "alliance": "allies",
            "color": "#D4AC0D",
            "fillOpacity": 0.4
        },
        "geometry": mapping(bel_colonies_geom)
    })

if not spain_core_geom.is_empty:
    features.append({
        "type": "Feature",
        "properties": {
            "name": "Spanyol (Inti)",
            "alliance": "neutral",
            "color": "#F1C40F", # Sunflower Yellow
            "fillOpacity": 0.8
        },
        "geometry": mapping(spain_core_geom)
    })

if not spain_colonies_geom.is_empty:
    features.append({
        "type": "Feature",
        "properties": {
            "name": "Koloni Spanyol",
            "alliance": "neutral",
            "color": "#F1C40F",
            "fillOpacity": 0.4
        },
        "geometry": mapping(spain_colonies_geom)
    })

if not portugal_core_geom.is_empty:
    features.append({
        "type": "Feature",
        "properties": {
            "name": "Portugal (Inti)",
            "alliance": "neutral",
            "color": "#27AE60", # Emerald Green
            "fillOpacity": 0.8
        },
        "geometry": mapping(portugal_core_geom)
    })

if not portugal_colonies_geom.is_empty:
    features.append({
        "type": "Feature",
        "properties": {
            "name": "Koloni Portugal",
            "alliance": "neutral",
            "color": "#27AE60", # Same Emerald Green as core
            "fillOpacity": 0.4
        },
        "geometry": mapping(portugal_colonies_geom)
    })

if not italy_core_geom.is_empty:
    features.append({
        "type": "Feature",
        "properties": {
            "name": "Kerajaan Italia (Inti)",
            "alliance": "axis",
            "color": "#2e7d32", # Dark Forest Green
            "fillOpacity": 0.8
        },
        "geometry": mapping(italy_core_geom)
    })

if not italy_protectorates_geom.is_empty:
    features.append({
        "type": "Feature",
        "properties": {
            "name": "Protektorat Italia (Albania)",
            "alliance": "axis",
            "color": "#2e7d32", # Dark Forest Green
            "fillOpacity": 0.6
        },
        "geometry": mapping(italy_protectorates_geom)
    })

if not italy_colonies_geom.is_empty:
    features.append({
        "type": "Feature",
        "properties": {
            "name": "Wilayah Koloni Italia (Libya & Afrika Timur)",
            "alliance": "axis",
            "color": "#2e7d32", # Dark Forest Green
            "fillOpacity": 0.4
        },
        "geometry": mapping(italy_colonies_geom)
    })

if not estonia_geom.is_empty:
    features.append({
        "type": "Feature",
        "properties": {
            "name": "Estonia",
            "alliance": "neutral",
            "color": "#5DADE2", # Soft Blue
            "fillOpacity": 0.8
        },
        "geometry": mapping(estonia_geom)
    })

if not latvia_geom.is_empty:
    features.append({
        "type": "Feature",
        "properties": {
            "name": "Latvia",
            "alliance": "neutral",
            "color": "#A93226", # Muted Crimson
            "fillOpacity": 0.8
        },
        "geometry": mapping(latvia_geom)
    })

if not lithuania_geom.is_empty:
    features.append({
        "type": "Feature",
        "properties": {
            "name": "Lituania",
            "alliance": "neutral",
            "color": "#48C9B0", # Soft Teal-Green
            "fillOpacity": 0.8
        },
        "geometry": mapping(lithuania_geom)
    })

if not denmark_core_geom.is_empty:
    features.append({
        "type": "Feature",
        "properties": {
            "name": "Denmark (Inti)",
            "alliance": "neutral",
            "color": "#C0392B", # Dark Red
            "fillOpacity": 0.8
        },
        "geometry": mapping(denmark_core_geom)
    })

if not iceland_geom.is_empty:
    features.append({
        "type": "Feature",
        "properties": {
            "name": "Kerajaan Islandia (Uni Personal)",
            "alliance": "neutral",
            "color": "#C0392B",
            "fillOpacity": 0.6
        },
        "geometry": mapping(iceland_geom)
    })

if not greenland_geom.is_empty:
    features.append({
        "type": "Feature",
        "properties": {
            "name": "Koloni Greenland & Faroe",
            "alliance": "neutral",
            "color": "#C0392B",
            "fillOpacity": 0.4
        },
        "geometry": mapping(greenland_geom)
    })

if not nat_geom.is_empty:
    features.append({
        "type": "Feature",
        "properties": {
            "name": "Republik Tiongkok (Nasionalis/KMT)",
            "alliance": "allies",
            "color": "#1A5276", # Deep Navy Blue
            "fillOpacity": 0.8
        },
        "geometry": mapping(nat_geom)
    })

if not communist_geom.is_empty:
    features.append({
        "type": "Feature",
        "properties": {
            "name": "Partai Komunis Tiongkok (PKT)",
            "alliance": "allies",
            "color": "#E74C3C", # Red
            "fillOpacity": 0.8
        },
        "geometry": mapping(communist_geom)
    })

if not ma_geom.is_empty:
    features.append({
        "type": "Feature",
        "properties": {
            "name": "Klik Ma (Xibei San Ma)",
            "alliance": "allies",
            "color": "#D4AC0D", # Golden/Brownish Yellow
            "fillOpacity": 0.8
        },
        "geometry": mapping(ma_geom)
    })

if not shanxi_geom.is_empty:
    features.append({
        "type": "Feature",
        "properties": {
            "name": "Klik Shanxi",
            "alliance": "allies",
            "color": "#5D6D7E", # Dark Grey-Blue
            "fillOpacity": 0.8
        },
        "geometry": mapping(shanxi_geom)
    })

if not sichuan_geom.is_empty:
    features.append({
        "type": "Feature",
        "properties": {
            "name": "Klik Sichuan",
            "alliance": "allies",
            "color": "#2980B9", # Dark Blue
            "fillOpacity": 0.8
        },
        "geometry": mapping(sichuan_geom)
    })

if not yunnan_geom.is_empty:
    features.append({
        "type": "Feature",
        "properties": {
            "name": "Klik Yunnan",
            "alliance": "allies",
            "color": "#34495E", # Dark Slate Blue to be completely distinct
            "fillOpacity": 0.8
        },
        "geometry": mapping(yunnan_geom)
    })

if not guangxi_geom.is_empty:
    features.append({
        "type": "Feature",
        "properties": {
            "name": "Klik Guangxi",
            "alliance": "allies",
            "color": "#16A085", # Teal
            "fillOpacity": 0.8
        },
        "geometry": mapping(guangxi_geom)
    })

if not mengjiang_geom.is_empty:
    features.append({
        "type": "Feature",
        "properties": {
            "name": "Mengjiang (Negara Boneka Jepang)",
            "alliance": "axis",
            "color": "#A3E4D7", # Pale Cyan/Mint
            "fillOpacity": 0.8
        },
        "geometry": mapping(mengjiang_geom)
    })

if not xinjiang_geom.is_empty:
    features.append({
        "type": "Feature",
        "properties": {
            "name": "Faksi Xinjiang (Pengaruh Soviet)",
            "alliance": "neutral",
            "color": "#E67E22", # Darker Orange
            "fillOpacity": 0.8
        },
        "geometry": mapping(xinjiang_geom)
    })

if not tibet_geom.is_empty:
    features.append({
        "type": "Feature",
        "properties": {
            "name": "Tibet (Independen De Facto)",
            "alliance": "neutral",
            "color": "#9B59B6", # Purple
            "fillOpacity": 0.8
        },
        "geometry": mapping(tibet_geom)
    })

if not siam_geom.is_empty:
    features.append({
        "type": "Feature",
        "properties": {
            "name": "Kerajaan Siam (Thailand)",
            "alliance": "neutral",
            "color": "#F1C40F", # Yellow
            "fillOpacity": 0.8
        },
        "geometry": mapping(siam_geom)
    })
if not nepal_geom.is_empty:
    features.append({"type": "Feature", "properties": {"name": "Nepal", "alliance": "neutral", "color": "#3498DB", "fillOpacity": 0.8}, "geometry": mapping(nepal_geom)})
if not bhutan_geom.is_empty:
    features.append({"type": "Feature", "properties": {"name": "Bhutan", "alliance": "neutral", "color": "#E67E22", "fillOpacity": 0.8}, "geometry": mapping(bhutan_geom)})

if not swiss_geom.is_empty:
    features.append({"type": "Feature", "properties": {"name": "Swiss", "alliance": "neutral", "color": "#95A5A6", "fillOpacity": 0.8}, "geometry": mapping(swiss_geom)})
if not lux_geom.is_empty:
    features.append({"type": "Feature", "properties": {"name": "Luksemburg", "alliance": "neutral", "color": "#8E44AD", "fillOpacity": 0.8}, "geometry": mapping(lux_geom)})
if not ireland_geom.is_empty:
    features.append({"type": "Feature", "properties": {"name": "Irlandia", "alliance": "neutral", "color": "#2ECC71", "fillOpacity": 0.8}, "geometry": mapping(ireland_geom)})
if not hungary_geom.is_empty:
    features.append({"type": "Feature", "properties": {"name": "Hungaria", "alliance": "neutral", "color": "#AF7AC5", "fillOpacity": 0.8}, "geometry": mapping(hungary_geom)})
if not romania_geom.is_empty:
    features.append({"type": "Feature", "properties": {"name": "Rumania", "alliance": "neutral", "color": "#F4D03F", "fillOpacity": 0.8}, "geometry": mapping(romania_geom)})
if not bulgaria_geom.is_empty:
    features.append({"type": "Feature", "properties": {"name": "Bulgaria", "alliance": "neutral", "color": "#58D68D", "fillOpacity": 0.8}, "geometry": mapping(bulgaria_geom)})

if not norway_geom.is_empty:
    features.append({"type": "Feature", "properties": {"name": "Norwegia", "alliance": "neutral", "color": "#EC7063", "fillOpacity": 0.8}, "geometry": mapping(norway_geom)})
if not sweden_geom.is_empty:
    features.append({"type": "Feature", "properties": {"name": "Swedia", "alliance": "neutral", "color": "#85C1E9", "fillOpacity": 0.8}, "geometry": mapping(sweden_geom)})
if not finland_geom.is_empty:
    features.append({"type": "Feature", "properties": {"name": "Finlandia", "alliance": "neutral", "color": "#BDC3C7", "fillOpacity": 0.8}, "geometry": mapping(finland_geom)})

if not saudi_geom.is_empty:
    features.append({"type": "Feature", "properties": {"name": "Arab Saudi", "alliance": "neutral", "color": "#1E8449", "fillOpacity": 0.8}, "geometry": mapping(saudi_geom)})
if not yemen_geom.is_empty:
    features.append({"type": "Feature", "properties": {"name": "Kerajaan Mutawakkiliyah Yaman (Yaman Utara - Independen)", "alliance": "neutral", "color": "#8E44AD", "fillOpacity": 0.8}, "geometry": mapping(yemen_geom)})
if not iran_geom.is_empty:
    features.append({"type": "Feature", "properties": {"name": "Iran", "alliance": "neutral", "color": "#F5B041", "fillOpacity": 0.8}, "geometry": mapping(iran_geom)})
if not afghan_geom.is_empty:
    features.append({"type": "Feature", "properties": {"name": "Afganistan", "alliance": "neutral", "color": "#D98880", "fillOpacity": 0.8}, "geometry": mapping(afghan_geom)})
if not liberia_geom.is_empty:
    features.append({"type": "Feature", "properties": {"name": "Liberia", "alliance": "neutral", "color": "#9B59B6", "fillOpacity": 0.8}, "geometry": mapping(liberia_geom)})


out_data = {
    "type": "FeatureCollection",
    "features": features
}

with open('../../src/data/germany_1939.json', 'w', encoding='utf-8') as f:
    json.dump(out_data, f)
    
print("Successfully generated v12 map with modern Turkey and fixed USSR borders!")
