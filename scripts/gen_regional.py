import os
import json
from spawn_utils import *

def generate_regional_wiki():
    grouped_data = {}
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")

    for filename in os.listdir(SPAWN_DATA_PATH):
        if filename.endswith('.json') and not filename[0].isdigit():
            with open(os.path.join(SPAWN_DATA_PATH, filename), 'r', encoding='utf-8') as f:
                data = json.load(f)
                for s in data.get('spawns', []):
                    dex_num, name = parse_spawn_id(s)
                    stats = get_conditions(s)
                    
                    entry = {
                        "loc": clean_location(s, stats),
                        "time": stats['time'],
                        "season": stats['season'],
                        "rarity": s.get('bucket', 'common').replace('_', '-').title()
                    }

                    if name not in grouped_data:
                        grouped_data[name] = {"dex": dex_num, "name": name, "variants": [entry]}
                    else:
                        grouped_data[name]["variants"].append(entry)

    for start, end, label in GEN_RANGES:
        gen_list = sorted([v for v in grouped_data.values() if start <= v["dex"] <= end], key=lambda x: x['dex'])
        content = f"# 🌲 {label.title()} Spawns\n\n{get_nav_bar(label)}\n---\n\n"
        content += "| # | Pokémon | Location | Time | Season | Key Item | Rarity |\n"
        content += "| :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n"
        
        for d in gen_list:
            locs = "<br>".join([v['loc'] for v in d['variants']])
            times = "<br>".join([v['time'] for v in d['variants']])
            seasons = "<br>".join([v['season'] for v in d['variants']])
            rarities = "<br>".join([f"**{v['rarity']}**" for v in d['variants']])
            
            content += f"| {d['dex']} | **{d['name']}** | {locs} | {times} | {seasons} | None | {rarities} |\n"
        
        content += f"\n---\n*Last Updated: {timestamp}*"
        write_safe_md(os.path.join(WIKI_DIR, f"{label}_spawns.md"), content)

if __name__ == "__main__":
    generate_regional_wiki()
    print("✅ Regional Wiki updated successfully.")
