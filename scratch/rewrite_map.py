import codecs
import re

with codecs.open('src/components/map/InteractiveMap.tsx', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Remove the entire countryData block
code = re.sub(r'const countryData: Record<string, any> = \{.*?^\};\n', '', code, flags=re.MULTILINE|re.DOTALL)

# 2. Rewrite the onEachFeature block
old_onEachFeature = re.search(r'  const onEachFeature = \(feature: any, layer: any\) => \{.*?\n      popupContent = `', code, flags=re.MULTILINE|re.DOTALL).group(0)

new_onEachFeature = '''  const onEachFeature = (feature: any, layer: any) => {
    const props = feature.properties;
    if (!props || !props.name) return;

    let popupContent = '';
    
    // Semua data kini diambil langsung dari properties GeoJSON!
    if (props.leader || props.ideology || props.alliance) {
      let badgeStyle = "background-color: #f1f5f9; color: #475569;"; // Default abu-abu (Netral)
      const lowerAlliance = (props.alliance || '').toLowerCase();
      if (lowerAlliance.includes('komintern') || lowerAlliance.includes('soviet') || lowerAlliance.includes('komunis')) {
        badgeStyle = "background-color: #fee2e2; color: #991b1b;"; // Merah (Komintern)
      } else if (lowerAlliance.includes('poros') || lowerAlliance.includes('axis')) {
        badgeStyle = "background-color: #1e293b; color: #f8fafc;"; // Hitam/Charcoal (Poros)
      } else if (lowerAlliance.includes('sekutu') || lowerAlliance.includes('allies')) {
        badgeStyle = "background-color: #dbeafe; color: #1e40af;"; // Biru (Sekutu)
      } else if (lowerAlliance.includes('jepang')) {
        badgeStyle = "background-color: #fef08a; color: #854d0e;"; // Kuning Emas (Faksi Jepang)
      }

      const flagUrl = props.flagUrl || `/flags/${props.name.toLowerCase().replace(/ /g, '_')}.jpeg`;
      const allianceLabel = props.alliance === 'neutral' ? 'Netral' : props.alliance || 'Netral';

      popupContent = `'''

code = code.replace(old_onEachFeature, new_onEachFeature)

# Fix variables inside popupContent
code = code.replace('${info.name}', '${props.name}')
code = code.replace('${info.flagUrl}', '${flagUrl}')
code = code.replace('${info.leader}', '${props.leader || "Tidak diketahui"}')
code = code.replace('${info.ideology}', '${props.ideology || "Tidak diketahui"}')
code = code.replace('${info.alliance}', '${allianceLabel}')

# Fix the if (info) check closure
code = code.replace('    if (info) {', '    if (props.leader || props.ideology || props.alliance) {')

with codecs.open('src/components/map/InteractiveMap.tsx', 'w', encoding='utf-8') as f:
    f.write(code)
