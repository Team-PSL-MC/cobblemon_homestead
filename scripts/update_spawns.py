import os
import json

# Configuration: Update these paths to match your Repo structure
SPAWN_DATA_PATH = 'data/cobblemon/spawn_pool_world/'
OUTPUT_FILE = 'wiki/spawns.md'

def get_requirement(spawn_data):
    # Logic to find "Myths and Legends" item requirements
    # Usually located in 'context' or 'condition'
    context = spawn_data.get('context', {})
    condition = spawn_data.get('condition', {})
    
    # Check for common item-requirement keys
    item = condition.get('item') or context.get('item') or "None"
    return item.replace('minecraft:', '').replace('cobblemon:', '').replace('_', ' ').title()

def generate_table():
    entries = []
    
    for filename in os.listdir(SPAWN_DATA_PATH):
        if filename.endswith('.json'):
            with open(os.path.join(SPAWN_DATA_PATH, filename), 'r') as f:
                data = json.load(f)
                
                # Handle single spawns or arrays
                spawns = data if isinstance(data, list) else [data]
                
                for s in spawns:
                    if not s.get('enabled', True): continue
                    
                    pokemon = s.get('pokemon', 'Unknown').capitalize()
                    weight = s.get('weight', 0)
                    biomes = ", ".join(s.get('biomes', ['Global']))
                    req_item = get_requirement(s)
                    
                    # Tag Legendaries for sorting (usually weight < 1 or specific file prefix)
                    is_legend = weight <= 1 or "legendary" in filename.lower()
                    
                    entries.append({
                        "name": pokemon,
                        "biomes": biomes,
                        "weight": weight,
                        "item": req_item,
                        "legend": is_legend
                    })

    # Sort: Legends at the top, then alphabetically
    entries.sort(key=lambda x: (not x['legend'], x['name']))

    with open(OUTPUT_FILE, 'w') as f:
        f.write("# 🐾 World Spawn List\n\n")
        f.write("> This list is automatically updated from the server's data packs.\n\n")
        
        f.write("### 💎 Legendary & Mythic Spawns\n")
        f.write("| Pokémon | Required Item | Biomes | Weight |\n")
        f.write("| :--- | :--- | :--- | :--- |\n")
        for e in [x for x in entries if x['legend']]:
            f.write(f"| **{e['name']}** | `{e['item']}` | {e['biomes']} | {e['weight']} |\n")
            
        f.write("\n### 🌲 Standard Spawns\n")
        f.write("| Pokémon | Biomes | Rarity |\n")
        f.write("| :--- | :--- | :--- |\n")
        for e in [x for x in entries if not x['legend']]:
            f.write(f"| {e['name']} | {e['biomes']} | {e['weight']} |\n")

if __name__ == "__main__":
    generate_table()
