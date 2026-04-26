import json
import os

FILE = "data.json"

def load_data():
    if not os.path.exists(FILE) or os.stat(FILE).st_size == 0:
        return {}

    try:
        with open(FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}

def save_data(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)
