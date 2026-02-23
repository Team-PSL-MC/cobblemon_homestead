import os
import json
from spawn_utils import *

def generate_legendary_wiki():
    grouped_data = {}
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")

    for filename in os.listdir(SPAWN_DATA_PATH):
        if filename.endswith('.json') and filename[0].isdigit():
            with open(os.path.join(SPAWN_DATA_PATH, filename), 'r', encoding='utf-8') as f:
                data = json.load(f)
                for s in data.get('spawns', []):
                    dex_num, name = parse_spawn_id(s)
                    stats = get_conditions(s)
                    
                    entry = {
                        "loc": clean_location(s, stats),
                        "time": stats['time'],
                        "season": stats['season'],
                        "item": stats['item'],
                        "rarity": s.get('bucket', 'ultra-rare').replace('_', '-').title()
                    }

                    if name not in grouped_data:
                        grouped_data[name] = {"dex": dex_num, "name": name, "variants": [entry]}
                    else:
                        grouped_data[name]["variants"].append(entry)

    content = f"# 💎 Legendary Spawns\n\n{get_nav_bar('legendaries')}\n---\n\n"
    content += "| # | Pokémon | Location | Time | Season | Key Item | Rarity |\n"
    content += "| :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n"
    
    for name in sorted(grouped_data.keys(), key=lambda x: grouped_data[x]['dex']):
        d = grouped_data[name]
        # Join variants with <br> if there are multiple spawn conditions
        locs = "<br>".join([v['loc'] for v in d['variants']])
        times = "<br>".join([v['time'] for v in d['variants']])
        seasons = "<br>".join([v['season'] for v in d['variants']])
        items = d['variants'][0]['item'] # Key item is usually the same for all variants
        rarities = "<br>".join([f"**{v['rarity']}**" for v in d['variants']])
        
        content += f"| {d['dex']} | **{d['name']}** | {locs} | {times} | {seasons} | {items} | {rarities} |\n"
    
    content += f"\n---\n*Last Updated: {timestamp}*"
    write_safe_md(os.path.join(WIKI_DIR, 'legendaries.md'), content)
