def generate_legendary_wiki():
    grouped_data = {}
    special_list = []  # To store any Pokémon with a 'special' condition
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")

    for filename in os.listdir(SPAWN_DATA_PATH):
        if filename.endswith('.json'):
            with open(os.path.join(SPAWN_DATA_PATH, filename), 'r', encoding='utf-8') as f:
                data = json.load(f)
                for s in data.get('spawns', []):
                    dex_num, name = parse_spawn_id(s)
                    stats = get_conditions(s)
                    
                    # 1. ALWAYS check for Special Conditions (Citadels, Blocks, etc.)
                    if stats.get("special"):
                        special_list.append({
                            "name": name,
                            "dim": get_dimension(s),
                            "special": stats["special"],
                            "time": stats["time"],
                            "weather": stats["weather"]
                        })

                    # 2. ONLY add to Legendary Table if filename starts with a number
                    if filename[0].isdigit():
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

    # ... (Keep your existing legendary markdown building code) ...
    
    # 3. Final step: Write both files
    write_safe_md(os.path.join(WIKI_DIR, 'legendaries.md'), content)
    generate_special_wiki(special_list)