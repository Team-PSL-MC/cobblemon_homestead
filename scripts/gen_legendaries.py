import os
import json
from spawn_utils import *

def generate_legendary_wiki():
    grouped_data = {}
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")

    # 1. Collect Data
    for filename in os.listdir(SPAWN_DATA_PATH):
        # Only process files starting with numbers (Legendaries)
        if filename.endswith('.json') and filename[0].isdigit():
            with open(os.path.join(SPAWN_DATA_PATH, filename), 'r', encoding='utf-8') as f:
                data = json.load(f)
                for s in data.get('spawns', []):
                    dex_num, name = parse_spawn_id(s)
                    stats = get_conditions(s)
                    
                    entry = {
                        "world": get_dimension(s),
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

    # 2. Build Markdown Content
    content = f"# 💎 Legendary Spawns\n\n{get_nav_bar('legendaries')}\n---\n\n"
    
    # Updated Header with "World"
    content += "| # | Pokémon | World | Location | Time | Season | Key Item | Rarity |\n"
    content += "| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n"
    
    # 3. Sort by Pokedex Number and Generate Rows
    for name in sorted(grouped_data.keys(), key=lambda x: grouped_data[x]['dex']):
        d = grouped_data[name]
        
        # Use <br> to handle multiple spawn sets for the same Pokemon
        worlds = "<br>".join([v['world'] for v in d['variants']])
        locs = "<br>".join([v['loc'] for v in d['variants']])
        times = "<br>".join([v['time'] for v in d['variants']])
        seasons = "<br>".join([v['season'] for v in d['variants']])
        rarities = "<br>".join([f"**{v['rarity']}**" for v in d['variants']])
        
        # Key item is usually constant for the species, taking from first variant
        item = d['variants'][0]['item']
        
        content += f"| {d['dex']} | **{d['name']}** | {worlds} | {locs} | {times} | {seasons} | {item} | {rarities} |\n"
    
    content += f"\n---\n*Last Updated: {timestamp}*"
    
    # 4. Write to File
    write_safe_md(os.path.join(WIKI_DIR, 'legendaries.md'), content)

if __name__ == "__main__":
    generate_legendary_wiki()
    print("✅ Legendary Wiki updated successfully with World column.")
