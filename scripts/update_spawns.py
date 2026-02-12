import os
import json
import re
import csv
from datetime import datetime

# Configuration
SPAWN_DATA_PATH = 'data/cobblemon/spawn_pool_world/'
WIKI_DIR = 'wiki/cobblemon-gameplay/'
LEGENDARY_FILE = os.path.join(WIKI_DIR, 'legendaries.md')
CSV_FILE = 'full_spawn_list.csv'

# Generation Ranges (Start, End, Filename Label)
GEN_RANGES = [
    (1, 151, "kanto"),
    (152, 251, "johto"),
    (252, 386, "hoenn"),
    (387, 493, "sinnoh"),
    (494, 649, "unova"),
    (650, 721, "kalos"),
    (722, 809, "alola"),
    (810, 905, "galar"),
    (906, 1025, "paldea")
]

# Navigation Bar Generator
def get_nav_bar():
    nav = "### National Pokédex Navigation\n"
    links = []
    for start, end, label in GEN_RANGES:
        links.append(f"[{start}-{end}]({label}_spawns.md)")
    return nav + " | ".join(links) + "\n\n---\n"

def parse_spawn_id(spawn_obj):
    raw_id = spawn_obj.get('id', '')
    pokemon_name = spawn_obj.get('pokemon', 'Unknown')
    dex_num = 9999
    match = re.search(r'(\d+)', raw_id)
    if match: dex_num = int(match.group(1))
    name = pokemon_name.replace('_', ' ').title()
    return dex_num, name

def get_conditions(spawn_obj):
    res = {"item": "None", "time": "Any", "season": "Any", "weather": "Clear", "location": None}
    found_item = (spawn_obj.get('key_item') or spawn_obj.get('needed_item') or spawn_obj.get('custom_absent_required_item'))
    cond = spawn_obj.get('condition', {})
    if isinstance(cond, dict) and not found_item:
        found_item = cond.get('key_item') or cond.get('needed_item')
    if found_item: res["item"] = str(found_item).split(':')[-1].replace('_', ' ').title()

    def scan_cond(c):
        if not isinstance(c, dict): return
        if 'times_of_day' in c: res["time"] = ", ".join([t.capitalize() for t in c['times_of_day']])
        if 'season' in c: res["season"] = c['season'].capitalize()
        if 'weather' in c: res["weather"] = c['weather'].split(':')[-1].capitalize()
        if 'location' in c and isinstance(c['location'], dict):
            loc = c['location']
            if 'block' in loc: res["location"] = "Near " + loc['block'].split(':')[-1].replace('_', ' ').title()
        for logical_key in ['and', 'or']:
            if logical_key in c and isinstance(c[logical_key], list):
                for sub_c in c[logical_key]: scan_cond(sub_c)

    scan_cond(cond)
    return res

def generate_tables():
    grouped_data = {}
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")

    if not os.path.exists(SPAWN_DATA_PATH): return

    for filename in os.listdir(SPAWN_DATA_PATH):
        if not filename.endswith('.json'): continue
        with open(os.path.join(SPAWN_DATA_PATH, filename), 'r') as f:
            try:
                data = json.load(f)
                for s in data.get('spawns', []):
                    dex_num, name = parse_spawn_id(s)
                    stats = get_conditions(s)
                    bucket = s.get('bucket', 'common').replace('_', '-').title()
                    
                    if stats["location"]: display_loc = stats["location"]
                    else:
                        biomes_list = s.get('condition', {}).get('biomes', ["Global"])
                        display_loc = ", ".join(biomes_list).replace('minecraft:', '').replace('cobblemon:', '').replace('#', '')

                    req_line = f"• {display_loc} ({stats['time']}) — **{bucket}**"
                    if stats["season"] != "Any": req_line = req_line.replace(")", f", {stats['season']})")

                    if name not in grouped_data:
                        grouped_data[name] = {
                            "dex": dex_num, "name": name, "item": stats["item"],
                            "requirements": [req_line], "is_legendary": (s.get('weight', 0) <= 1 or "myth" in filename.lower())
                        }
                    else:
                        if req_line not in grouped_data[name]["requirements"]:
                            grouped_data[name]["requirements"].append(req_line)
            except: continue

    os.makedirs(WIKI_DIR, exist_ok=True)
    nav_bar = get_nav_bar()

    # 1. Write Legendary File
    legend_list = sorted([v for v in grouped_data.values() if v["is_legendary"]], key=lambda x: x['dex'])
    with open(LEGENDARY_FILE, 'w') as f:
        f.write("---\nlayout:\n  width: full\n---\n\n# 💎 Legendary Spawns\n\n" + nav_bar)
        f.write("| # | Pokémon | Key Item | Location & Rarity |\n| :--- | :--- | :--- | :--- |\n")
        for e in legend_list:
            f.write(f"| {e['dex']} | **{e['name']}** | {e['item']} | {'<br>'.join(e['requirements'])} |\n")

    # 2. Write Generation Files
    for start, end, label in GEN_RANGES:
        gen_list = sorted([v for v in grouped_data.values() if not v["is_legendary"] and start <= v["dex"] <= end], key=lambda x: x['dex'])
        file_path = os.path.join(WIKI_DIR, f"{label}_spawns.md")
        with open(file_path, 'w') as f:
            f.write(f"---\nlayout:\n  width: full\n---\n\n# 🌲 {label.title()} Spawns ({start}-{end})\n\n" + nav_bar)
            f.write("| # | Pokémon | Location, Time & Rarity |\n| :--- | :--- | :--- |\n")
            for e in gen_list:
                f.write(f"| {e['dex']} | **{e['name']}** | {'<br>'.join(e['requirements'])} |\n")
            f.write(f"\n\n---\n*Last Updated: {timestamp}*")

    # 3. Export CSV
    with open(CSV_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Dex #', 'Name', 'Type', 'Requirements', 'Key Item'])
        for name in sorted(grouped_data.keys(), key=lambda x: grouped_data[x]['dex']):
            d = grouped_data[name]
            writer.writerow([d['dex'], d['name'], 'Legendary' if d['is_legendary'] else 'Standard', " | ".join(d['requirements']), d['item']])

if __name__ == "__main__":
    generate_tables()
