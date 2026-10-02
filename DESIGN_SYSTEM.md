# Kids Games Design System & UI Kit Specification

Based on the [Kids Learning Game Mobile UI Kit](https://www.figma.com/community/file/1560366525230816041/kids-learning-game-ui).

---

## 1. Color Profile & Palette Tokens

The color profile is specially calibrated for young learners: high vibrance, friendly contrast, warm creamy backgrounds, and saturated gamified accent colors.

### 1.1 Brand Accent Colors

```css
:root {
  /* --- Primary: Tangerine Play (Missions, Streak, Primary Highlights) --- */
  --kid-orange-500: #FF7A00; /* Main hero orange */
  --kid-orange-400: #FF9633; /* Light hover */
  --kid-orange-600: #E66600; /* 3D bottom bevel */
  --kid-orange-100: #FFF3E6; /* Soft chip background */

  /* --- Secondary: Sky Azure Blue (Actions, Continue, Alphabets) --- */
  --kid-blue-500: #2DA8FF;   /* Crisp sky blue */
  --kid-blue-400: #62BFFF;   /* Lighter glow */
  --kid-blue-600: #0D8FE8;   /* 3D bottom bevel */
  --kid-blue-100: #EAF5FF;   /* Soft chip background */

  /* --- Success: Grass Green (Correct catch, Level up, Progress) --- */
  --kid-green-500: #58CC02;  /* Vibrant learning green */
  --kid-green-400: #76DE2C;  /* Light green */
  --kid-green-600: #46A302;  /* 3D bottom bevel */
  --kid-green-100: #EFFCE8;  /* Soft green pill background */

  /* --- Knowledge: Lilac Purple (World cards, Knowledge badges) --- */
  --kid-purple-500: #8C52FF; /* Playful purple */
  --kid-purple-400: #AB7EFF; /* Lilac tint */
  --kid-purple-600: #7135E8; /* 3D bottom bevel */
  --kid-purple-100: #F4EEFF; /* Soft purple chip */

  /* --- Rewards: Golden Sun Yellow (Stars, Coins, XP) --- */
  --kid-yellow-500: #FFB800; /* Rich gold */
  --kid-yellow-400: #FFCA3A; /* Shiny yellow */
  --kid-yellow-600: #E09E00; /* 3D shadow */
  --kid-yellow-100: #FFF8E6; /* Cream yellow */

  /* --- Vitality: Coral Red (Hearts, Warning, Near-miss) --- */
  --kid-red-500: #FF4757;    /* Bouncy heart red */
  --kid-red-400: #FF6B81;    /* Bright pinkish red */
  --kid-red-600: #DE283A;    /* 3D shadow */
  --kid-red-100: #FFEAEB;    /* Soft red chip */

  /* --- Canvas & Surfaces --- */
  --kid-bg-cream: #FFFDF9;      /* Warm off-white page background */
  --kid-bg-cream-dark: #FBF4E8; /* Subtle background contrast */
  --kid-card-bg: #FFFFFF;       /* Pure white card surface */
  --kid-card-border: #EFE7DA;   /* Soft warm outline */
  
  /* --- Text Hierarchy --- */
  --kid-text-dark: #1E293B;  /* Headings & bold labels */
  --kid-text-body: #475569;  /* Explanations & facts */
  --kid-text-muted: #94A3B8; /* Secondary clues & placeholders */

  /* --- Sky Stage Environment --- */
  --kid-sky-top: #56B7FF;
  --kid-sky-mid: #A3DDFF;
  --kid-sky-bottom: #E8F6FF;
}
```

---

## 2. Typography System

Kids games require round, approachable, highly legible typefaces with generous line height and friendly letterforms.

- **Primary Display & Headings:** `Outfit`, `Fredoka`, or `Nunito`, rounded sans-serif.
- **Fallback Stack:** `system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif`.

| Style Class | Font Size | Weight | Line Height | Letter Spacing | Usage |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `text-kid-display` | `32px` - `40px` | Bold (`800`) | `1.15` | `-0.02em` | Level Victory, Country Reveal |
| `text-kid-title` | `24px` - `28px` | Bold (`700`) | `1.2` | `-0.01em` | Screen Headers, Mission Prompts |
| `text-kid-subtitle` | `18px` - `20px` | SemiBold (`600`) | `1.3` | `0` | Card Titles, Category Tags |
| `text-kid-body` | `15px` - `16px` | Medium (`500`) | `1.4` | `0` | Country Facts, Instructions |
| `text-kid-caption` | `12px` - `13px` | SemiBold (`600`) | `1.2` | `0.02em` | Chips, Sub-badges, Timers |

---

## 3. UI Component Library

### 3.1 Chunky 3D Pushable Buttons
The signature element from the Kids Games UI Kit is tactile 3D pill buttons that sink upon touch.

```css
.btn-kid {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  border-radius: 9999px;
  font-family: inherit;
  font-weight: 800;
  font-size: 16px;
  border: none;
  cursor: pointer;
  padding: 14px 28px;
  transition: transform 0.1s ease, box-shadow 0.1s ease;
  user-select: none;
  text-decoration: none;
}

/* Primary Orange Button */
.btn-kid-primary {
  background-color: var(--kid-orange-500);
  color: #FFFFFF;
  box-shadow: 0 5px 0 var(--kid-orange-600);
}
.btn-kid-primary:active {
  transform: translateY(3px);
  box-shadow: 0 2px 0 var(--kid-orange-600);
}

/* Action Blue Button */
.btn-kid-blue {
  background-color: var(--kid-blue-500);
  color: #FFFFFF;
  box-shadow: 0 5px 0 var(--kid-blue-600);
}
.btn-kid-blue:active {
  transform: translateY(3px);
  box-shadow: 0 2px 0 var(--kid-blue-600);
}

/* Success Green Button */
.btn-kid-green {
  background-color: var(--kid-green-500);
  color: #FFFFFF;
  box-shadow: 0 5px 0 var(--kid-green-600);
}
.btn-kid-green:active {
  transform: translateY(3px);
  box-shadow: 0 2px 0 var(--kid-green-600);
}

/* Clean White Card Button */
.btn-kid-white {
  background-color: #FFFFFF;
  color: var(--kid-text-dark);
  border: 2px solid var(--kid-card-border);
  box-shadow: 0 4px 0 #DED5C5;
}
.btn-kid-white:active {
  transform: translateY(2px);
  box-shadow: 0 2px 0 #DED5C5;
}
```

### 3.2 Status & Stat Chips
Used in the global top header for continuous gamified reinforcement:
- **Streak Chip:** Flame icon 🔥 with bold orange count inside a soft cream pill.
- **Lives Chip:** 3 bouncing red hearts ❤️❤️❤️ with pulse effect on miss.
- **Audio & Settings Chips:** Round circular buttons with 3D bottom bevels.

### 3.3 Flying Flag Cards
- Vector SVG flag framed in a soft rounded squircle (`border-radius: 18px`).
- Border: `3px solid #FFFFFF` with soft floating shadow (`0 10px 20px rgba(0, 0, 0, 0.12)`).
- Gentle sinusoidal bobbing animation imitating a balloon or kite in the sky.
- Subtle interactive hover/touch pop: expands by $8\%$ with a golden outline ring.

### 3.4 Glossy Level Progress Bar
- Rounded pill container with inner depth (`background: #E8E2D5`).
- Progress indicator filled with vibrant orange-to-yellow gradient.
- Glossy top sheen highlight (`rgba(255, 255, 255, 0.35)`).
- Star milestones along the track that pop into bright gold when passed.

### 3.5 Country Reveal & Pronunciation Modal
- Springy bottom sheet / centered modal window with a soft frosted glass backdrop.
- Large $240 \times 160\text{px}$ crisp country flag display.
- **"Listen Again" Audio Button:** Chunky pill with pulsing soundwave animation.
- Capital city badge & Continent tag.
- Fun kid-friendly fact (e.g., *"Brazil is famous for the Amazon rainforest and carnival!"*).

---

## 4. Animation & Micro-Interactions

| Interaction | Animation Spec | Emotion / Feedback |
| :--- | :--- | :--- |
| **Flag Catch** | Scale `1.0` $\rightarrow$ `1.25` $\rightarrow$ `0` with confetti burst | Instant triumph, sensory satisfaction |
| **Speech Audio Trigger** | Ripple ring expands outward around the caught flag | Visually ties spoken audio to the touch |
| **Wrong Flag Tap** | Quick $6\text{Hz}$ horizontal wiggle ($\pm 6\text{px}$) + soft boing | Clear gentle feedback without discouragement |
| **Cloud Drift** | Infinite smooth horizontal drift with random altitude | Living, serene sky atmosphere |
| **Button Press** | $3\text{px}$ down translation + shadow collapse in $60\text{ms}$ | Physical squishy toy feeling |
