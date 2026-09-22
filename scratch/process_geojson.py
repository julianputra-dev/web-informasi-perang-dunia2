import json
import re

# Mock data mapping to inject into GeoJSON
mock_data = {
    # --- NEGARA INTI ---
    'Jerman Nazi': {'leader': 'Adolf Hitler', 'ideology': 'Fasisme / Nazisme', 'alliance': 'Blok Poros (Axis)', 'flagUrl': '/flags/jerman.jpeg'},
    'Jerman Nazi (Pra-1938)': {'name': 'Jerman Nazi', 'leader': 'Adolf Hitler', 'ideology': 'Fasisme / Nazisme', 'alliance': 'Blok Poros (Axis)', 'flagUrl': '/flags/jerman.jpeg'},
    'Kekaisaran Jepang': {'leader': 'Kaisar Hirohito', 'ideology': 'Militerisme / Nasionalisme Kuat', 'alliance': 'Faksi Kekaisaran Jepang', 'flagUrl': '/flags/jepang.jpeg'},
    'Kekaisaran Jepang (Inti & Pendudukan)': {'name': 'Kekaisaran Jepang', 'leader': 'Kaisar Hirohito', 'ideology': 'Militerisme / Nasionalisme Kuat', 'alliance': 'Faksi Kekaisaran Jepang', 'flagUrl': '/flags/jepang.jpeg'},
    'Kerajaan Italia': {'leader': 'Benito Mussolini', 'ideology': 'Fasisme', 'alliance': 'Blok Poros (Axis)', 'flagUrl': '/flags/italia.jpeg'},

    # --- WILAYAH JAJAHAN / PENGARUH ---
    'Austria (Dianeksasi / Protektorat)': {'name': 'Austria (Dianeksasi Jerman)', 'leader': 'Adolf Hitler / Arthur Seyss-Inquart', 'ideology': 'Fasisme / Nazisme', 'alliance': 'Blok Poros (Axis)', 'flagUrl': '/flags/jerman.jpeg'},
    'Sudetenland (Dianeksasi / Protektorat)': {'name': 'Sudetenland (Dianeksasi Jerman)', 'leader': 'Adolf Hitler / Konrad Henlein', 'ideology': 'Fasisme / Nazisme', 'alliance': 'Blok Poros (Axis)', 'flagUrl': '/flags/jerman.jpeg'},
    'Protektorat Kerajaan Italia': {'name': 'Protektorat Italia', 'leader': 'Benito Mussolini', 'ideology': 'Fasisme', 'alliance': 'Blok Poros (Axis)', 'flagUrl': '/flags/italia.jpeg'},
    'Negara Boneka Manchukuo': {'name': 'Manchukuo (Negara Boneka Jepang)', 'leader': 'Kaisar Puyi', 'ideology': 'Nasionalisme Manchu', 'alliance': 'Faksi Kekaisaran Jepang', 'flagUrl': '/flags/manchukuo.jpeg'},
    'Mandat Pasifik Selatan (Jepang)': {'name': 'Mandat Pasifik Selatan (Mandat Jepang)', 'leader': 'Kaisar Hirohito', 'ideology': 'Militerisme / Imperialisme', 'alliance': 'Faksi Kekaisaran Jepang', 'flagUrl': '/flags/jepang.jpeg'},
    'Protektorat Italia (Albania)': {'name': 'Albania (Dalam Pengaruh Italia)', 'leader': 'Raja Zog I', 'ideology': 'Monarki', 'alliance': 'Pengaruh Italia', 'flagUrl': '/flags/albania.jpeg'},
    'Libya (Koloni Italia)': {'leader': 'Benito Mussolini / Italo Balbo', 'ideology': 'Fasisme / Imperialisme', 'alliance': 'Blok Poros (Axis)', 'flagUrl': '/flags/italia.jpeg'},
    'Afrika Timur (Koloni Italia)': {'leader': 'Benito Mussolini', 'ideology': 'Fasisme / Imperialisme', 'alliance': 'Blok Poros (Axis)', 'flagUrl': '/flags/italia.jpeg'},
    'Kekaisaran Ethiopia (Diinvasi Italia)': {'name': 'Ethiopia (Diinvasi Italia)', 'leader': 'Benito Mussolini', 'ideology': 'Fasisme (Pendudukan)', 'alliance': 'Blok Poros (Axis)', 'flagUrl': '/flags/italia.jpeg'},
    'Mengjiang (Negara Boneka Jepang)': {'leader': 'Pangeran Demchugdongrub', 'ideology': 'Nasionalisme Mongol', 'alliance': 'Faksi Kekaisaran Jepang', 'flagUrl': '/flags/mengjiang.jpeg'},

    # --- BLOK SOVIET / KOMUNIS ---
    'Uni Soviet': {'leader': 'Joseph Stalin', 'ideology': 'Komunisme', 'alliance': 'Komintern', 'flagUrl': '/flags/soviet.jpeg'},
    'Mongolia (Negara Satelit USSR)': {'name': 'Mongolia (Satelit Uni Soviet)', 'leader': 'Khorloogiin Choibalsan', 'ideology': 'Komunisme', 'alliance': 'Komintern', 'flagUrl': '/flags/mongolia.jpeg'},
    'Faksi Xinjiang (Pengaruh Soviet)': {'name': 'Xinjiang (Pengaruh Soviet)', 'leader': 'Sheng Shicai', 'ideology': 'Militerisme / Pro-Soviet', 'alliance': 'Pengaruh Uni Soviet', 'flagUrl': '/flags/xinjiang.jpeg'},

    # --- BLOK PRANCIS & JAJAHANNYA ---
    'Prancis Metropolitan & Aljazair': {'name': 'Republik Prancis', 'leader': 'Édouard Daladier', 'ideology': 'Demokrasi', 'alliance': 'Blok Sekutu (Allies)', 'flagUrl': '/flags/prancis.jpeg'},
    'Maroko (Protektorat Prancis)': {'leader': 'Sultan Mohammed V', 'ideology': 'Monarki / Protektorat', 'alliance': 'Blok Sekutu (Allies)', 'flagUrl': '/flags/maroko.jpeg'},
    'Tunisia (Protektorat Prancis)': {'leader': 'Ahmad II ibn Ali', 'ideology': 'Monarki / Protektorat', 'alliance': 'Blok Sekutu (Allies)', 'flagUrl': '/flags/tunisia.jpeg'},
    'Mandat Suriah & Lebanon (Prancis)': {'name': 'Suriah & Lebanon (Mandat Prancis)', 'leader': 'Hashim al-Atassi', 'ideology': 'Mandat LBB', 'alliance': 'Blok Sekutu (Allies)', 'flagUrl': '/flags/suriah_lebanon.jpeg'},
    'Togo (Mandat Prancis)': {'leader': 'Administrasi Mandat Prancis', 'ideology': 'Mandat LBB', 'alliance': 'Blok Sekutu (Allies)', 'flagUrl': '/flags/prancis.jpeg'},
    'Kamerun (Mandat Prancis)': {'leader': 'Administrasi Mandat Prancis', 'ideology': 'Mandat LBB', 'alliance': 'Blok Sekutu (Allies)', 'flagUrl': '/flags/prancis.jpeg'},

    # --- SPANYOL ---
    'Republik Spanyol Kedua': {'leader': 'Juan Negrín', 'ideology': 'Republikanisme / Sosialis', 'alliance': 'Netral (Didukung Komintern)', 'flagUrl': '/flags/spanyol_republik.jpeg'},
    'Spanyol Nasionalis (Franco)': {'name': 'Spanyol Nasionalis', 'leader': 'Jenderal Francisco Franco', 'ideology': 'Fasisme / Nasionalisme', 'alliance': 'Netral (Didukung Blok Poros)', 'flagUrl': '/flags/spanyol_nasionalis.jpeg'},
    'Koloni Spanyol': {'leader': 'Jenderal Francisco Franco', 'ideology': 'Imperialisme / Fasisme', 'alliance': 'Netral', 'flagUrl': '/flags/spanyol_nasionalis.jpeg'},

    # --- BLOK INGGRIS / BRITANIA RAYA ---
    'Britania Raya': {'name': 'Kerajaan Britania Raya', 'leader': 'Neville Chamberlain', 'ideology': 'Demokrasi', 'alliance': 'Blok Sekutu (Allies)', 'flagUrl': '/flags/inggris.jpeg'},
    'Burma Britania (Koloni Inggris)': {'name': 'Burma (Koloni Inggris)', 'leader': 'Gubernur Lokal', 'ideology': 'Imperialisme', 'alliance': 'Blok Sekutu (Allies)', 'flagUrl': '/flags/burma_britania.jpeg'},
    'Dominion Kanada': {'name': 'Kanada (Dominion Inggris)', 'leader': 'Mackenzie King', 'ideology': 'Demokrasi', 'alliance': 'Blok Sekutu (Allies)', 'flagUrl': '/flags/kanada.jpeg'},
    'Dominion Afrika Selatan': {'name': 'Afrika Selatan (Dominion Inggris)', 'leader': 'J. B. M. Hertzog', 'ideology': 'Demokrasi', 'alliance': 'Blok Sekutu (Allies)', 'flagUrl': '/flags/afrika_selatan.jpeg'},
    'Dominion Australia (Inggris)': {'name': 'Australia (Dominion Inggris)', 'leader': 'Joseph Lyons', 'ideology': 'Demokrasi', 'alliance': 'Blok Sekutu (Allies)', 'flagUrl': '/flags/australia.jpeg'},
    'Dominion Selandia Baru (Inggris)': {'name': 'Selandia Baru (Dominion Inggris)', 'leader': 'Michael Joseph Savage', 'ideology': 'Demokrasi', 'alliance': 'Blok Sekutu (Allies)', 'flagUrl': '/flags/selandia_baru.jpeg'},
    'British Raj (India Britania)': {'name': 'India Britania (Kemaharajaan)', 'leader': 'Victor Hope (Viceroy)', 'ideology': 'Imperialisme', 'alliance': 'Blok Sekutu (Allies)', 'flagUrl': '/flags/india_britania.jpeg'},
    'Egypt (Protektorat Inggris)': {'name': 'Mesir (Protektorat Inggris)', 'leader': 'Raja Farouk I', 'ideology': 'Monarki / Pengaruh Asing', 'alliance': 'Blok Sekutu (Allies)', 'flagUrl': '/flags/mesir.jpeg'},
    'Mandat Nugini & Papua (Australia)': {'name': 'Nugini & Papua (Mandat Australia)', 'leader': 'Administrasi Australia', 'ideology': 'Mandat LBB', 'alliance': 'Blok Sekutu (Allies)', 'flagUrl': '/flags/australia.jpeg'},
    'Samoa Barat (Selandia Baru)': {'name': 'Samoa Barat (Mandat Selandia Baru)', 'leader': 'Administrasi Selandia Baru', 'ideology': 'Mandat LBB', 'alliance': 'Blok Sekutu (Allies)', 'flagUrl': '/flags/selandia_baru.jpeg'},
    'Nauru (Mandat Australia/Inggris)': {'name': 'Nauru (Mandat Bersama)', 'leader': 'Administrasi Australia', 'ideology': 'Mandat LBB', 'alliance': 'Blok Sekutu (Allies)', 'flagUrl': '/flags/australia.jpeg'},
    
    # --- BELANDA & BELGIA ---
    'Belanda': {'name': 'Kerajaan Belanda', 'leader': 'Ratu Wilhelmina', 'ideology': 'Demokrasi', 'alliance': 'Netral', 'flagUrl': '/flags/belanda.jpeg'},
    'Belgia': {'name': 'Kerajaan Belgia', 'leader': 'Raja Leopold III', 'ideology': 'Demokrasi', 'alliance': 'Netral', 'flagUrl': '/flags/belgia.jpeg'},
    'Kongo Belgia (Koloni Belgia)': {'leader': 'Gubernur Jenderal Pierre Ryckmans', 'ideology': 'Imperialisme', 'alliance': 'Netral', 'flagUrl': '/flags/belgia.jpeg'},

    # --- AMERIKA SERIKAT ---
    'Persemakmuran Filipina (AS)': {'name': 'Filipina (Persemakmuran AS)', 'leader': 'Manuel L. Quezon', 'ideology': 'Demokrasi', 'alliance': 'Netral', 'flagUrl': '/flags/filipina.jpeg'},
    'Teritori Amerika Serikat': {'leader': 'Franklin D. Roosevelt', 'ideology': 'Demokrasi', 'alliance': 'Netral', 'flagUrl': '/flags/amerika_serikat.jpeg'},
}

def clean_name(name):
    # Remove certain artifacts if they exist
    return name

with open('src/data/geojson/world-1939.json', 'r', encoding='utf-8') as f:
    geojson = json.load(f)

for feat in geojson.get('features', []):
    props = feat.get('properties', {})
    original_name = props.get('name', '')
    if not original_name:
        continue

    # 1. Apply Mock Data overrides if exact match
    if original_name in mock_data:
        override = mock_data[original_name]
        for k, v in override.items():
            props[k] = v
    else:
        # 2. Dynamic Rules for others not explicitly in mock_data
        
        # A. British Colonies
        if '(Koloni Inggris)' in original_name:
            props['leader'] = props.get('leader', 'Administrasi Kolonial Inggris')
            props['ideology'] = props.get('ideology', 'Imperialisme')
            props['alliance'] = props.get('alliance', 'Blok Sekutu (Allies)')
            props['flagUrl'] = '/flags/inggris.jpeg'
        elif '(Protektorat Inggris)' in original_name:
            if 'Mandatory Palestine' in original_name:
                props['name'] = 'Palestina (Mandat Inggris)'
                props['flagUrl'] = '/flags/palestina.jpeg'
            else:
                props['leader'] = props.get('leader', 'Penguasa Lokal / Administrasi Inggris')
                props['ideology'] = props.get('ideology', 'Protektorat')
                props['alliance'] = props.get('alliance', 'Blok Sekutu (Allies)')
                props['flagUrl'] = '/flags/inggris.jpeg'
        elif '(Inggris)' in original_name:
            props['leader'] = props.get('leader', 'Administrasi Kolonial Inggris')
            props['ideology'] = props.get('ideology', 'Imperialisme')
            props['alliance'] = props.get('alliance', 'Blok Sekutu (Allies)')
            props['flagUrl'] = '/flags/inggris.jpeg'
            
        # B. French Colonies
        elif '(Koloni Prancis)' in original_name or '(Prancis)' in original_name:
            props['leader'] = props.get('leader', 'Administrasi Kolonial Prancis')
            props['ideology'] = props.get('ideology', 'Imperialisme')
            props['alliance'] = props.get('alliance', 'Blok Sekutu (Allies)')
            props['flagUrl'] = '/flags/prancis.jpeg'
            
        # C. Dutch Colonies
        elif '(Koloni Belanda)' in original_name or 'Hindia Belanda' in original_name:
            props['leader'] = props.get('leader', 'Gubernur Jenderal Belanda')
            props['ideology'] = props.get('ideology', 'Imperialisme')
            props['alliance'] = props.get('alliance', 'Netral')
            props['flagUrl'] = '/flags/belanda.jpeg'
            
        # D. US Territories
        elif '(AS)' in original_name:
            props['leader'] = props.get('leader', 'Franklin D. Roosevelt')
            props['ideology'] = props.get('ideology', 'Demokrasi / Teritori AS')
            props['alliance'] = props.get('alliance', 'Netral')
            if 'Filipina' in original_name:
                props['flagUrl'] = '/flags/filipina.jpeg'
            else:
                props['flagUrl'] = '/flags/amerika_serikat.jpeg'
                
        # E. Independent states missing leader flag
        else:
            if 'flagUrl' not in props:
                clean = original_name.lower().replace(' ', '_').replace('(', '').replace(')', '')
                props['flagUrl'] = f'/flags/{clean}.jpeg'

    # Finally, ensure properties are written back
    feat['properties'] = props

with open('src/data/geojson/world-1939.json', 'w', encoding='utf-8') as f:
    json.dump(geojson, f, ensure_ascii=False, separators=(',', ':'))
