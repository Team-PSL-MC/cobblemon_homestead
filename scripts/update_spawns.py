import os
import json
import re

# Configuration
SPAWN_DATA_PATH = 'data/cobblemon/spawn_pool_world/'
OUTPUT_FILE = 'wiki/spawns.md'

def format_name(raw_id):
    """ Cleans IDs like 'mythsandlegends-celebi-starlight' into 'Celebi Starlight' """
    name = raw_id.split(':')[-1]
    parts = re.split(r'[-_]', name)
    # Remove digits and the mod name prefix
    clean_parts = [p.capitalize() for p in parts if not p.isdigit() and p.lower() != 'mythsandlegends']
    final_name = " ".join(clean_parts)
    return final_name if final_name else name.capitalize()

def get_conditions(spawn_obj):
    """ Extracts item, time, season, and weather from the spawn object based on your JSON syntax """
    res = {"item": "None", "time": "Any", "season": "Any", "weather": "Clear"}
    
    # Grab the condition block
    cond = spawn_obj.get('condition', {})
    if not isinstance(cond, dict):
        return res

    # 1. Key Item (nested inside condition)
    found_item = cond.get('key_item') or cond.get('custom_absent_required_item') or cond.get('needed_item')
    if found_item:
        res["item"] = found_item.split(':')[-1].replace('_', ' ').title()

    # 2. Times of Day (handling list format)
    times = cond.get('times_of_day')
    if times:
        res["time"] = ", ".join([t.capitalize() for t in times])

    # 3. Weather & Season
    if 'weather' in cond:
        res["weather"] = cond['weather'].split(':')[-1].capitalize()
    if 'season' in cond:
        res["season"] = cond['season'].capitalize()

    return res

def generate_table():
    entries = []
    if not os.path.exists(SPAWN_DATA_PATH):
        print(f"Directory not found: {SPAWN_DATA_PATH}")
        return

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

                    # Weight check for Legendary status
                    is_legend = weight <= 1 or "myth" in filename.lower()
                    
                    entries.append({
                        "name": name, "biomes": biomes, "weight": weight,
                        "item": stats["item"], "time": stats["time"], 
                        "season": stats["season"], "weather": stats["weather"],
                        "legend": is_legend
                    })
            except Exception as e:
                print(f"Error parsing {filename}: {e}")

    # Alphabetical sort
    entries.sort(key=lambda x: x['name'])

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
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


# --- Auto-Sync to GitBook Summary ---
summary_path = 'SUMMARY.md'
spawn_link = "* [🐾 World Spawn List](wiki/spawns.md)"

if os.path.exists(summary_path):
    with open(summary_path, 'r') as f:
        content = f.read()
    
    if "wiki/spawns.md" not in content:
        with open(summary_path, 'a') as f:
            f.write(f"\n{spawn_link}")
        print("Added spawns.md to SUMMARY.md")
else:
    # Create SUMMARY.md if it doesn't exist
    with open(summary_path, 'w') as f:
        f.write(f"# Table of contents\n\n{spawn_link}")
