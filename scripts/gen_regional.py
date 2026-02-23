import os
import json
from spawn_utils import *

def generate_regional_wiki():
    grouped_data = {}
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")

    for filename in os.listdir(SPAWN_DATA_PATH):
        # Only process biome files (don't start with numbers)
        if filename.endswith('.json') and not filename[0].isdigit():
            with open(os.path.join(SPAWN_DATA_PATH, filename), 'r', encoding='utf-8') as f:
                data = json.load(f)
                for s in data.get('spawns', []):
                    dex_num, name = parse_spawn_id(s)
                    stats = get_conditions(s)
                    bucket = s.get('bucket', 'common').title()
                    
                    biomes_list = s.get('condition', {}).get('biomes', ["Global"])
                    display_loc = ", ".join(biomes_list).replace('minecraft:', '').replace('cobblemon:', '').replace('#', '')
                    req_line = f"• {display_loc} ({stats['time']}) — **{bucket}**"

                    if name not in grouped_data:
                        grouped_data[name] = {"dex": dex_num, "name": name, "requirements": [req_line]}
                    elif req_line not in grouped_data[name]["requirements"]:
                        grouped_data[name]["requirements"].append(req_line)

    for start, end, label in GEN_RANGES:
        gen_list = sorted([v for v in grouped_data.values() if start <= v["dex"] <= end], key=lambda x: x['dex'])
        content = f"# 🌲 {label.title()} Spawns ({start}-{end})\n\n{get_nav_bar(label)}\n---\n\n"
        content += "| # | Pokémon | Location, Time & Rarity |\n| :--- | :--- | :--- |\n"
        
        for e in gen_list:
            safe_reqs = "<br>".join(e['requirements']).replace('|', r'\|')
            content += f"| {e['dex']} | **{e['name']}** | {safe_reqs} |\n"
        
        content += f"\n---\n*Last Updated: {timestamp}*"
        write_safe_md(os.path.join(WIKI_DIR, f"{label}_spawns.md"), content)
    
    print("✅ Regional Wikis Updated.")

if __name__ == "__main__":
    generate_regional_wiki()
