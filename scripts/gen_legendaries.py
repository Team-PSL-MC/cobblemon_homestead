def generate_legendary_wiki():
    grouped_data = {}
    special_list = [] # <--- 1. CREATE THIS LIST
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")

    for filename in os.listdir(SPAWN_DATA_PATH):
        if filename.endswith('.json'): # Removed the [0].isdigit() to catch ALL special spawns
            with open(os.path.join(SPAWN_DATA_PATH, filename), 'r', encoding='utf-8') as f:
                data = json.load(f)
                for s in data.get('spawns', []):
                    dex_num, name = parse_spawn_id(s)
                    stats = get_conditions(s)
                    
                    # --- 2. ADD TO SPECIAL LIST IF CONDITION EXISTS ---
                    if stats.get("special"):
                        special_list.append({
                            "name": name,
                            "dim": get_dimension(s),
                            "special": stats["special"],
                            "time": stats["time"],
                            "weather": stats["weather"]
                        })

                    # --- 3. ONLY ADD TO LEGENDARY TABLE IF FILENAME STARTS WITH NUMBER ---
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

    # ... (Keep your existing legendary table building code) ...
    
    # 4. WRITE THE SPECIAL WIKI AT THE END
    generate_special_wiki(special_list) 

if __name__ == "__main__":
    generate_legendary_wiki()