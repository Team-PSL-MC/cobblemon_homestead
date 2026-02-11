import json
import os
import sys

def validate_json_files(path):
    errors_found = False
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.json'):
                full_path = os.path.join(root, file)
                try:
                    with open(full_path, 'r') as f:
                        json.load(f)
                except json.JSONDecodeError as e:
                    print(f"❌ Syntax Error in {full_path}: {e}")
                    errors_found = True
    return errors_found

if __name__ == "__main__":
    if validate_json_files('data/'):
        sys.exit(1) # Stop the GitHub Action
    print("✅ All JSON files are valid!")