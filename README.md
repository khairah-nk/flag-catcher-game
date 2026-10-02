# 🚩 Catch the Flag! - Kids World Geography Learning Game

A responsive, cheerful, multi-sensory educational game designed for children (ages 4–10) inspired by the **Kids Games Mobile UI Kit** from Figma.

Children watch world flags drift gently across an animated sky. When a flag is touched or clicked, the game **speaks the country's name aloud** using natural speech synthesis, pops up tactile 3D micro-animations, and displays country details (capital, continent, and fun facts).

---

## 🌟 What We Built & Delivered

### 1. Product Requirements Document (PRD)
- Full documentation in [PRD.md](file:///Users/khairahn/Documents/flag-flying-game/PRD.md).
- Covers Target Personas, Core Gameplay Loop, Flying Flag Physics, Web Speech Synthesis Voice Architecture, Web Audio Synthesizer, 3 Game Modes (Mission Quest, Free Explorer, Continent Safari), Gamification (Streaks, XP, Hearts, Badges), and COPPA kid-safety standards.

### 2. Color Profile & UI Kit
- Full specification in [DESIGN_SYSTEM.md](file:///Users/khairahn/Documents/flag-flying-game/DESIGN_SYSTEM.md).
- Reusable CSS tokens and components in [ui-kit.css](file:///Users/khairahn/Documents/flag-flying-game/ui-kit.css).
- Features:
  - **Color Tokens**: Tangerine Orange (`#FF7A00`), Azure Sky Blue (`#2DA8FF`), Grass Green (`#58CC02`), Knowledge Lilac (`#8C52FF`), Sun Gold (`#FFB800`), Coral Heart Red (`#FF4757`), Cream Canvas (`#FFFDF9`).
  - **Tactile 3D Buttons**: Chunky, squishy pill buttons with 3D bottom bevels (`box-shadow: 0 5px 0 ...`) and bouncy active press states.
  - **Stat Chips**: Streak Flame (`🔥 3 Days`), XP Stars (`⭐ 0 XP`), Resilient Hearts (`❤️❤️❤️`).
  - **Animated Sky Stage**: Fluffy floating clouds, gentle sinusoidal flag bobbing, and responsive layout.
  - **Country Detail Modal**: Educational popup sheet with large flag, capital, continent, and animated soundwave "Listen Again" button.

### 3. Country Flag Resources
- **271 Crisp Vector SVG World Flags** located in [assets/flags/](file:///Users/khairahn/Documents/flag-flying-game/assets/flags/).
- **Metadata Database** in [assets/data/countries.json](file:///Users/khairahn/Documents/flag-flying-game/assets/data/countries.json) with country names, 2-letter ISO codes, capital cities, continents, and direct flag paths.
- Sourced from open, free, high-quality standard ISO 3166-1 flag suite.

### 4. Interactive Game Prototype
- Main application in [index.html](file:///Users/khairahn/Documents/flag-flying-game/index.html) and [app.js](file:///Users/khairahn/Documents/flag-flying-game/app.js).
- **Features in action**:
  - Live flag spawning & floating across 3 sky lanes.
  - Real-time speech synthesis (`window.speechSynthesis.speak()`) pronouncing every country name when touched.
  - Web Audio API synthesizer for cheerful marimba chimes, fanfares, and pop effects without external MP3 dependencies.
  - Interactive Mascot Catcher (🦁 Pilot Lion).
  - Mission Quest mode ("Find & Touch Japan!") and Free Explorer mode.
  - Continent filters (All, Asia, Europe, Americas, Africa, Oceania).

---

## 🚀 How to Run Locally

### Option 1: Run with Python & Streamlit (Recommended)
```bash
python3 -m streamlit run streamlit_app.py --server.port 8502
```
Open **`http://localhost:8502`** in your browser.

Includes:
- 🎮 **Sky Arena**: Floating flags, interactive mascot, Web Speech synthesis on touch.
- 📖 **Flag Passport**: Interactive gallery of all 271 world flags with click-to-speak audio.
- 🧩 **Flag Trivia Quiz**: Multiple choice quiz inspired by the Figma kit's "What Letter is this?" screen.
- 📋 **PRD & UI Kit Viewer**: Live inspection of PRD and Design Tokens.

### Option 2: Run Vanilla HTML5 Server
```bash
python3 -m http.server 8080
```
Open **`http://localhost:8080/index.html`** in your browser.

---

## 📱 Supported Devices & Browsers
- **Mobile Browsers**: Safari (iOS 15+), Chrome for Android, Firefox Mobile.
- **Desktop**: Chrome, Edge, Safari, Firefox.
- **Audio API**: Uses standard Web Speech API + Web Audio API supported across all modern mobile and desktop browsers.
