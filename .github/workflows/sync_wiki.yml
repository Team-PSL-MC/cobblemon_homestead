import os
import json

# Configuration
SPAWN_DATA_PATH = 'data/cobblemon/spawn_pool_world/'
OUTPUT_FILE = 'wiki/spawns.md'

def get_requirement(spawn_obj):
    """ Digs through conditions to find the required item for Myths and Legends """
    # 1. Check for standard item condition
    condition = spawn_obj.get('condition', {})
    if isinstance(condition, dict):
        item = condition.get('item') or condition.get('custom_absent_required_item')
        if item:
            return item.replace('minecraft:', '').replace('cobblemon:', '').replace('_', ' ').title()
    
    # 2. Check for nested 'and' conditions (common in M&L)
    if isinstance(condition, dict) and 'and' in condition:
        for sub in condition['and']:
            item = sub.get('item') or sub.get('custom_absent_required_item')
            if item:
                return item.replace('minecraft:', '').replace('cobblemon:', '').replace('_', ' ').title()
                
    return "None"

def generate_table():
    entries = []
    
    if not os.path.exists(SPAWN_DATA_PATH):
        print(f"Error: Path {SPAWN_DATA_PATH} not found!")
        return

    for filename in os.listdir(SPAWN_DATA_PATH):
        if filename.endswith('.json'):
            with open(os.path.join(SPAWN_DATA_PATH, filename), 'r') as f:
                try:
                    data = json.load(f)
                    
                    # Cobblemon files usually have a top-level "spawns" list
                    spawn_list = data.get('spawns', [])
                    
                    for s in spawn_list:
                        pokemon = s.get('id', s.get('pokemon', 'Unknown')).split(':')[-1].replace('_', ' ').capitalize()
                        weight = s.get('weight', 0)
                        
                        # Extract biomes from the condition block
                        cond = s.get('condition', {})
                        biomes_list = cond.get('biomes', ["Global"])
                        biomes = ", ".join(biomes_list) if isinstance(biomes_list, list) else str(biomes_list)
                        
                        req_item = get_requirement(s)
                        
                        # Categorize as Legendary if weight is low or folder/filename suggests it
                        is_legend = weight <= 1 or "legendary" in filename.lower() or "mythic" in filename.lower()
                        
                        entries.append({
                            "name": pokemon,
                            "biomes": biomes,
                            "weight": weight,
                            "item": req_item,
                            "legend": is_legend
                        })
                except Exception as e:
                    print(f"Could not parse {filename}: {e}")

    # Sort: Legends first, then Alphabetical
    entries.sort(key=lambda x: (not x['legend'], x['name']))

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, 'w') as f:
        f.write("# 🐾 World Spawn List\n\n")
        f.write("> This list is automatically updated from the server's data packs.\n\n")
        
        f.write("## 💎 Legendary & Mythic Spawns\n")
        f.write("| Pokémon | Required Item | Biomes | Weight |\n")
        f.write("| :--- | :--- | :--- | :--- |\n")
        for e in [x for x in entries if x['legend']]:
            f.write(f"| **{e['name']}** | `{e['item']}` | {e['biomes']} | {e['weight']} |\n")
            
        f.write("\n---\n\n")
        f.write("## 🌲 Standard Spawns\n")
        f.write("| Pokémon | Biomes | Rarity |\n")
        f.write("| :--- | :--- | :--- |\n")
        for e in [x for x in entries if not x['legend']]:
            f.write(f"| {e['name']} | {e['biomes']} | {e['weight']} |\n")

if __name__ == "__main__":
    generate_table()
