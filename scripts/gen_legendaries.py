import os
import json
from spawn_utils import *

LEGENDARY_FILE = os.path.join(WIKI_DIR, 'legendaries.md')

def generate_legendary_wiki():
    grouped_data = {}
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")

    for filename in os.listdir(SPAWN_DATA_PATH):
        # Only process files that start with a number (Legendary pattern)
        if filename.endswith('.json') and filename[0].isdigit():
            with open(os.path.join(SPAWN_DATA_PATH, filename), 'r', encoding='utf-8') as f:
                data = json.load(f)
                for s in data.get('spawns', []):
                    dex_num, name = parse_spawn_id(s)
                    stats = get_conditions(s)
                    bucket = s.get('bucket', 'ultra-rare').title()
                    
                    biomes_list = s.get('condition', {}).get('biomes', ["Global"])
                    display_loc = ", ".join(biomes_list).replace('minecraft:', '').replace('cobblemon:', '').replace('#', '')
                    req_line = f"• {display_loc} ({stats['time']}) — **{bucket}**"

                    if name not in grouped_data:
                        grouped_data[name] = {"dex": dex_num, "name": name, "item": stats["item"], "requirements": [req_line]}
                    elif req_line not in grouped_data[name]["requirements"]:
                        grouped_data[name]["requirements"].append(req_line)

    legend_list = sorted(grouped_data.values(), key=lambda x: x['dex'])
    content = f"# 💎 Legendary Spawns\n\n{get_nav_bar('legendaries')}\n---\n\n"
    content += "| # | Pokémon | Key Item | Location & Rarity |\n| :--- | :--- | :--- | :--- |\n"
    
    for e in legend_list:
        safe_reqs = "<br>".join(e['requirements']).replace('|', r'\|')
        content += f"| {e['dex']} | **{e['name']}** | {e['item']} | {safe_reqs} |\n"
    
    content += f"\n---\n*Last Updated: {timestamp}*"
    write_safe_md(LEGENDARY_FILE, content)
    print("✅ Legendary Wiki Updated.")

if __name__ == "__main__":
    generate_legendary_wiki()
