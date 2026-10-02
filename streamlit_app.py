import streamlit as st
import json
import base64
import os
import random
import streamlit.components.v1 as components

# ==============================================================================
# Page Configuration
# ==============================================================================
st.set_page_config(
    page_title="Catch the Flag! 🚩 Kids Game",
    page_icon="🚩",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# Load Country & State Flag Datasets (Base64 SVG Encoded)
# ==============================================================================
def _load_dataset_file(filename):
    json_path = os.path.join(os.path.dirname(__file__), "assets", "data", filename)
    if not os.path.exists(json_path):
        return []
    with open(json_path, "r", encoding="utf-8") as f:
        items = json.load(f)

    for item in items:
        rel_path = item.get("flag", item.get("flag_path", ""))
        flag_path = os.path.join(os.path.dirname(__file__), rel_path)
        try:
            with open(flag_path, "rb") as svg_file:
                item["flag_data"] = "data:image/svg+xml;base64," + base64.b64encode(svg_file.read()).decode("utf-8")
        except Exception:
            item["flag_data"] = ""
    return items

@st.cache_data
def load_all_game_datasets():
    return {
        "countries": _load_dataset_file("countries.json"),
        "malaysia": _load_dataset_file("malaysia_states.json"),
        "usa": _load_dataset_file("usa_states.json")
    }

game_datasets = load_all_game_datasets()
countries_data = game_datasets["countries"]
malaysia_data = game_datasets["malaysia"]
usa_data = game_datasets["usa"]

@st.cache_data
def load_map_data():
    map_path = os.path.join(os.path.dirname(__file__), "assets", "maps", "kids-world-map.svg")
    with open(map_path, "rb") as f:
        return "data:image/svg+xml;base64," + base64.b64encode(f.read()).decode("utf-8")

world_map_uri = load_map_data()

# ==============================================================================
# Global Theme Styling (Kids Learning Game UI Kit)
# ==============================================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Outfit', sans-serif !important;
}

.stApp {
    background-color: #FFFDF9;
    color: #1E293B;
}

/* Sidebar Custom Styling */
[data-testid="stSidebar"] {
    background-color: #FFF6EC !important;
    border-right: 2px solid #EFE4D6;
}

/* Custom 3D Buttons */
div.stButton > button {
    border-radius: 9999px !important;
    font-weight: 800 !important;
    font-size: 15px !important;
    padding: 10px 22px !important;
    border: none !important;
    transition: all 0.1s ease !important;
    box-shadow: 0 4px 0 #E26400 !important;
    background-color: #FF7A00 !important;
    color: #FFFFFF !important;
}
div.stButton > button:hover {
    filter: brightness(1.05) !important;
    color: #FFFFFF !important;
}
div.stButton > button:active {
    transform: translateY(2px) !important;
    box-shadow: 0 2px 0 #E26400 !important;
}

/* Chips */
.kid-chip {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 6px 14px;
    border-radius: 9999px;
    font-weight: 800;
    font-size: 14px;
    background: #FFFFFF;
    border: 2px solid #EFE7DA;
    box-shadow: 0 3px 0 #E2D7C5;
}
.chip-flame {
    background: #FFF3E6;
    color: #FF7A00;
    border-color: #FFDEBF;
}
.chip-xp {
    background: #FFF8E6;
    color: #DB9900;
    border-color: #FFE699;
}
.chip-heart {
    background: #FFEAEB;
    color: #FF4757;
    border-color: #FFC9CE;
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# Sidebar - Game Settings & Mascot (Only Catch the Flag)
# ==============================================================================
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 6px 0 16px 0;">
        <h2 style="margin: 0; font-weight: 900; font-size: 22px; color: #1E293B;">Catch the Flag! 🚩</h2>
        <p style="margin: 0; color: #64748B; font-weight: 600; font-size: 13px;">Kids Learning Arcade</p>
    </div>
    """, unsafe_allow_html=True)

    # Mascot Selector
    st.markdown("<h4 style='font-weight: 800; font-size: 15px; margin-bottom: 6px;'>🐾 Choose Your Catcher</h4>", unsafe_allow_html=True)
    mascot_choice = st.selectbox(
        "Mascot",
        ["🦁 Leo the Lion", "🐱 Whiskers the Cat", "🐼 Pandy the Panda", "🦊 Rusty the Fox", "🐰 Fluffy Bunny"],
        index=0,
        label_visibility="collapsed"
    )
    mascot_emoji = mascot_choice.split()[0]

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

    # Edition / World Filter
    st.markdown("<h4 style='font-weight: 800; font-size: 15px; margin-bottom: 6px;'>🌍 Choose Edition / World</h4>", unsafe_allow_html=True)
    continent_filter = st.selectbox(
        "Edition",
        [
            "🌍 All World Flags (271 Countries)",
            "🇲🇾 Special Edition: Malaysian States (17 Flags)",
            "🇺🇸 Special Edition: USA States (56 Flags)",
            "🌏 Asia",
            "🏰 Europe",
            "🌎 Americas",
            "🦁 Africa",
            "🏝️ Oceania"
        ],
        index=0,
        label_visibility="collapsed"
    )

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

    # Fall Speed / Difficulty
    st.markdown("<h4 style='font-weight: 800; font-size: 15px; margin-bottom: 6px;'>🎈 Falling Speed</h4>", unsafe_allow_html=True)
    speed_option = st.select_slider(
        "Falling Speed",
        options=["Gentle 🐢", "Normal 🎈", "Fast 🚀"],
        value="Normal 🎈",
        label_visibility="collapsed"
    )
    speed_multipliers = {"Gentle 🐢": 1.2, "Normal 🎈": 1.8, "Fast 🚀": 2.5}
    fall_speed_base = speed_multipliers[speed_option]

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

    # Voice Settings
    st.markdown("<h4 style='font-weight: 800; font-size: 15px; margin-bottom: 6px;'>🔊 Voice Speed</h4>", unsafe_allow_html=True)
    voice_speed = st.slider("Voice Speed", min_value=0.7, max_value=1.2, value=0.9, step=0.05, label_visibility="collapsed")

    st.markdown("<hr style='border: 1px solid #EFE4D6; margin: 16px 0;'>", unsafe_allow_html=True)

    st.markdown("""
    <div style="background: #FFFFFF; border-radius: 18px; padding: 14px; border: 2px solid #EFE4D6; text-align: center;">
        <div style="font-size: 12px; font-weight: 800; color: #64748B; text-transform: uppercase;">🎮 How to Play</div>
        <p style="font-size: 13px; color: #1E293B; font-weight: 600; margin: 6px 0 0 0; line-height: 1.4;">
            1. Look at the <b>FIND &amp; CATCH</b> target flag.<br>
            2. Tap or click the matching falling flag!<br>
            3. Earn <b>+100 points</b>, build combos, and listen to the voice!
        </p>
    </div>
    """, unsafe_allow_html=True)

# Filter country/state pool based on sidebar selection
def get_current_countries():
    if "Malaysian States" in continent_filter:
        return malaysia_data
    elif "USA States" in continent_filter:
        return usa_data
    elif "All World Flags" in continent_filter or continent_filter == "All Worlds":
        return countries_data
    elif "Americas" in continent_filter:
        return [c for c in countries_data if c.get("continent") in ["North America", "South America"]]
    elif "Asia" in continent_filter:
        return [c for c in countries_data if c.get("continent") == "Asia"]
    elif "Europe" in continent_filter:
        return [c for c in countries_data if c.get("continent") == "Europe"]
    elif "Africa" in continent_filter:
        return [c for c in countries_data if c.get("continent") == "Africa"]
    elif "Oceania" in continent_filter:
        return [c for c in countries_data if c.get("continent") == "Oceania"]
    else:
        return [c for c in countries_data if c.get("continent") == continent_filter]

filtered_countries = get_current_countries()
if not filtered_countries:
    filtered_countries = countries_data or []

# ==============================================================================
# MAIN PAGE: Dedicated Catch the Flag Arcade
# ==============================================================================
# Dynamic subtitle and edition badge based on selection
if "Malaysian States" in continent_filter:
    edition_sub = "🇲🇾 Special Edition: Catch the flags of Malaysian States &amp; Federal Territories!"
    edition_badge = "🇲🇾 Malaysia Edition"
elif "USA States" in continent_filter:
    edition_sub = "🇺🇸 Special Edition: Catch the flags of all 50 US States &amp; Territories!"
    edition_badge = "🇺🇸 USA States Edition"
else:
    edition_sub = "Touch or click the falling flag before it reaches the ground!"
    edition_badge = "⭐ Kids Arcade"

st.markdown(f"""
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; flex-wrap: wrap; gap: 8px;">
    <div>
        <h1 style="font-size: 28px; font-weight: 900; margin: 0; color: #1E293B; display: flex; align-items: center; gap: 8px;">
            Catch the Flag! 🚩
        </h1>
        <p style="margin: 0; color: #64748B; font-weight: 600; font-size: 14px;">{edition_sub}</p>
    </div>
    <div style="display: flex; gap: 8px; align-items: center;">
        <div class="kid-chip chip-xp">{edition_badge}</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Pick country subset (up to 70 countries) with flag base64 data
pool = filtered_countries if len(filtered_countries) <= 70 else random.sample(filtered_countries, 70)
country_json_payload = json.dumps(pool)

# The Complete Interactive Falling Flag Game Engine
game_html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700;800;900&display=swap" />
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; user-select: none; -webkit-user-select: none; }}
    body {{ font-family: 'Outfit', sans-serif; background: transparent; overflow: hidden; }}

    .game-viewport {{
      position: relative;
      width: 100%;
      height: 640px;
      border-radius: 28px;
      background: linear-gradient(180deg, #42A5F5 0%, #90CAF9 45%, #E3F2FD 85%, #C8E6C9 100%);
      border: 4px solid #FFFFFF;
      box-shadow: 0 16px 36px rgba(30, 110, 180, 0.22), 0 4px 0 #90CAF9;
      overflow: hidden;
      touch-action: none;
    }}

    /* World Map Background Layer */
    .world-map-bg {{
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100%;
      object-fit: cover;
      opacity: 0.94;
      pointer-events: none;
      z-index: 2;
    }}

    /* Top Mission Header */
    .mission-header {{
      position: absolute;
      top: 14px;
      left: 16px;
      right: 16px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      background: rgba(255, 255, 255, 0.96);
      backdrop-filter: blur(8px);
      padding: 10px 20px;
      border-radius: 9999px;
      border: 2px solid #EFE7DA;
      box-shadow: 0 4px 0 #D5C9B5;
      z-index: 50;
    }}

    .target-group {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}

    .target-flag-card {{
      width: 48px;
      height: 34px;
      border-radius: 8px;
      object-fit: cover;
      box-shadow: 0 3px 8px rgba(0,0,0,0.15);
      border: 2px solid #FFFFFF;
    }}

    .target-text {{
      display: flex;
      flex-direction: column;
    }}

    .target-subtext {{
      font-size: 11px;
      font-weight: 800;
      color: #8C52FF;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }}

    .target-name {{
      font-size: 22px;
      font-weight: 900;
      color: #FF7A00;
      line-height: 1.1;
    }}

    .mission-actions {{
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    .btn-audio-speak {{
      background: #2DA8FF;
      color: #FFFFFF;
      border: none;
      padding: 9px 18px;
      border-radius: 9999px;
      font-weight: 800;
      font-size: 14px;
      cursor: pointer;
      box-shadow: 0 4px 0 #0D8FE8;
      display: flex;
      align-items: center;
      gap: 6px;
      transition: all 0.1s ease;
    }}
    .btn-audio-speak:active {{
      transform: translateY(2px);
      box-shadow: 0 2px 0 #0D8FE8;
    }}

    .btn-pause {{
      background: #FFB800;
      color: #FFFFFF;
      border: none;
      padding: 9px 16px;
      border-radius: 9999px;
      font-weight: 800;
      font-size: 14px;
      cursor: pointer;
      box-shadow: 0 4px 0 #DB9900;
      display: flex;
      align-items: center;
      gap: 6px;
      transition: all 0.1s ease;
    }}
    .btn-pause:active {{
      transform: translateY(2px);
      box-shadow: 0 2px 0 #DB9900;
    }}

    /* Score & Combo HUD */
    .hud-stats {{
      position: absolute;
      top: 76px;
      left: 20px;
      display: flex;
      gap: 10px;
      z-index: 45;
    }}

    /* Start Audio Prompt Badge */
    .start-audio-prompt {{
      position: absolute;
      top: 76px;
      right: 20px;
      background: #FFFFFF;
      border: 2px solid #FF7A00;
      border-radius: 9999px;
      padding: 6px 16px;
      font-size: 13px;
      font-weight: 800;
      color: #FF7A00;
      box-shadow: 0 4px 10px rgba(255, 122, 0, 0.2);
      z-index: 60;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      animation: pulseBanner 1.8s infinite ease-in-out;
      transition: all 0.3s ease;
    }}
    .start-audio-prompt.dismissed {{
      opacity: 0;
      pointer-events: none;
      transform: translateY(-10px);
    }}
    @keyframes pulseBanner {{
      0%, 100% {{ transform: scale(1); }}
      50% {{ transform: scale(1.05); }}
    }}

    .score-badge {{
      background: #FFFFFF;
      border: 2px solid #FFE699;
      border-radius: 9999px;
      padding: 6px 16px;
      font-size: 17px;
      font-weight: 900;
      color: #D69E00;
      box-shadow: 0 3px 0 #E2D7C5;
      display: flex;
      align-items: center;
      gap: 6px;
      transition: transform 0.15s ease;
    }}

    .combo-badge {{
      background: #FFF3E6;
      border: 2px solid #FFDEBF;
      border-radius: 9999px;
      padding: 6px 14px;
      font-size: 14px;
      font-weight: 900;
      color: #FF7A00;
      box-shadow: 0 3px 0 #E2D7C5;
      opacity: 0;
      transform: scale(0.8);
      transition: all 0.2s ease;
    }}
    .combo-badge.active {{
      opacity: 1;
      transform: scale(1);
    }}

    /* Drifting Clouds in Sky */
    .cloud {{
      position: absolute;
      background: rgba(255, 255, 255, 0.88);
      border-radius: 100px;
      pointer-events: none;
      filter: drop-shadow(0 6px 12px rgba(45, 120, 190, 0.12));
    }}

    /* FALLING FLAGS: Pure 3D Squishy Kids UI Style */
    .falling-flag {{
      position: absolute;
      top: 0;
      left: 0;
      cursor: pointer;
      display: flex;
      flex-direction: column;
      align-items: center;
      touch-action: manipulation;
      z-index: 25;
      will-change: transform;
    }}

    /* Parachute / Balloon on top of flag */
    .flag-parachute {{
      font-size: 22px;
      margin-bottom: -6px;
      filter: drop-shadow(0 3px 4px rgba(0,0,0,0.15));
      pointer-events: none;
      animation: swayChute 2s ease-in-out infinite alternate;
    }}

    .flag-box {{
      width: 104px;
      height: 74px;
      border-radius: 18px;
      background-color: #FFFFFF;
      padding: 4px;
      box-shadow: 0 12px 26px rgba(0, 40, 90, 0.22), 0 4px 0 #D5C9B5;
      border: 3px solid #FFFFFF;
      overflow: hidden;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: transform 0.1s ease;
    }}

    .flag-box:hover {{
      transform: scale(1.08);
      border-color: #FFD54F;
      box-shadow: 0 16px 30px rgba(255, 180, 0, 0.35), 0 4px 0 #FFB300;
    }}

    .flag-box:active {{
      transform: scale(0.95);
    }}

    .flag-img {{
      width: 100%;
      height: 100%;
      object-fit: cover;
      border-radius: 12px;
      pointer-events: none;
    }}

    .flag-name-tag {{
      background: #FFFFFF;
      padding: 3px 12px;
      border-radius: 9999px;
      font-size: 12px;
      font-weight: 800;
      color: #1E293B;
      box-shadow: 0 3px 8px rgba(0,0,0,0.12);
      border: 1.5px solid #EFE7DA;
      margin-top: 4px;
      white-space: nowrap;
      pointer-events: none;
    }}

    /* Mascot at the Bottom */
    #mascot-catcher {{
      position: absolute;
      bottom: 12px;
      left: 50%;
      transform: translateX(-50%);
      width: 90px;
      height: 85px;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      pointer-events: none;
      z-index: 35;
      transition: transform 0.08s ease-out;
    }}

    .mascot-avatar {{
      width: 66px;
      height: 66px;
      background: #FFFFFF;
      border: 3px solid #FFFFFF;
      border-radius: 50%;
      box-shadow: 0 8px 18px rgba(0,0,0,0.2), 0 4px 0 #D5C9B5;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 38px;
    }}

    .mascot-basket {{
      font-size: 26px;
      margin-top: -12px;
      filter: drop-shadow(0 3px 4px rgba(0,0,0,0.2));
    }}

    /* Confetti Canvas */
    #confetti-canvas {{
      position: absolute;
      inset: 0;
      pointer-events: none;
      z-index: 40;
    }}

    /* Floating Feedback Text */
    .floating-text {{
      position: absolute;
      font-weight: 900;
      font-size: 22px;
      pointer-events: none;
      z-index: 60;
      transition: transform 0.8s ease-out, opacity 0.8s ease-out;
      text-shadow: 0 2px 6px rgba(255,255,255,0.9);
    }}

    /* Bottom Level Bar */
    .level-strip {{
      position: absolute;
      bottom: 14px;
      right: 18px;
      background: rgba(255, 255, 255, 0.95);
      backdrop-filter: blur(8px);
      padding: 7px 18px;
      border-radius: 9999px;
      border: 2px solid #EFE7DA;
      box-shadow: 0 3px 0 #D5C9B5;
      display: flex;
      align-items: center;
      gap: 10px;
      z-index: 45;
    }}

    .prog-track {{
      width: 130px;
      height: 12px;
      background: #E8E2D5;
      border-radius: 9999px;
      overflow: hidden;
      padding: 2px;
    }}

    .prog-fill {{
      height: 100%;
      background: linear-gradient(90deg, #FF7A00, #FFC700);
      border-radius: 9999px;
      width: 20%;
      transition: width 0.3s ease;
    }}

    /* Modal for Level Win */
    .celebrate-modal {{
      position: absolute;
      inset: 0;
      background: rgba(20, 30, 45, 0.5);
      backdrop-filter: blur(6px);
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 100;
      opacity: 0;
      pointer-events: none;
      transition: opacity 0.25s ease;
    }}
    .celebrate-modal.active {{
      opacity: 1;
      pointer-events: auto;
    }}

    .celebrate-card {{
      background: #FFFFFF;
      border-radius: 32px;
      border: 3px solid #EFE7DA;
      box-shadow: 0 24px 60px rgba(0, 0, 0, 0.25), 0 6px 0 #D5C9B5;
      width: 90%;
      max-width: 400px;
      padding: 28px 20px;
      text-align: center;
      transform: scale(0.85);
      transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }}
    .celebrate-modal.active .celebrate-card {{
      transform: scale(1);
    }}

    @keyframes bounceTrophy {{
      0% {{ transform: translateY(0) scale(1); }}
      100% {{ transform: translateY(-10px) scale(1.08); }}
    }}

    /* Pause Screen Overlay */
    .pause-overlay {{
      position: absolute;
      inset: 0;
      background: rgba(20, 30, 45, 0.55);
      backdrop-filter: blur(8px);
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 95;
      opacity: 0;
      pointer-events: none;
      transition: opacity 0.25s ease;
    }}
    .pause-overlay.active {{
      opacity: 1;
      pointer-events: auto;
    }}

    .pause-card {{
      background: #FFFFFF;
      border-radius: 32px;
      border: 3px solid #EFE7DA;
      box-shadow: 0 24px 60px rgba(0, 0, 0, 0.25), 0 6px 0 #D5C9B5;
      width: 90%;
      max-width: 380px;
      padding: 30px 24px;
      text-align: center;
      transform: scale(0.85);
      transition: transform 0.25s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }}
    .pause-overlay.active .pause-card {{
      transform: scale(1);
    }}

    .btn-resume {{
      background: #58CC02;
      color: #FFFFFF;
      border: none;
      border-radius: 9999px;
      font-weight: 800;
      font-size: 18px;
      padding: 14px 34px;
      cursor: pointer;
      box-shadow: 0 5px 0 #429E00;
      display: inline-flex;
      align-items: center;
      gap: 8px;
      transition: all 0.1s ease;
    }}
    .btn-resume:active {{
      transform: translateY(3px);
      box-shadow: 0 2px 0 #429E00;
    }}

    @keyframes swayChute {{
      0% {{ transform: rotate(-8deg); }}
      100% {{ transform: rotate(8deg); }}
    }}

    @keyframes catchPop {{
      0% {{ transform: scale(1); opacity: 1; }}
      50% {{ transform: scale(1.4) rotate(10deg); opacity: 1; }}
      100% {{ transform: scale(0) rotate(-15deg); opacity: 0; }}
    }}
  </style>
</head>
<body>
  <div class="game-viewport" id="viewport">
    
    <!-- World Map Background (Matching Kids Games UI Color Profile) -->
    <img src="{world_map_uri}" class="world-map-bg" alt="Kids World Map" />

    <!-- Top Mission Target -->
    <div class="mission-header">
      <div class="target-group" id="target-click-box" style="cursor: pointer;" title="Tap to hear target country!">
        <img id="target-img" class="target-flag-card" src="" alt="Target" />
        <div class="target-text">
          <span class="target-subtext">FIND &amp; CATCH</span>
          <span class="target-name" id="target-title">Loading...</span>
        </div>
      </div>
      <div class="mission-actions">
        <button class="btn-audio-speak" id="btn-hear-target" title="Hear Target Country">
          <span>🔊 Say Target</span>
        </button>
        <button class="btn-pause" id="btn-pause" title="Pause Game">
          <span id="pause-btn-label">⏸️ Pause</span>
        </button>
      </div>
    </div>

    <!-- HUD Score, Level & Combo -->
    <div class="hud-stats">
      <div class="score-badge" id="score-badge">
        <span>⭐</span> <span id="score-num">0</span> PTS
      </div>
      <div class="score-badge" id="hud-level-badge" style="border-color: #D8B4FE; color: #7E22CE; background: #FAF5FF; padding: 6px 14px;">
        <span>🚀</span> <span id="hud-level-num">Level 1</span>
      </div>
      <div class="combo-badge" id="combo-badge">
        🔥 <span id="combo-num">2</span>x COMBO!
      </div>
    </div>

    <!-- Tap to Start Audio Banner -->
    <div id="start-audio-prompt" class="start-audio-prompt" title="Tap to start voice audio!">
      <span>🔊 Tap to Hear Target!</span>
    </div>

    <!-- Confetti Canvas -->
    <canvas id="confetti-canvas"></canvas>

    <!-- Pilot Mascot with Catch Basket -->
    <div id="mascot-catcher">
      <div class="mascot-avatar">{mascot_emoji}</div>
      <div class="mascot-basket">🧺</div>
    </div>

    <!-- Bottom Progress Strip -->
    <div class="level-strip">
      <span style="font-size: 13px; font-weight: 800; color: #8C52FF;" id="level-title-label">Level 1: Novice Explorer</span>
      <div class="prog-track">
        <div class="prog-fill" id="prog-fill" style="width: 0%;"></div>
      </div>
      <span style="font-size: 12px; font-weight: 800; color: #64748B;" id="catches-num">0/5</span>
    </div>

    <!-- Level Complete Celebration Modal (Intermediate Levels) -->
    <div class="celebrate-modal" id="win-modal">
      <div class="celebrate-card">
        <div style="font-size: 60px; margin-bottom: 8px;">🌟</div>
        <h2 style="font-size: 26px; font-weight: 900; color: #1E293B; margin-bottom: 6px;" id="level-win-title">Level Complete!</h2>
        <p style="font-size: 15px; color: #64748B; font-weight: 600; margin-bottom: 18px;" id="level-win-desc">
          You caught 5 flags like a champion aviator!
        </p>
        <button id="btn-next-level" style="background: #FF7A00; color: #FFF; border: none; border-radius: 9999px; font-weight: 800; font-size: 17px; padding: 13px 32px; cursor: pointer; box-shadow: 0 4px 0 #E26400;">
          Play Next Level 🚀
        </button>
      </div>
    </div>

    <!-- Game Won Grand Celebration Modal (Level 5 Completed) -->
    <div class="celebrate-modal" id="game-won-modal">
      <div class="celebrate-card" style="max-width: 440px; padding: 32px 24px;">
        <div style="font-size: 70px; margin-bottom: 6px; display: inline-block; animation: bounceTrophy 0.9s infinite alternate ease-in-out;">🏆</div>
        <h2 style="font-size: 28px; font-weight: 900; color: #1E293B; margin-bottom: 4px;">CONGRATULATIONS!</h2>
        <div style="font-size: 15px; font-weight: 800; color: #8C52FF; margin-bottom: 14px; letter-spacing: 0.5px;">
          👑 YOU WON THE GAME! 👑
        </div>
        <p style="font-size: 14px; color: #475569; font-weight: 600; line-height: 1.5; margin-bottom: 16px;">
          Superstar! You completed all 5 levels and caught flags from around the globe!
        </p>
        <div style="background: linear-gradient(135deg, #FFF6E5 0%, #FFE9B8 100%); border: 3px solid #FFD066; border-radius: 20px; padding: 14px 20px; margin-bottom: 20px; box-shadow: 0 4px 14px rgba(255, 184, 0, 0.25);">
          <div style="font-size: 12px; font-weight: 800; color: #B38600; text-transform: uppercase; letter-spacing: 1px;">FINAL SCORE</div>
          <div style="font-size: 40px; font-weight: 900; color: #FF7A00; line-height: 1.1; margin: 4px 0;">
            <span id="final-score-val">0</span> <span style="font-size: 20px;">PTS ⭐</span>
          </div>
          <div style="font-size: 13px; font-weight: 700; color: #64748B;">
            All 5 Levels Completed • Flag Master Champion!
          </div>
        </div>
        <button id="btn-play-again" style="background: linear-gradient(135deg, #58CC02 0%, #46A302 100%); color: #FFF; border: none; border-radius: 9999px; font-weight: 900; font-size: 18px; padding: 14px 34px; cursor: pointer; box-shadow: 0 5px 0 #327A00;">
          Play Again 🔄
        </button>
      </div>
    </div>

    <!-- Pause Screen Overlay -->
    <div class="pause-overlay" id="pause-overlay">
      <div class="pause-card">
        <div style="font-size: 52px; margin-bottom: 8px;">⏸️</div>
        <h2 style="font-size: 26px; font-weight: 900; color: #1E293B; margin-bottom: 6px;">Game Paused</h2>
        <p style="font-size: 15px; color: #64748B; font-weight: 600; margin-bottom: 20px;">
          Take a breath! When you're ready, let's catch more flags!
        </p>
        <button id="btn-resume" class="btn-resume">
          ▶️ Resume Playing
        </button>
      </div>
    </div>

  </div>

  <script>
    const countries = {country_json_payload};
    const speechRate = {voice_speed};
    const fallBase = {fall_speed_base};

    const viewport = document.getElementById('viewport');
    const targetTitle = document.getElementById('target-title');
    const targetImg = document.getElementById('target-img');
    const scoreNum = document.getElementById('score-num');
    const scoreBadge = document.getElementById('score-badge');
    const comboBadge = document.getElementById('combo-badge');
    const progFill = document.getElementById('prog-fill');
    const catchesNum = document.getElementById('catches-num');
    const mascot = document.getElementById('mascot-catcher');
    const winModal = document.getElementById('win-modal');
    const btnNextLevel = document.getElementById('btn-next-level');

    // Confetti canvas setup
    const canvas = document.getElementById('confetti-canvas');
    const ctx = canvas.getContext('2d');
    function resizeCanvas() {{
      canvas.width = viewport.clientWidth || 800;
      canvas.height = viewport.clientHeight || 640;
    }}
    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);

    // Level progression targets:
    // Level 1: 5 catches to reach Level 2
    // Level 2: 10 catches to reach Level 3
    // Level 3: 20 catches to reach Level 4
    // Level 4: 30 catches to reach Level 5
    // Level 5: 50 catches to WIN THE GAME!
    const LEVEL_CONFIG = {{
      1: {{ target: 5, title: 'Novice Explorer' }},
      2: {{ target: 10, title: 'Sky Adventurer' }},
      3: {{ target: 20, title: 'Globe Trotter' }},
      4: {{ target: 30, title: 'Flag Master' }},
      5: {{ target: 50, title: 'Grand Aviator' }}
    }};
    const MAX_LEVEL = 5;

    let targetCountry = null;
    let score = 0;
    let combo = 0;
    let currentLevel = 1;
    let catchesInLevel = 0;
    let activeFlags = [];
    let confettiParticles = [];
    let mascotX = (viewport.clientWidth || 800) / 2;

    function updateLevelUI() {{
      const cfg = LEVEL_CONFIG[currentLevel] || {{ target: 50, title: 'Champion' }};
      const targetCatches = cfg.target;

      const hudLvl = document.getElementById('hud-level-num');
      if (hudLvl) hudLvl.textContent = `Level ${{currentLevel}}`;

      const titleLabel = document.getElementById('level-title-label');
      if (titleLabel) titleLabel.textContent = `Level ${{currentLevel}}: ${{cfg.title}}`;

      catchesNum.textContent = `${{catchesInLevel}}/${{targetCatches}}`;
      const pct = Math.min(100, (catchesInLevel / targetCatches) * 100);
      progFill.style.width = `${{pct}}%`;
    }}

    // Web Audio Synthesizer
    let audioCtx = null;
    function playTone(freq, type = 'sine', duration = 0.2) {{
      try {{
        if (!audioCtx) {{
          const AudioContext = window.AudioContext || window.webkitAudioContext;
          audioCtx = new AudioContext();
        }}
        if (audioCtx.state === 'suspended') audioCtx.resume();
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.type = type;
        osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
        gain.gain.setValueAtTime(0.28, audioCtx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.0001, audioCtx.currentTime + duration);
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.start();
        osc.stop(audioCtx.currentTime + duration);
      }} catch (e) {{}}
    }}

    function playCatchSuccess() {{
      playTone(523.25, 'triangle', 0.15); // C5
      setTimeout(() => playTone(659.25, 'triangle', 0.15), 70); // E5
      setTimeout(() => playTone(783.99, 'triangle', 0.25), 140); // G5
      setTimeout(() => playTone(1046.5, 'sine', 0.35), 210); // C6
    }}

    function playLevelUpFanfare() {{
      playTone(523.25, 'triangle', 0.18);
      setTimeout(() => playTone(659.25, 'triangle', 0.18), 90);
      setTimeout(() => playTone(783.99, 'triangle', 0.18), 180);
      setTimeout(() => playTone(1046.5, 'triangle', 0.35), 270);
      setTimeout(() => playTone(1318.5, 'sine', 0.45), 400);
    }}

    function playGrandFanfare() {{
      const notes = [523.25, 659.25, 783.99, 1046.5, 1318.5, 1567.98];
      notes.forEach((freq, idx) => {{
        setTimeout(() => playTone(freq, 'triangle', 0.25), idx * 80);
      }});
      setTimeout(() => {{
        playTone(1046.5, 'sine', 0.7);
        playTone(1318.5, 'sine', 0.7);
        playTone(1567.98, 'sine', 0.7);
      }}, notes.length * 80 + 40);
    }}

    function playMissSound() {{
      playTone(330, 'sawtooth', 0.15);
      setTimeout(() => playTone(260, 'sawtooth', 0.25), 100);
    }}

    let voices = [];
    function loadVoices() {{
      if ('speechSynthesis' in window) {{
        voices = window.speechSynthesis.getVoices();
      }}
    }}
    loadVoices();
    if ('speechSynthesis' in window && 'onvoiceschanged' in window.speechSynthesis) {{
      window.speechSynthesis.onvoiceschanged = loadVoices;
    }}

    window.activeUtterance = null;
    let activeAudio = null;

    function announceTarget() {{
      if (!targetCountry) return;
      speak(`Catch the flag of ${{targetCountry.name}}!`);
    }}

    function speak(text) {{
      // Play a quick soft cheerful chime first
      playTone(587.33, 'triangle', 0.12);

      // Stop any prior audio
      if (activeAudio) {{
        try {{ activeAudio.pause(); activeAudio.currentTime = 0; }} catch(e) {{}}
      }}

      let html5Played = false;
      try {{
        const url = 'https://translate.google.com/translate_tts?ie=UTF-8&tl=en&client=tw-ob&q=' + encodeURIComponent(text);
        activeAudio = new Audio(url);
        const p = activeAudio.play();
        if (p !== undefined) {{
          p.then(() => {{
            html5Played = true;
          }}).catch(e => {{
            fallbackSpeech(text);
          }});
        }}
      }} catch (e) {{
        fallbackSpeech(text);
      }}

      // Safety timeout: if HTML5 audio didn't start in 400ms, fallback to browser speech
      setTimeout(() => {{
        if (!html5Played) {{
          fallbackSpeech(text);
        }}
      }}, 400);
    }}

    function fallbackSpeech(text) {{
      if (!('speechSynthesis' in window)) return;
      try {{
        window.speechSynthesis.cancel();
        setTimeout(() => {{
          window.speechSynthesis.resume();
          const ut = new SpeechSynthesisUtterance(text);
          ut.rate = speechRate || 0.9;
          ut.pitch = 1.15;
          ut.lang = 'en-US';

          if (!voices.length) loadVoices();
          const preferred = voices.find(v => 
            v.lang.startsWith('en') && (v.name.includes('Samantha') || v.name.includes('Victoria') || v.name.includes('Google') || v.name.includes('Natural'))
          ) || voices.find(v => v.lang.startsWith('en'));
          if (preferred) ut.voice = preferred;

          window.activeUtterance = ut;
          window.speechSynthesis.speak(ut);
        }}, 60);
      }} catch (err) {{}}
    }}

    function pickNewTarget() {{
      if (!countries.length) return;
      targetCountry = countries[Math.floor(Math.random() * countries.length)];
      targetTitle.textContent = targetCountry.name;
      targetImg.src = targetCountry.flag_data;
      announceTarget();
    }}

    // Spawn 4 decorative fluffy clouds floating gently above the map
    for (let i = 0; i < 4; i++) {{
      const c = document.createElement('div');
      c.className = 'cloud';
      c.style.width = `${{110 + Math.random() * 70}}px`;
      c.style.height = `${{45 + Math.random() * 20}}px`;
      c.style.top = `${{70 + Math.random() * 220}}px`;
      c.style.left = `${{Math.random() * 80}}%`;
      c.style.opacity = (0.35 + Math.random() * 0.25).toFixed(2);
      c.style.zIndex = '8';
      viewport.appendChild(c);
    }}

    // Confetti explosion
    function explodeConfetti(x, y) {{
      const colors = ['#FF7A00', '#2DA8FF', '#58CC02', '#FFB800', '#FF4757', '#8C52FF'];
      for (let i = 0; i < 35; i++) {{
        const angle = Math.random() * Math.PI * 2;
        const speed = 3 + Math.random() * 6;
        confettiParticles.push({{
          x: x,
          y: y,
          vx: Math.cos(angle) * speed,
          vy: Math.sin(angle) * speed - 2,
          color: colors[Math.floor(Math.random() * colors.length)],
          size: 5 + Math.random() * 6,
          life: 1.0,
          decay: 0.02 + Math.random() * 0.02
        }});
      }}
    }}

    // Floating text particle (+100 PTS ⭐)
    function spawnFloatingText(text, x, y, color = '#FF7A00') {{
      const el = document.createElement('div');
      el.className = 'floating-text';
      el.textContent = text;
      el.style.left = `${{x}}px`;
      el.style.top = `${{y}}px`;
      el.style.color = color;
      viewport.appendChild(el);

      requestAnimationFrame(() => {{
        el.style.transform = 'translateY(-55px) scale(1.15)';
        el.style.opacity = '0';
      }});

      setTimeout(() => el.remove(), 800);
    }}

    // SPAWN A FALLING FLAG (Drops from the top!)
    function spawnFallingFlag() {{
      if (!countries.length) return;

      const vpWidth = viewport.clientWidth || 800;

      // 45% chance to drop target country to keep missions fun
      let country;
      if (targetCountry && Math.random() < 0.45) {{
        country = targetCountry;
      }} else {{
        country = countries[Math.floor(Math.random() * countries.length)];
      }}

      const el = document.createElement('div');
      el.className = 'falling-flag';
      el.innerHTML = `
        <div class="flag-parachute">🎈</div>
        <div class="flag-box">
          <img class="flag-img" src="${{country.flag_data}}" alt="${{country.name}}" />
        </div>
        <span class="flag-name-tag">${{country.name}}</span>
      `;

      // Random X column across the sky width
      const startX = 30 + Math.random() * (vpWidth - 170);
      const startY = -110; // start above top of sky

      const flagObj = {{
        el: el,
        country: country,
        x: startX,
        baseX: startX,
        y: startY,
        speed: fallBase + (currentLevel - 1) * 0.18 + (Math.random() * 0.6 - 0.3),
        seed: Math.random() * 100,
        caught: false
      }};

      // Instant Catch Handler (Touch or Click anywhere on the falling flag)
      const catchHandler = (e) => {{
        e.stopPropagation();
        if (flagObj.caught) return;
        flagObj.caught = true;

        handleCatch(flagObj, e.clientX || flagObj.x, e.clientY || flagObj.y);
      }};

      el.addEventListener('pointerdown', catchHandler);
      el.addEventListener('click', catchHandler);

      viewport.appendChild(el);
      activeFlags.push(flagObj);
    }}

    function handleCatch(flagObj, clickX, clickY) {{
      const country = flagObj.country;

      // Say country flag name aloud!
      speak(country.name);

      // Pop burst animation
      flagObj.el.style.animation = 'catchPop 0.35s forwards cubic-bezier(0.175, 0.885, 0.32, 1.275)';
      setTimeout(() => {{
        flagObj.el.remove();
        activeFlags = activeFlags.filter(f => f !== flagObj);
      }}, 350);

      // Check if matches the target country!
      if (targetCountry && country.code === targetCountry.code) {{
        // CORRECT FLAG!
        combo++;
        const points = 100 + (combo > 1 ? (combo - 1) * 50 : 0);
        score += points;

        // Visual fanfare & sound
        playCatchSuccess();
        explodeConfetti(flagObj.x + 50, flagObj.y + 40);

        // Floating text
        const comboMsg = combo > 1 ? `+${{points}} (x${{combo}} 🔥)` : `+${{points}} ⭐`;
        spawnFloatingText(comboMsg, flagObj.x + 10, flagObj.y, '#58CC02');

        // Update score HUD
        scoreNum.textContent = score;
        scoreBadge.style.transform = 'scale(1.2)';
        setTimeout(() => {{ scoreBadge.style.transform = 'scale(1)'; }}, 200);

        // Update combo badge
        if (combo > 1) {{
          comboBadge.textContent = `🔥 ${{combo}}x COMBO!`;
          comboBadge.classList.add('active');
        }}

        // Advance level progress
        catchesInLevel++;
        const currentTarget = LEVEL_CONFIG[currentLevel]?.target || 50;
        updateLevelUI();

        if (catchesInLevel >= currentTarget) {{
          if (currentLevel < MAX_LEVEL) {{
            // Level Completed! Advance to next level modal
            setTimeout(() => {{
              showLevelCompleteModal();
            }}, 400);
          }} else {{
            // LEVEL 5 COMPLETED: WIN THE GAME!
            setTimeout(() => {{
              showGameWonModal();
            }}, 400);
          }}
        }} else {{
          // Pick next target after short pause
          setTimeout(pickNewTarget, 600);
        }}

      }} else {{
        // WRONG FLAG: gentle educational cue
        combo = 0;
        comboBadge.classList.remove('active');
        playMissSound();
        spawnFloatingText(`That was ${{country.name}}!`, flagObj.x - 10, flagObj.y, '#FF4757');
        speak(`That's ${{country.name}}! Find ${{targetCountry.name}}!`);
      }}
    }}

    function showLevelCompleteModal() {{
      playLevelUpFanfare();
      explodeConfetti(viewport.clientWidth / 2, viewport.clientHeight / 2);

      const nextLevel = currentLevel + 1;
      const nextTarget = LEVEL_CONFIG[nextLevel]?.target || 10;
      const currentTarget = LEVEL_CONFIG[currentLevel]?.target || 5;

      const titleEl = document.getElementById('level-win-title');
      const descEl = document.getElementById('level-win-desc');
      if (titleEl) titleEl.textContent = `🎉 Level ${{currentLevel}} Complete!`;
      if (descEl) descEl.innerHTML = `You caught <b>${{currentTarget}} flags</b> like a champion aviator!<br>Current Score: <b style="color: #FF7A00;">${{score}} PTS</b> ⭐<br><br>Ready for <b>Level ${{nextLevel}}</b>? Catch <b>${{nextTarget}} flags</b> to advance!`;

      btnNextLevel.textContent = `Play Level ${{nextLevel}} 🚀`;
      winModal.classList.add('active');

      speak(`Level ${{currentLevel}} complete! Fantastic job! Get ready for Level ${{nextLevel}}!`);
    }}

    // Next level button
    btnNextLevel.addEventListener('click', () => {{
      winModal.classList.remove('active');
      currentLevel++;
      catchesInLevel = 0;
      updateLevelUI();

      // Clear remaining active flags for fresh level start
      activeFlags.forEach(f => f.el.remove());
      activeFlags = [];

      speak(`Welcome to Level ${{currentLevel}}! Catch ${{LEVEL_CONFIG[currentLevel]?.target}} flags!`);
      setTimeout(pickNewTarget, 600);
    }});

    function showGameWonModal() {{
      playGrandFanfare();
      // Multi-burst confetti celebration
      for (let i = 0; i < 6; i++) {{
        setTimeout(() => {{
          explodeConfetti(viewport.clientWidth * (0.15 + i * 0.14), viewport.clientHeight * 0.4);
        }}, i * 220);
      }}

      const finalScoreEl = document.getElementById('final-score-val');
      if (finalScoreEl) finalScoreEl.textContent = score;

      const wonModal = document.getElementById('game-won-modal');
      if (wonModal) wonModal.classList.add('active');

      speak(`Congratulations! You won the game with ${{score}} points! You are the grand champion!`);
    }}

    const btnPlayAgain = document.getElementById('btn-play-again');
    if (btnPlayAgain) {{
      btnPlayAgain.addEventListener('click', () => {{
        const wonModal = document.getElementById('game-won-modal');
        if (wonModal) wonModal.classList.remove('active');

        // Reset game to Level 1
        currentLevel = 1;
        catchesInLevel = 0;
        score = 0;
        combo = 0;
        scoreNum.textContent = '0';
        updateLevelUI();

        activeFlags.forEach(f => f.el.remove());
        activeFlags = [];

        speak(`Welcome back! Let's play Level 1!`);
        setTimeout(pickNewTarget, 600);
      }});
    }}

    // Audio Announcement & Interaction Unlock
    let hasInteracted = false;
    function onFirstInteraction() {{
      const promptBadge = document.getElementById('start-audio-prompt');
      if (promptBadge) promptBadge.classList.add('dismissed');

      if (audioCtx && audioCtx.state === 'suspended') audioCtx.resume();
      if ('speechSynthesis' in window) window.speechSynthesis.resume();

      if (!hasInteracted) {{
        hasInteracted = true;
        announceTarget();
      }}
    }}
    viewport.addEventListener('pointerdown', onFirstInteraction);
    document.addEventListener('pointerdown', onFirstInteraction);
    document.addEventListener('click', onFirstInteraction);

    const startBadge = document.getElementById('start-audio-prompt');
    if (startBadge) {{
      startBadge.addEventListener('click', (e) => {{
        e.stopPropagation();
        onFirstInteraction();
        announceTarget();
      }});
    }}

    // Hear target audio prompt
    document.getElementById('btn-hear-target').addEventListener('click', (e) => {{
      e.stopPropagation();
      onFirstInteraction();
      announceTarget();
    }});

    const targetClickBox = document.getElementById('target-click-box');
    if (targetClickBox) {{
      targetClickBox.addEventListener('click', (e) => {{
        e.stopPropagation();
        onFirstInteraction();
        announceTarget();
      }});
    }}

    // Pause & Resume Functionality
    let isPaused = false;
    const pauseOverlay = document.getElementById('pause-overlay');
    const pauseBtnLabel = document.getElementById('pause-btn-label');
    const btnResume = document.getElementById('btn-resume');

    function togglePause() {{
      isPaused = !isPaused;
      if (isPaused) {{
        pauseOverlay.classList.add('active');
        pauseBtnLabel.textContent = '▶️ Resume';
        playTone(350, 'sine', 0.15);
        speak('Game paused');
      }} else {{
        pauseOverlay.classList.remove('active');
        pauseBtnLabel.textContent = '⏸️ Pause';
        playTone(550, 'sine', 0.15);
        announceTarget();
      }}
    }}

    document.getElementById('btn-pause').addEventListener('click', (e) => {{
      e.stopPropagation();
      togglePause();
    }});

    btnResume.addEventListener('click', (e) => {{
      e.stopPropagation();
      togglePause();
    }});

    window.addEventListener('keydown', (e) => {{
      if (e.code === 'Space') {{
        e.preventDefault();
        togglePause();
      }}
    }});

    // Mascot tracks cursor / touch horizontally across bottom
    viewport.addEventListener('pointermove', (e) => {{
      const rect = viewport.getBoundingClientRect();
      mascotX = Math.max(50, Math.min(rect.width - 50, e.clientX - rect.left));
      mascot.style.transform = `translateX(${{mascotX - 45}}px)`;
    }});

    updateLevelUI();
    pickNewTarget();

    // MAIN GAME LOOP (Falls downwards with gentle swaying)
    let lastSpawnTime = 0;
    function gameLoop(timestamp) {{
      if (isPaused) {{
        requestAnimationFrame(gameLoop);
        return;
      }}
      const vpWidth = viewport.clientWidth || 800;
      const vpHeight = viewport.clientHeight || 640;

      // Spawn a new falling flag every 1.8 seconds
      if (timestamp - lastSpawnTime > 1800) {{
        if (activeFlags.length < 5) {{
          spawnFallingFlag();
        }}
        lastSpawnTime = timestamp;
      }}

      // Move falling flags downwards
      for (let i = activeFlags.length - 1; i >= 0; i--) {{
        const f = activeFlags[i];
        if (f.caught) continue;

        f.y += f.speed; // Fall down!
        const sway = Math.sin((timestamp / 450) + f.seed) * 16;
        const currentX = f.baseX + sway;

        f.x = currentX;
        f.el.style.transform = `translate3d(${{currentX}}px, ${{f.y}}px, 0)`;

        // Check Mascot Catch zone near bottom!
        if (f.y >= vpHeight - 120 && f.y <= vpHeight - 40) {{
          if (Math.abs((currentX + 50) - mascotX) < 55) {{
            f.caught = true;
            handleCatch(f, currentX, f.y);
            continue;
          }}
        }}

        // If fell past bottom of sky
        if (f.y > vpHeight + 30) {{
          f.el.remove();
          activeFlags.splice(i, 1);
        }}
      }}

      // Render confetti
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      for (let i = confettiParticles.length - 1; i >= 0; i--) {{
        const p = confettiParticles[i];
        p.x += p.vx;
        p.y += p.vy;
        p.vy += 0.15; // gravity
        p.life -= p.decay;

        ctx.fillStyle = p.color;
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
        ctx.fill();

        if (p.life <= 0) {{
          confettiParticles.splice(i, 1);
        }}
      }}

      requestAnimationFrame(gameLoop);
    }}

    requestAnimationFrame(gameLoop);
  </script>
</body>
</html>
"""

# Render full screen interactive game
components.html(game_html, height=660)
