import os
import json
import re
import csv
from datetime import datetime

# Configuration
GITHUB_REPO = "Team-PSL-MC/cobblemon_homestead" 
SPAWN_DATA_PATH = 'data/cobblemon/spawn_pool_world/'
WIKI_DIR = 'wiki/cobblemon-gameplay/'
LEGENDARY_FILE = os.path.join(WIKI_DIR, 'legendaries.md')
CSV_FILE = 'full_spawn_list.csv'

GEN_RANGES = [
    (1, 151, "kanto"), (152, 251, "johto"), (252, 386, "hoenn"),
    (387, 493, "sinnoh"), (494, 649, "unova"), (650, 721, "kalos"),
    (722, 809, "alola"), (810, 905, "galar"), (906, 1025, "paldea")
]

def get_nav_bar(current_label):
    nav = "### 🗺️ National Pokédex Navigation\n\n"
    links = []
    for start, end, label in GEN_RANGES:
        if label == current_label:
            links.append(f"**{start}-{end}**")
        else:
            links.append(f"[{start}-{end}]({label}_spawns.md)")
    return nav + " | ".join(links) + "\n\n"

def get_resource_links():
    csv_url = f"https://github.com/{GITHUB_REPO}/blob/main/full_spawn_list.csv"
    return (
        "### 📑 Resources & Downloads\n\n"
        f"* [📥 **Download Homestead Custom Spawns (CSV)**]({csv_url})\n"
        "* [📊 Default Cobblemon Spawns (Official)](https://docs.google.com/spreadsheets/d/1DJT7Hd0ldgVUjJbN0kYQFAyNBP6JGG_Clkipax98x-g/edit?gid=0#gid=0)\n"
        "* [🎒 Cobblemon Drops (Official)](https://docs.google.com/spreadsheets/d/1EG8-VxLukiGWonM7e9J_DH0ZAVdkWo3W64bP2Allie6koo/edit?gid=0#gid=0)\n\n"
    )

def generate_tables():
    grouped_data = {}
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")

    if not os.path.exists(SPAWN_DATA_PATH): return

    # ... [Same parsing logic as before remains here] ...
    # (Simplified for brevity, use your existing parsing logic)
    for filename in os.listdir(SPAWN_DATA_PATH):
        if not filename.endswith('.json'): continue
        with open(os.path.join(SPAWN_DATA_PATH, filename), 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                for s in data.get('spawns', []):
                    # [Your existing parsing code]
                    pass 
            except: continue

    os.makedirs(WIKI_DIR, exist_ok=True)
    resource_links = get_resource_links()

    def write_safe_md(filepath, content):
        """Writes content with forced LF endings and no BOM for GitBook safety."""
        # Trim trailing whitespace from each line to prevent parser confusion
        clean_content = "\n".join([line.rstrip() for line in content.splitlines()])
        with open(filepath, 'w', encoding='utf-8', newline='\n') as f:
            f.write(clean_content + "\n")

    # 1. Generate Legendary Content
    legend_list = sorted([v for v in grouped_data.values() if v.get("is_legendary")], key=lambda x: x['dex'])
    leg_content = f"---\nlayout:\n  width: full\n---\n\n# 💎 Legendary Spawns\n\n"
    leg_content += get_nav_bar("legendaries") + "\n---\n\n"
    if not legend_list:
        leg_content += "No legendary spawns recorded yet.\n"
    else:
        leg_content += "| # | Pokémon | Key Item | Location & Rarity |\n| :--- | :--- | :--- | :--- |\n"
        for e in legend_list:
            safe_reqs = "<br>".join(e['requirements']).replace('|', r'\|')
            leg_content += f"| {e['dex']} | **{e['name']}** | {e['item']} | {safe_reqs} |\n"
    leg_content += f"\n---\n*Last Updated: {timestamp}*"
    write_safe_md(LEGENDARY_FILE, leg_content)

    # 2. Generate Regional Content
    for start, end, label in GEN_RANGES:
        gen_list = sorted([v for v in grouped_data.values() if not v.get("is_legendary") and start <= v["dex"] <= end], key=lambda x: x['dex'])
        reg_content = f"---\nlayout:\n  width: full\n---\n\n# 🌲 {label.title()} Spawns ({start}-{end})\n\n"
        reg_content += get_nav_bar(label)
        reg_content += resource_links
        reg_content += "\n---\n\n"
        
        if not gen_list:
            reg_content += f"No custom spawns recorded for the {label.title()} region yet.\n"
        else:
            reg_content += "| # | Pokémon | Location, Time & Rarity |\n| :--- | :--- | :--- |\n"
            for e in gen_list:
                safe_reqs = "<br>".join(e['requirements']).replace('|', r'\|')
                reg_content += f"| {e['dex']} | **{e['name']}** | {safe_reqs} |\n"
        
        reg_content += f"\n---\n*Last Updated: {timestamp}*"
        write_safe_md(os.path.join(WIKI_DIR, f"{label}_spawns.md"), reg_content)

    # 3. CSV Export (standard)
    with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Dex #', 'Name', 'Type', 'Requirements', 'Key Item'])
        for name in sorted(grouped_data.keys(), key=lambda x: grouped_data[x]['dex']):
            d = grouped_data[name]
            writer.writerow([d['dex'], d['name'], 'Legendary' if d['is_legendary'] else 'Standard', " | ".join(d['requirements']), d['item']])

if __name__ == "__main__":
    generate_tables()
