import os
import json
import re
from datetime import datetime
from pokemon_map import POKEMON_DEX  # Ensure this file exists in the same folder

# Shared Configuration
GITHUB_REPO = "Team-PSL-MC/cobblemon_homestead" 
SPAWN_DATA_PATH = 'data/cobblemon/spawn_pool_world/'
WIKI_DIR = 'wiki/cobblemon-gameplay/'

GEN_RANGES = [
    (1, 151, "kanto"), (152, 251, "johto"), (252, 386, "hoenn"),
    (387, 493, "sinnoh"), (494, 649, "unova"), (650, 721, "kalos"),
    (722, 809, "alola"), (810, 905, "galar"), (906, 1025, "paldea")
]

DIMENSION_MAP = {
    "twilightforest": "Twilight Forest",
    "eternal_starlight": "Eternal Starlight",
    "the_bumblezone": "Bumblezone",
    "minecraft": "Overworld",
    "nether": "Nether",
    "the_end": "The End",
    "stellaris": "Space",
    "aether": "Aether",
    "deep_aether": "Deep Aether"
}

def parse_spawn_id(spawn_obj):
    """Gets Dex ID from map first, then tries to regex the ID string."""
    pokemon_name_raw = spawn_obj.get('pokemon', 'unknown').lower()
    
    # 1. Try to get Dex Number from our Map
    dex_num = POKEMON_DEX.get(pokemon_name_raw, 9999)
    
    # 2. Fallback: try to find a number in the ID if not in map
    if dex_num == 9999:
        raw_id = spawn_obj.get('id', '')
        match = re.search(r'(\d+)', raw_id)
        if match: 
            dex_num = int(match.group(1))
            
    name = pokemon_name_raw.replace('_', ' ').title()
    return dex_num, name

def get_dimension(spawn_obj):
    """Identifies the dimension based on the mod prefix of the first biome."""
    biomes_list = spawn_obj.get('condition', {}).get('biomes', ["minecraft:global"])
    first_biome = biomes_list[0]
    mod_id = first_biome.split(':')[0] if ':' in first_biome else "minecraft"
    return DIMENSION_MAP.get(mod_id, "Overworld")

def clean_location(spawn_obj, stats):
    """Returns a clean location string (Biomes or Block context)."""
    if stats.get("location"):
        return stats["location"] 
    
    biomes_list = spawn_obj.get('condition', {}).get('biomes', ["Global"])
    clean_biomes = [b.split(':')[-1].replace('_', ' ').title() for b in biomes_list]
    return ", ".join(clean_biomes)

def get_nav_bar(current_label):
    nav = "### 🗺️ National Pokédex Navigation\n\n"
    links = []
    legend_link = "**Legendaries**" if current_label == "legendaries" else "[Legendaries](legendaries.md)"
    links.append(legend_link)
    
    for start, end, label in GEN_RANGES:
        if label == current_label:
            links.append(f"**{start}-{end}**")
        else:
            links.append(f"[{start}-{end}]({label}_spawns.md)")
    return nav + " | ".join(links) + "\n\n"

def get_conditions(spawn_obj):
    # Initialize keys
    res = {"item": "None", "time": "Any", "season": "Any", "weather": "Clear", "location": None, "special": None}
    
    cond = spawn_obj.get('condition', {})
    if not cond:
        return res

    # Check for items at top level or inside condition
    found_item = (spawn_obj.get('key_item') or spawn_obj.get('needed_item') or cond.get('key_item') or cond.get('needed_item'))
    if found_item: 
        res["item"] = str(found_item).split(':')[-1].replace('_', ' ').title()

    def scan_cond(c):
        if not isinstance(c, dict): return
        
        # --- Capture Special Requirements ---
        if 'structures' in c and isinstance(c['structures'], list):
            res["special"] = ", ".join([s.split(':')[-1].replace('_', ' ').title() for s in c['structures']])
            
        if 'neededNearbyBlocks' in c and isinstance(c['neededNearbyBlocks'], list):
            res["special"] = ", ".join([b.split(':')[-1].replace('_', ' ').title() for b in b])

        # --- Capture Environmental Extras ---
        if 'moonPhase' in c:
            phase_map = {0: "Full Moon", 1: "Waning Gibbous", 4: "New Moon"} # Expand as needed
            res["special"] = (res["special"] + " + " if res["special"] else "") + phase_map.get(c['moonPhase'], f"Moon Phase {c['moonPhase']}")
        
        # --- Capture Standard Conditions ---
        if 'times_of_day' in c: 
            res["time"] = ", ".join([t.capitalize() for t in c['times_of_day']])
        elif 'timeRange' in c:
            res["time"] = str(c['timeRange']).capitalize()

        if 'season' in c: 
            res["season"] = str(c['season']).capitalize()
        if 'weather' in c: 
            res["weather"] = c['weather'].split(':')[-1].capitalize()
        
        # Recursive check for nested logic
        for logical_key in ['and', 'or']:
            if logical_key in c and isinstance(c[logical_key], list):
                for sub_c in c[logical_key]: 
                    scan_cond(sub_c)

    scan_cond(cond)
    return res

def generate_special_wiki(special_spawns):
    """Generates the special.md table."""
    if not special_spawns:
        return

    content = "# ✨ Special Spawn Locations\n\n"
    content += "This table lists Pokémon that require specific structures or nearby blocks to appear.\n\n"
    content += "| Pokémon | Dimension | Special Requirement | Time | Weather |\n"
    content += "| :--- | :--- | :--- | :--- | :--- |\n"
    
    # Sort by Name
    sorted_special = sorted(special_spawns, key=lambda x: x['name'])
    
    for s in sorted_special:
        content += f"| {s['name']} | {s['dim']} | **{s['special']}** | {s['time']} | {s['weather']} |\n"
    
    write_safe_md(os.path.join(WIKI_DIR, 'special.md'), content)

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

def write_safe_md(filepath, content):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    clean_content = "\n".join([line.rstrip() for line in content.splitlines()])
    with open(filepath, 'w', encoding='utf-8', newline='\n') as f:
        f.write(clean_content + "\n")
