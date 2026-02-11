import os
import json

# Configuration
SPAWN_DATA_PATH = 'data/cobblemon/spawn_pool_world/'
OUTPUT_FILE = 'wiki/spawns.md'

def format_name(name):
    """ Cleans 'mythsandlegends-registeel-2' into 'Registeel' """
    clean = name.split('-')[1] if '-' in name else name
    return clean.replace('_', ' ').title()

def get_item_and_conditions(spawn_obj):
    """ Extracts item, time, and season from nested condition blocks """
    cond = spawn_obj.get('condition', {})
    
    # Defaults
    item = "None"
    time = "Any"
    season = "Any"
    
    # Helper to scan a dictionary for keys
    def scan_dict(d):
        nonlocal item, time, season
        # M&L Item key
        found_item = d.get('custom_absent_required_item') or d.get('item')
        if found_item: item = found_item.split(':')[-1].replace('_', ' ').title()
        
        # Time / Season
        if 'timeRange' in d: time = d['timeRange'].capitalize()
        if 'season' in d: season = d['season'].capitalize()

    # Scan top level
    scan_dict(cond)
    
    # Scan 'and' blocks (standard for complex spawns)
    if 'and' in cond:
        for sub in cond['and']:
            scan_dict(sub)
            
    return item, time, season

def generate_table():
    entries = []
    if not os.path.exists(SPAWN_DATA_PATH): return

    for filename in os.listdir(SPAWN_DATA_PATH):
        if not filename.endswith('.json'): continue
        with open(os.path.join(SPAWN_DATA_PATH, filename), 'r') as f:
            try:
                data = json.load(f)
                for s in data.get('spawns', []):
                    # Basic Info
                    raw_id = s.get('id', s.get('pokemon', 'Unknown'))
                    name = format_name(raw_id)
                    weight = s.get('weight', 0)
                    
                    # Conditions
                    item, time, season = get_item_and_conditions(s)
                    
                    # Biomes
                    cond = s.get('condition', {})
                    biomes_list = cond.get('biomes', ["Global"])
                    biomes = ", ".join(biomes_list) if isinstance(biomes_list, list) else str(biomes_list)
                    biomes = biomes.replace('minecraft:', '').replace('cobblemon:', '')

                    is_legend = weight <= 1 or "myth" in filename.lower()
                    
                    entries.append({
                        "name": name, "biomes": biomes, "weight": weight,
                        "item": item, "time": time, "season": season, "legend": is_legend
                    })
            except: continue

    # Sort alphabetically by name
    entries.sort(key=lambda x: x['name'])

    with open(OUTPUT_FILE, 'w') as f:
        f.write("# 🐾 World Spawn List\n\n")
        
        f.write("## 💎 Legendary & Mythic Spawns\n")
        f.write("| Pokémon | Key Item | Biomes | Time | Season | Weight |\n")
        f.write("| :--- | :--- | :--- | :--- | :--- | :--- |\n")
        for e in [x for x in entries if x['legend']]:
            f.write(f"| **{e['name']}** | `{e['item']}` | {e['biomes']} | {e['time']} | {e['season']} | {e['weight']} |\n")
            
        f.write("\n---\n\n## 🌲 Standard Spawns\n")
        f.write("| Pokémon | Biomes | Time | Season | Rarity |\n")
        f.write("| :--- | :--- | :--- | :--- | :--- |\n")
        for e in [x for x in entries if not x['legend']]:
            f.write(f"| {e['name']} | {e['biomes']} | {e['time']} | {e['season']} | {e['weight']} |\n")

if __name__ == "__main__":
    generate_table()
