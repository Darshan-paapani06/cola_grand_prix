
# 🏁 Cola Grand Prix

> **The ultimate animated racing showdown between Pepsi & Coca-Cola.**
> Two legendary brands. One track. One winner.

<br/>

---

## 🎮 What Is This?

**Cola Grand Prix** is a fun, fully animated racing game built in two versions:

| Version | Technology | Where It Runs |
|---|---|---|
| 🖥️ **Terminal Edition** | Python 3 · ANSI color | Any terminal / command line |
| 🌐 **Browser Edition** | HTML · CSS · JavaScript | Any modern web browser |

Both versions feature **Pepsi vs Coca-Cola** in a head-to-head race — complete with named cars, boost events, smooth animation, and a winner celebration screen.

---

## 📁 Project Structure

```
cola-grand-prix/
├── race.py               # Terminal racing game (Python)
├── cola_grand_prix.html  # Browser racing game (HTML/CSS/JS)
└── README.md             # This file
```

---

## 🐍 Terminal Version — `race.py`

### Features

- 🚗 **Named ASCII cars** — `PEPSI` and `COCA-COLA` are stamped directly on the car body
- 🎬 **Smooth animation** — cursor-up redraws at ~18 fps for fluid car movement
- 📐 **Auto-scales** to your terminal width using `shutil.get_terminal_size()`
- ⚡ **Random race events** — Nitro Boost, Tyre Slip, Engine Sputter, Drafting Issues
- 📊 **Live progress bars** with percentage readout per lane
- 🏆 **Trophy screen** with celebration flicker on Pepsi victory
- 🚀 **3-2-1 countdown** before the race begins

### Requirements

- Python **3.6+**
- A terminal that supports **ANSI escape codes**
  - ✅ macOS Terminal, iTerm2
  - ✅ Linux (bash, zsh, fish)
  - ✅ Windows Terminal / PowerShell (modern)
  - ✅ VS Code integrated terminal

### Run It

```bash
python3 race.py
```

> Press `ENTER` at the intro screen to begin. Use `Ctrl+C` to exit at any time.

---

## 🌐 Browser Version — `cola_grand_prix.html`

### Features

- 🎨 **Fully designed SVG cars** — detailed Pepsi (blue) and Coca-Cola (red) racers with branded colors, windows, wheels, headlights, spoilers and name labels
- 🌌 **Cinematic dark theme** — deep navy starfield background with glowing lane effects
- 🖋️ **Orbitron + Rajdhani** typefaces — purpose-built for racing UIs
- 🎬 **60 fps animation** via `requestAnimationFrame` with sub-frame interpolation
- ⚡ **Race events** — real-time event ticker (Nitro Boost, Tyre Slip, Turbo Fire, etc.)
- 📊 **Live progress bars** with speed readout in km/h per lane
- 🔢 **Win scoreboard** — tracks Pepsi vs Cola wins across multiple races
- 🏆 **Winner overlay** — animated trophy pop-in with gold gradient title
- ⏱️ **Countdown overlay** — full-screen 3…2…1…GO! before each race

### How to Open

No server or installation needed. Just double-click the file:

```
cola_grand_prix.html
```

Or open it in your browser manually:

```
File → Open File → cola_grand_prix.html
```

### Supported Browsers

| Browser | Supported |
|---|---|
| Chrome / Edge | ✅ |
| Firefox | ✅ |
| Safari | ✅ |
| Mobile (iOS / Android) | ✅ |

---

## 🏎️ How the Race Works

### Speed System

Each car has a **base speed** and a **random variance** applied every frame:

| Car | Base Speed | Variance | Effective Range |
|---|---|---|---|
| 🔵 Pepsi | 0.18 u/s | ±0.12 | 0.18 – 0.30 |
| 🔴 Coca-Cola | 0.13 u/s | ±0.10 | 0.13 – 0.23 |

Pepsi's minimum speed exceeds Cola's maximum on most ticks — giving Pepsi a **reliable winning advantage** while keeping the race visually competitive.

### Race Events

Random events fire throughout the race to add drama:

| Event | Affects | Effect | Duration |
|---|---|---|---|
| ⚡ Nitro Boost | Pepsi | +0.18 speed | 500 ms |
| 🔥 Turbo Fire | Pepsi | +0.14 speed | 400 ms |
| 🔧 Pit Wobble | Pepsi | −0.08 speed | 300 ms |
| ⚠ Tyre Slip | Coca-Cola | −0.14 speed | 500 ms |
| 💨 Engine Sputter | Coca-Cola | −0.12 speed | 600 ms |

### Winner Guarantee

A safety clamp in the race engine ensures Pepsi **always crosses the finish line first** — even in edge cases where Coca-Cola's random rolls are unusually high.

```python
# Terminal version safety clamp
if cola_pos >= finish - 2 and pepsi_pos < finish - 2:
    cola_pos = finish - 3
```

```javascript
// Browser version safety clamp
if (colaPos >= 0.97 && pepsiPos < 0.97) {
    colaPos = 0.96;
}
```

---

## 🎨 Design Language

### Terminal Version

| Element | Implementation |
|---|---|
| Colors | ANSI escape sequences (`\033[94m` = Blue, `\033[91m` = Red) |
| Animation | Cursor-up escape `\033[nA` to rewrite lines in-place |
| Car width | 20 characters, name embedded in row 4 of the car art |
| Track | Dot-matrix (`·`) ground with `║` finish line marker |
| Cursor | Hidden during race (`\033[?25l`), restored on exit |

### Browser Version

| Element | Implementation |
|---|---|
| Typography | `Orbitron` (display) + `Rajdhani` (body) via Google Fonts |
| Palette | `#004B93` Pepsi Blue · `#F40009` Cola Red · `#FFD700` Gold |
| Cars | Inline SVG with branded colors, glass, wheels, text labels |
| Animation | CSS keyframes + `requestAnimationFrame` JS loop at 60 fps |
| Responsiveness | `clamp()` font sizes, flex layout, scales on all screen sizes |

---

## ⚙️ Customisation

### Change Race Speed (Terminal)

In `race.py`, adjust the `TICK` variable and speed ranges:

```python
TICK = 0.055          # Seconds per frame — lower = faster animation

pepsi_speed = random.uniform(0.42, 0.82)   # Pepsi speed per tick
cola_speed  = random.uniform(0.22, 0.62)   # Cola speed per tick
```

### Change Race Speed (Browser)

In `cola_grand_prix.html`, adjust the constants near the top of the `<script>` block:

```javascript
const PEPSI_BASE = 0.18;   // Pepsi base speed (units per second)
const PEPSI_RAND = 0.12;   // Pepsi random variance
const COLA_BASE  = 0.13;   // Cola base speed
const COLA_RAND  = 0.10;   // Cola random variance
```

### Let Cola Win (Browser)

To make the race truly random, remove the safety clamp block in `raceLoop()`:

```javascript
// Delete or comment out these lines:
if (colaPos >= 0.97 && pepsiPos < 0.97) { colaPos = 0.96; }
if (colaPos >= 1.0  && pepsiPos < 1.0)  { colaPos = 0.995; }
```

---

## 🚀 Quick Start Summary

```bash
# Clone or download the project
# Terminal game:
python3 race.py

# Browser game:
open cola_grand_prix.html       # macOS
start cola_grand_prix.html      # Windows
xdg-open cola_grand_prix.html   # Linux
```

---

## 📄 License

This project is made for fun and learning purposes.  
All brand names (Pepsi, Coca-Cola) belong to their respective owners.

---

<div align="center">

**Made with ☕ and a little friendly rivalry.**

🔵 **PEPSI** always wins. That's just science.

</div>
