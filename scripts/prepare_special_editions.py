import os
import re
import json
import shutil

def setup_directories():
    for d in [
        "assets/flags_malaysia",
        "static/flags_malaysia",
        "assets/flags_usa",
        "static/flags_usa",
        "assets/data"
    ]:
        os.makedirs(d, exist_ok=True)

def process_malaysia_flags():
    src_dir = "temp_my_flags/flags/1x2"
    if not os.path.exists(src_dir):
        print(f"Error: {src_dir} not found!")
        return []
    
    # Metadata for Malaysian states & federal territories
    states_meta = [
        {"code": "jhr", "name": "Johor", "capital": "Johor Bahru", "type": "State"},
        {"code": "kdh", "name": "Kedah", "capital": "Alor Setar", "type": "State"},
        {"code": "ktn", "name": "Kelantan", "capital": "Kota Bharu", "type": "State"},
        {"code": "mlk", "name": "Melaka", "capital": "Melaka City", "type": "State"},
        {"code": "nsn", "name": "Negeri Sembilan", "capital": "Seremban", "type": "State"},
        {"code": "phg", "name": "Pahang", "capital": "Kuantan", "type": "State"},
        {"code": "png", "name": "Penang", "capital": "George Town", "type": "State"},
        {"code": "prk", "name": "Perak", "capital": "Ipoh", "type": "State"},
        {"code": "pls", "name": "Perlis", "capital": "Kangar", "type": "State"},
        {"code": "sbh", "name": "Sabah", "capital": "Kota Kinabalu", "type": "State"},
        {"code": "swk", "name": "Sarawak", "capital": "Kuching", "type": "State"},
        {"code": "sgr", "name": "Selangor", "capital": "Shah Alam", "type": "State"},
        {"code": "trg", "name": "Terengganu", "capital": "Kuala Terengganu", "type": "State"},
        {"code": "kul", "name": "Kuala Lumpur", "capital": "Kuala Lumpur", "type": "Federal Territory"},
        {"code": "lbn", "name": "Labuan", "capital": "Victoria", "type": "Federal Territory"},
        {"code": "pjy", "name": "Putrajaya", "capital": "Putrajaya", "type": "Federal Territory"},
        {"code": "ft", "name": "Wilayah Persekutuan", "capital": "Kuala Lumpur", "type": "Federal Territory"}
    ]
    
    records = []
    for item in states_meta:
        code = item["code"]
        src_svg = os.path.join(src_dir, f"{code}.svg")
        if os.path.exists(src_svg):
            dest_asset = f"assets/flags_malaysia/{code}.svg"
            dest_static = f"static/flags_malaysia/{code}.svg"
            shutil.copyfile(src_svg, dest_asset)
            shutil.copyfile(src_svg, dest_static)
            
            records.append({
                "code": code,
                "name": item["name"],
                "capital": item["capital"],
                "type": item["type"],
                "continent": "Malaysia",
                "edition": "Malaysian States",
                "emoji": "🇲🇾",
                "flag_path": dest_asset,
                "web_flag_path": f"/app/static/flags_malaysia/{code}.svg"
            })
            print(f"Copied Malaysia flag: {item['name']} ({code})")
        else:
            print(f"Warning: Missing {src_svg}")
            
    with open("assets/data/malaysia_states.json", "w") as f:
        json.dump(records, f, indent=2)
    print(f"Saved {len(records)} Malaysian state records to assets/data/malaysia_states.json")
    return records

def process_usa_flags():
    meta_path = "temp_us_flags/src/data/states.json"
    flags_src_dir = "temp_us_flags/src/components/flags"
    
    if not os.path.exists(meta_path) or not os.path.exists(flags_src_dir):
        print(f"Error: US flags source directories not found!")
        return []
        
    with open(meta_path) as f:
        states = json.load(f)
        
    records = []
    for s in states:
        abbr = s["abbreviation"]
        code = abbr.lower()
        js_file = os.path.join(flags_src_dir, f"Flag{abbr}.js")
        
        if not os.path.exists(js_file):
            print(f"Warning: missing {js_file}")
            continue
            
        with open(js_file, "r") as f:
            js_content = f.read()
            
        vb_match = re.search(r"viewBox:\s*['\"]([^'\"]+)['\"]", js_content)
        viewbox = vb_match.group(1) if vb_match else "0 0 250 167"
        
        html_match = re.search(r"__html:\s*`([^`]+)`", js_content, re.DOTALL)
        inner_html = html_match.group(1).strip() if html_match else ""
        
        svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="{viewbox}" width="250" height="167">
{inner_html}
</svg>'''

        dest_asset = f"assets/flags_usa/{code}.svg"
        dest_static = f"static/flags_usa/{code}.svg"
        
        with open(dest_asset, "w") as f:
            f.write(svg_content)
        with open(dest_static, "w") as f:
            f.write(svg_content)
            
        records.append({
            "code": code,
            "abbr": abbr,
            "name": s["name"],
            "capital": s["capital"],
            "territory": s.get("territory", False),
            "continent": "United States",
            "edition": "USA States",
            "emoji": "🇺🇸",
            "flag_path": dest_asset,
            "web_flag_path": f"/app/static/flags_usa/{code}.svg"
        })
        print(f"Generated US flag: {s['name']} ({abbr})")
        
    with open("assets/data/usa_states.json", "w") as f:
        json.dump(records, f, indent=2)
    print(f"Saved {len(records)} US state records to assets/data/usa_states.json")
    return records

if __name__ == "__main__":
    setup_directories()
    my_records = process_malaysia_flags()
    us_records = process_usa_flags()
    print("Done! Total Malaysia:", len(my_records), "Total US:", len(us_records))
