import os
import json
import re
from datetime import datetime

# Shared Configuration
GITHUB_REPO = "Team-PSL-MC/cobblemon_homestead" 
SPAWN_DATA_PATH = 'data/cobblemon/spawn_pool_world/'
WIKI_DIR = 'wiki/cobblemon-gameplay/'
GEN_RANGES = [
    (1, 151, "kanto"), (152, 251, "johto"), (252, 386, "hoenn"),
    (387, 493, "sinnoh"), (494, 649, "unova"), (650, 721, "kalos"),
    (722, 809, "alola"), (810, 905, "galar"), (906, 1025, "paldea")
]

def get_nav_bar(current_label):
    nav = "### 🗺️ National Pokédex Navigation\n\n"
    links = []
    # Add Legendary to Nav
    legend_link = "**Legendaries**" if current_label == "legendaries" else "[Legendaries](legendaries.md)"
    links.append(legend_link)
    
    for start, end, label in GEN_RANGES:
        if label == current_label:
            links.append(f"**{start}-{end}**")
        else:
            links.append(f"[{start}-{end}]({label}_spawns.md)")
    return nav + " | ".join(links) + "\n\n"

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
    if found_item: 
        res["item"] = str(found_item).split(':')[-1].replace('_', ' ').title()

    def scan_cond(c):
        if not isinstance(c, dict): return
        if 'times_of_day' in c: 
            res["time"] = ", ".join([t.capitalize() for t in c['times_of_day']])
        if 'season' in c: 
            res["season"] = c['season'].capitalize()
        if 'weather' in c: 
            res["weather"] = c['weather'].split(':')[-1].capitalize()
        if 'location' in c and isinstance(c['location'], dict):
            loc = c['location']
            if 'block' in loc: 
                res["location"] = "Near " + loc['block'].split(':')[-1].replace('_', ' ').title()
        
        for logical_key in ['and', 'or']:
            if logical_key in c and isinstance(c[logical_key], list):
                for sub_c in c[logical_key]: 
                    scan_cond(sub_c)

    scan_cond(cond)
    return res

def clean_location(spawn_obj, stats):
    """Returns a clean location string (Biomes or Block context)."""
    if stats.get("location"):
        return stats["location"] 
    
    biomes_list = spawn_obj.get('condition', {}).get('biomes', ["Global"])
    clean_biomes = [b.split(':')[-1].replace('_', ' ').title() for b in biomes_list]
    return ", ".join(clean_biomes)

def write_safe_md(filepath, content):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    # Strips trailing whitespace to keep GitBook files clean
    clean_content = "\n".join([line.rstrip() for line in content.splitlines()])
    with open(filepath, 'w', encoding='utf-8', newline='\n') as f:
        f.write(clean_content + "\n")
