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
    cond = spawn_obj.get('condition', {})
    if not isinstance(cond, dict): return res

    # 1. Check for Key Items (Looks in the 'condition' block)
    found_item = cond.get('key_item') or cond.get('custom_absent_required_item') or cond.get('needed_item')
    if found_item:
        res["item"] = found_item.split(':')[-1].replace('_', ' ').title()

    # 2. Check for Time
    times = cond.get('times_of_day')
    if times: res["time"] = ", ".join([t.capitalize() for t in times])
    
    # 3. Check for Nearby Blocks (Modded Machines)
    if 'location' in cond:
        loc = cond['location']
        if 'block' in loc:
            res["location"] = "Near " + loc['block'].split(':')[-1].replace('_', ' ').title()
    
    # 4. Check for Weather/Season
    if 'weather' in cond: res["weather"] = cond['weather'].split(':')[-1].capitalize()
    if 'season' in cond: res["season"] = cond['season'].capitalize()
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
