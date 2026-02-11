import os
import json
import re
from datetime import datetime

# Configuration
SPAWN_DATA_PATH = 'data/cobblemon/spawn_pool_world/'
LEGENDARY_FILE = 'wiki/cobblemon-gameplay/legendaries.md'
STANDARD_FILE = 'wiki/cobblemon-gameplay/spawns.md'

def parse_spawn_id(spawn_obj):
    """ 
    Extracts Dex Number and Name. 
    """
    raw_id = spawn_obj.get('id', '')
    pokemon_name = spawn_obj.get('pokemon', 'Unknown')
    
    # Try to find a number in the ID (e.g., "144-articuno")
    dex_num = 9999
    match = re.search(r'(\d+)', raw_id)
    if match:
        dex_num = int(match.group(1))
    
    # Simple clean name from the pokemon field
    name = pokemon_name.replace('_', ' ').title()
    
    return dex_num, name

def get_conditions(spawn_obj):
    res = {"item": "None", "time": "Any", "season": "Any", "weather": "Clear"}
    cond = spawn_obj.get('condition', {})
    if not isinstance(cond, dict): return res

    # Check for Key Items
    found_item = cond.get('key_item') or cond.get('custom_absent_required_item') or cond.get('needed_item')
    if found_item:
        res["item"] = found_item.split(':')[-1].replace('_', ' ').title()

    # Check for Time
    times = cond.get('times_of_day')
    if times: res["time"] = ", ".join([t.capitalize() for t in times])
    
    # Check for Nearby Blocks (Modded Machines)
    if 'location' in cond:
        loc = cond['location']
        if 'block' in loc:
            block_name = loc['block'].split(':')[-1].replace('_', ' ').title()
            res["biomes"] = f"Near {block_name}" # Overwrites biome with the machine name
    
    # Check for Weather/Season
    if 'weather' in cond: res["weather"] = cond['weather'].split(':')[-1].capitalize()
    if 'season' in cond: res["season"] = cond['season'].capitalize()
    return res

def generate_tables():
    legend_entries = []
    standard_entries = []
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")

    if not os.path.exists(SPAWN_DATA_PATH):
        print("Path not found!")
        return

    for filename in os.listdir(SPAWN_DATA_PATH):
        if not filename.endswith('.json'): continue
        with open(os.path.join(SPAWN_DATA_PATH, filename), 'r') as f:
            try:
                data = json.load(f)
                for s in data.get('spawns', []):
                    dex_num, name = parse_spawn_id(s)
                    weight = s.get('weight', 0)
                    stats = get_conditions(s)
                    
                    cond = s.get('condition', {})
                    biomes_list = cond.get('biomes', ["Global"])
                    biomes = ", ".join(biomes_list).replace('minecraft:', '').replace('cobblemon:', '').replace('#', '')

                    entry = {
                        "dex": dex_num, "name": name, "biomes": biomes, "weight": weight,
                        "item": stats["item"], "time": stats["time"], 
                        "season": stats["season"], "weather": stats["weather"]
                    }

                    # Legendaries are weight <= 1 OR in a file with "myth" in the name
                    if weight <= 1 or "myth" in filename.lower():
                        legend_entries.append(entry)
                    else:
                        standard_entries.append(entry)
            except: continue

    # Numerical Sort by Dex Number
    legend_entries.sort(key=lambda x: x['dex'])
    standard_entries.sort(key=lambda x: x['dex'])

    os.makedirs('wiki', exist_ok=True)

    # 1. Write Legendaries File
    with open(LEGENDARY_FILE, 'w') as f:
        f.write("# 💎 Legendary Spawns\n\n<small>\n\n")
        f.write("| # | Pokémon | Key Item | Biomes | Time | Season | Weather | Wt. |\n")
        f.write("| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n")
        for e in legend_entries:
            dex_str = f"#{e['dex']}" if e['dex'] != 9999 else "???"
            f.write(f"| {dex_str} | **{e['name']}** | {e['item']} | {e['biomes']} | {e['time']} | {e['season']} | {e['weather']} | {e['weight']} |\n")
        f.write(f"\n\n</small>\n\n---\n*Last Updated: {timestamp}*")

    # 2. Write Standard Spawns File
    with open(STANDARD_FILE, 'w') as f:
        f.write("# 🌲 Standard Spawns\n\n<small>\n\n")
        f.write("| # | Pokémon | Biomes | Time | Season | Weather | Rarity |\n")
        f.write("| :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n")
        for e in standard_entries:
            dex_str = f"#{e['dex']}" if e['dex'] != 9999 else "???"
            f.write(f"| {dex_str} | {e['name']} | {e['biomes']} | {e['time']} | {e['season']} | {e['weather']} | {e['weight']} |\n")
        f.write(f"\n\n</small>\n\n---\n*Last Updated: {timestamp}*")

if __name__ == "__main__":
    generate_tables()
