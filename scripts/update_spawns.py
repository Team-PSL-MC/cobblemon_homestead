import os
import json
import re

# Configuration
SPAWN_DATA_PATH = 'data/cobblemon/spawn_pool_world/'
OUTPUT_FILE = 'wiki/spawns.md'

def format_name(raw_id):
    """ Cleans IDs like 'mythsandlegends-articuno-1' or 'articuno' into 'Articuno' """
    name = raw_id.split(':')[-1]
    parts = re.split(r'[-_]', name)
    clean_parts = [p.capitalize() for p in parts if not p.isdigit() and p.lower() != 'mythsandlegends']
    final_name = " ".join(clean_parts)
    return final_name if final_name else name.capitalize()

def get_conditions(spawn_obj):
    """ Extracts item, time, season, and weather from the spawn object """
    res = {"item": "None", "time": "Any", "season": "Any", "weather": "Clear"}
    
    # 1. Check for the "key_item" at the top level (The fix for Myths & Legends)
    top_item = spawn_obj.get('key_item')
    if top_item:
        res["item"] = top_item.split(':')[-1].replace('_', ' ').title()

    def scan_dict(d):
        # 2. Check for items inside condition blocks (standard/other mods)
        found_item = d.get('custom_absent_required_item') or d.get('needed_item') or d.get('item')
        if found_item and res["item"] == "None": 
            res["item"] = found_item.split(':')[-1].replace('_', ' ').title()
        
        # Time / Season / Weather
        if 'timeRange' in d: res["time"] = d['timeRange'].capitalize()
        if 'season' in d: res["season"] = d['season'].capitalize()
        if 'weather' in d: res["weather"] = d['weather'].split(':')[-1].capitalize()

    cond = spawn_obj.get('condition', {})
    scan_dict(cond)
    if isinstance(cond, dict):
        if 'and' in cond:
            for sub in cond['and']: scan_dict(sub)
        if 'or' in cond:
            for sub in cond['or']: scan_dict(sub)
            
    return res

def generate_table():
    entries = []
    if not os.path.exists(SPAWN_DATA_PATH): return

    for filename in os.listdir(SPAWN_DATA_PATH):
        if not filename.endswith('.json'): continue
        with open(os.path.join(SPAWN_DATA_PATH, filename), 'r') as f:
            try:
                data = json.load(f)
                for s in data.get('spawns', []):
                    raw_id = s.get('id', s.get('pokemon', 'Unknown'))
                    name = format_name(raw_id)
                    weight = s.get('weight', 0)
                    
                    stats = get_conditions(s)
                    
                    # Biome Formatting
                    cond = s.get('condition', {})
                    biomes_list = cond.get('biomes', ["Global"])
                    biomes = ", ".join(biomes_list) if isinstance(biomes_list, list) else str(biomes_list)
                    biomes = biomes.replace('minecraft:', '').replace('cobblemon:', '').replace('#', '')

                    is_legend = weight <= 1 or "myth" in filename.lower()
                    
                    entries.append({
                        "name": name, "biomes": biomes, "weight": weight,
                        "item": stats["item"], "time": stats["time"], 
                        "season": stats["season"], "weather": stats["weather"],
                        "legend": is_legend
                    })
            except: continue

    # Sort alphabetically
    entries.sort(key=lambda x: x['name'])

    with open(OUTPUT_FILE, 'w') as f:
        f.write("# 🐾 World Spawn List\n\n")
        f.write("> This list is automatically updated from the server's data packs.\n\n")
        
        f.write("## 💎 Legendary & Mythic Spawns\n")
        f.write("| Pokémon | Key Item | Biomes | Time | Season | Weather | Weight |\n")
        f.write("| :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n")
        for e in [x for x in entries if x['legend']]:
            f.write(f"| **{e['name']}** | `{e['item']}` | {e['biomes']} | {e['time']} | {e['season']} | {e['weather']} | {e['weight']} |\n")
            
        f.write("\n---\n\n## 🌲 Standard Spawns\n")
        f.write("| Pokémon | Biomes | Time | Season | Weather | Rarity |\n")
        f.write("| :--- | :--- | :--- | :--- | :--- | :--- |\n")
        for e in [x for x in entries if not x['legend']]:
            f.write(f"| {e['name']} | {e['biomes']} | {e['time']} | {e['season']} | {e['weather']} | {e['weight']} |\n")

if __name__ == "__main__":
    generate_table()
