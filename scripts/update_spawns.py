import os
import json
import re
from datetime import datetime

# Configuration
SPAWN_DATA_PATH = 'data/cobblemon/spawn_pool_world/'
LEGENDARY_FILE = 'wiki/legendaries.md'
STANDARD_FILE = 'wiki/spawns.md'

def format_name(raw_id):
    name = raw_id.split(':')[-1]
    parts = re.split(r'[-_]', name)
    clean_parts = [p.capitalize() for p in parts if not p.isdigit() and p.lower() != 'mythsandlegends']
    final_name = " ".join(clean_parts)
    return final_name if final_name else name.capitalize()

def get_conditions(spawn_obj):
    res = {"item": "None", "time": "Any", "season": "Any", "weather": "Clear"}
    cond = spawn_obj.get('condition', {})
    if not isinstance(cond, dict): return res

    found_item = cond.get('key_item') or cond.get('custom_absent_required_item') or cond.get('needed_item')
    if found_item:
        res["item"] = found_item.split(':')[-1].replace('_', ' ').title()

    times = cond.get('times_of_day')
    if times: res["time"] = ", ".join([t.capitalize() for t in times])

    if 'weather' in cond: res["weather"] = cond['weather'].split(':')[-1].capitalize()
    if 'season' in cond: res["season"] = cond['season'].capitalize()
    return res

def generate_tables():
    legend_entries = []
    standard_entries = []
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")

    if not os.path.exists(SPAWN_DATA_PATH): return

    for filename in os.listdir(SPAWN_DATA_PATH):
        if not filename.endswith('.json'): continue
        with open(os.path.join(SPAWN_DATA_PATH, filename), 'r') as f:
            try:
                data = json.load(f)
                for s in data.get('spawns', []):
                    name = format_name(s.get('id', s.get('pokemon', 'Unknown')))
                    weight = s.get('weight', 0)
                    stats = get_conditions(s)
                    
                    cond = s.get('condition', {})
                    biomes_list = cond.get('biomes', ["Global"])
                    biomes = ", ".join(biomes_list) if isinstance(biomes_list, list) else str(biomes_list)
                    biomes = biomes.replace('minecraft:', '').replace('cobblemon:', '').replace('#', '')

                    entry = {
                        "name": name, "biomes": biomes, "weight": weight,
                        "item": stats["item"], "time": stats["time"], 
                        "season": stats["season"], "weather": stats["weather"]
                    }

                    if weight <= 1 or "myth" in filename.lower():
                        legend_entries.append(entry)
                    else:
                        standard_entries.append(entry)
            except: continue

    # Sort Alphabetically
    legend_entries.sort(key=lambda x: x['name'])
    standard_entries.sort(key=lambda x: x['name'])

    os.makedirs('wiki', exist_ok=True)

    # 1. Write Legendaries File
    with open(LEGENDARY_FILE, 'w') as f:
        f.write("# 💎 Legendary Spawns\n\n")
        f.write("| Pokémon | Key Item | Biomes | Time | Season | Weather | Weight |\n")
        f.write("| :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n")
        for e in legend_entries:
            f.write(f"| **{e['name']}** | `{e['item']}` | {e['biomes']} | {e['time']} | {e['season']} | {e['weather']} | {e['weight']} |\n")
        f.write(f"\n\n---\n*Last Updated: {timestamp}*")

    # 2. Write Standard Spawns File
    with open(STANDARD_FILE, 'w') as f:
        f.write("# 🌲 Standard Spawns\n\n")
        f.write("> 💡 Looking for default Cobblemon spawns? Check the [Official Spawn Spreadsheet](https://docs.google.com/spreadsheets/d/1DJT7Hd0ldgVUjJbN0kYQFAyNBP6JGG_Clkipax98x-g/edit?gid=0#gid=0).\n\n")
        f.write("| Pokémon | Biomes | Time | Season | Weather | Rarity |\n")
        f.write("| :--- | :--- | :--- | :--- | :--- | :--- |\n")
        for e in standard_entries:
            f.write(f"| {e['name']} | {e['biomes']} | {e['time']} | {e['season']} | {e['weather']} | {e['weight']} |\n")
        f.write(f"\n\n---\n*Last Updated: {timestamp}*")

if __name__ == "__main__":
    generate_tables()
