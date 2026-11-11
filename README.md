<h1 align="center">🪐 Planet Hunter</h1>

<p align="center">
  <i>An arcade space game in Python: pilot your rocket, capture planets discovered by NASA, and defeat three cosmic bosses.</i>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/Tkinter-GUI-1a1b27?style=for-the-badge" alt="Tkinter"/>
  <img src="https://img.shields.io/badge/Pygame-audio-2E8B57?style=for-the-badge" alt="Pygame"/>
  <img src="https://img.shields.io/badge/NASA-Exoplanet%20API-0B3D91?style=for-the-badge&logo=nasa&logoColor=white" alt="NASA API"/>
</p>

---

## 📖 About

**Planet Hunter** is a side-scrolling arcade game. You control a rocket on the left side of the screen and capture the planets flying towards you. Each level is named after a **real exoplanet**, fetched live from the **NASA Exoplanet Archive**. Every second level, a boss fight interrupts the hunt.

## 🎮 How to Play

| Key | Action |
|-----|--------|
| <kbd>↑</kbd> | Move the rocket up |
| <kbd>↓</kbd> | Move the rocket down |

- Capture planets to earn points; every **10 points** you level up.
- Planets get **faster and spawn more often** as levels increase, and each level changes their colour and shape.
- On levels **2, 4 and 6** you face a boss:
  1. **Titanus Prime**: a comet bouncing across the screen. Intercept it!
  2. **Spectra**: a faster, harder-to-catch boss.
  3. **Doppelvoid**: spawns decoys. Only the **real** one ends the game, so a fake one restarts the fight.
- Beat Doppelvoid to trigger the victory sequence and final screen. 🚀

## ✨ Features

- 🌌 **Live NASA data**: level names come from exoplanets discovered after 2010 (`pscomppars` table, NASA Exoplanet Archive TAP API)
- 🧵 **Non-blocking API calls**: requests run in a background thread so the game never freezes
- 🛡️ **Graceful fallback**: if the API is unreachable, the game keeps running with a placeholder name
- 👾 **3 unique boss fights** with their own movement patterns
- 🎵 **Dynamic soundtrack**: separate level, boss and victory music with fade-in transitions
- 🖼️ **Changing backgrounds** for each stage
- 🏠 **Main menu** with *Play* and *Rules* screens

## 🚀 Getting Started

### Requirements
- Python **3.8+** (Tkinter is included with the standard Python installer)
- An internet connection (optional, for real planet names)

### Installation
```bash
git clone https://github.com/DiasDias106/Planet_Hunter.git
cd Planet_Hunter/Planet_hunter/planet_hunter_game
pip install pillow requests pygame
python planet_hunter_main.py
```

> ⚠️ Run the script **from inside `planet_hunter_game/`**, because images and music are loaded through relative paths (`imagens_proj/`).

## 📁 Project Structure

```
Planet_hunter/planet_hunter_game/
├── planet_hunter_main.py   # Game logic, menus, bosses and API integration
└── imagens_proj/           # Backgrounds, boss sprites, rocket and soundtrack (.jpg/.png/.mp3)
```

## 🛠️ Built With

| Library | Purpose |
|---------|---------|
| `tkinter` | Window, canvas rendering, menus and input |
| `Pillow` | Loading and resizing images |
| `pygame` | Music playback (`pygame.mixer`) |
| `requests` | NASA Exoplanet Archive API calls |
| `threading` | Background API requests |

## 📜 License

Distributed under the terms of the [LICENSE](LICENSE) file in this repository.

---

<p align="center">Made by <a href="https://github.com/DiasDias106">Francisco Dias</a></p>
