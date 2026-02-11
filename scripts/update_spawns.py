import os
import json
import re
from datetime import datetime

# Configuration
SPAWN_DATA_PATH = 'data/cobblemon/spawn_pool_world/'
LEGENDARY_FILE = 'wiki/cobblemon-gameplay/legendaries.md'
STANDARD_FILE = 'wiki/cobblemon-gameplay/spawns.md'

def parse_spawn_id(spawn_obj):
    raw_id = spawn_obj.get('id', '')
    pokemon_name = spawn_obj.get('pokemon', 'Unknown')
    dex_num = 9999
    match = re.search(r'(\d+)', raw_id)
    if match:
        dex_num = int(match.group(1))
    name = pokemon_name.replace('_', ' ').title()
    return dex_num, name

def get_conditions(spawn_obj):
    # Initialize with defaults
    res = {"item": "None", "time": "Any", "season": "Any", "weather": "Clear", "location": None}
    
    # 1. Look for Key Item (Checks BOTH the main spawn object AND the condition block)
    # This fixes your Enamorus Key Item issue
    found_item = (spawn_obj.get('key_item') or 
                  spawn_obj.get('needed_item') or 
                  spawn_obj.get('custom_absent_required_item'))
    
    cond = spawn_obj.get('condition', {})
    if isinstance(cond, dict):
        # Also check inside condition if not found yet
        if not found_item:
            found_item = cond.get('key_item') or cond.get('needed_item')

    if found_item:
        res["item"] = str(found_item).split(':')[-1].replace('_', ' ').title()

    # 2. Helper to scan nested conditions (for "and", "or" blocks)
    def scan_cond(c):
        if not isinstance(c, dict): return
        
        # Check for Time
        if 'times_of_day' in c:
            res["time"] = ", ".join([t.capitalize() for t in c['times_of_day']])
        
        # Check for Season
        if 'season' in c:
            res["season"] = c['season'].capitalize()
            
        # Check for Weather
        if 'weather' in c:
            res["weather"] = c['weather'].split(':')[-1].capitalize()

        # Check for Location/Blocks
        if 'location' in c and isinstance(c['location'], dict):
            loc = c['location']
            if 'block' in loc:
                res["location"] = "Near " + loc['block'].split(':')[-1].replace('_', ' ').title()

        # Recurse into 'and' or 'or' lists (Fixes your Enamorus block issue)
        for logical_key in ['and', 'or']:
            if logical_key in c and isinstance(c[logical_key], list):
                for sub_c in c[logical_key]:
                    scan_cond(sub_c)

    # Start scanning from the root condition
    scan_cond(cond)
    
    return res

def generate_tables():
    legend_entries = []
    standard_entries = []
    summary_list = []
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
                    
                    # Logic Fix: If we found a specific block location, use that. 
                    # Otherwise, use the Biomes list.
                    if stats["location"]:
                        display_location = stats["location"]
                    else:
                        cond = s.get('condition', {})
                        biomes_list = cond.get('biomes', ["Global"])
                        display_location = ", ".join(biomes_list).replace('minecraft:', '').replace('cobblemon:', '').replace('#', '')

                    entry = {
                        "dex": dex_num, "name": name, "biomes": display_location, "weight": weight,
                        "item": stats["item"], "time": stats["time"], 
                        "season": stats["season"], "weather": stats["weather"]
                    }

                    summary_list.append(f"- {name}")

                    if weight <= 1 or "myth" in filename.lower():
                        legend_entries.append(entry)
                    else:
                        standard_entries.append(entry)
            except Exception as e: 
                print(f"Error parsing {filename}: {e}")
                continue

    # Numerical Sort
    legend_entries.sort(key=lambda x: x['dex'])
    standard_entries.sort(key=lambda x: x['dex'])

    # Write Files
    os.makedirs(os.path.dirname(LEGENDARY_FILE), exist_ok=True)

    with open(LEGENDARY_FILE, 'w') as f:
        f.write("# 💎 Legendary Spawns\n\n<small>\n\n| # | Pokémon | Key Item | Location | Time | Season | Weather | Wt. |\n| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n")
        for e in legend_entries:
            f.write(f"| {e['dex']} | **{e['name']}** | {e['item']} | {e['biomes']} | {e['time']} | {e['season']} | {e['weather']} | {e['weight']} |\n")
        f.write(f"\n\n</small>\n\n---\n*Last Updated: {timestamp}*")

    with open(STANDARD_FILE, 'w') as f:
        f.write("# 🌲 Standard Spawns\n\n<small>\n\n| # | Pokémon | Location | Time | Season | Weather | Rarity |\n| :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n")
        for e in standard_entries:
            f.write(f"| {e['dex']} | {e['name']} | {e['biomes']} | {e['time']} | {e['season']} | {e['weather']} | {e['weight']} |\n")
        f.write(f"\n\n</small>\n\n---\n*Last Updated: {timestamp}*")

    # Generate the version summary for GitHub Releases
    with open('version_summary.txt', 'w') as f:
        f.write("## 🐾 Featured Pokémon in this build:\n")
        f.write("\n".join(sorted(set(summary_list))))

if __name__ == "__main__":
    generate_tables()
