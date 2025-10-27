# 🪐 **Planet Hunter**

**Planet Hunter** is an arcade-style game developed in **Python**, where the player controls a spaceship to collect celestial bodies scattered across space.  
The game combines **Pygame** for graphics, sound, and event handling, **Tkinter** for the interactive main menu, and **Requests** for dynamic API integration.

---

## 🎮 **How to Play**

- Use the **W, A, S, D** keys to move the spaceship.  
- Capture celestial bodies to score points.  
- Every **10 points**, a **boss battle** appears — defeating the boss allows you to advance to the next stage.  
- After the first boss, **20 points** are required to progress between levels.  
- Defeat the **final boss** to unlock the ending screen!

---

## ✨ **Features**

- 🎨 **Menu Interface:** Main menu built with **Tkinter**, including buttons for “Play” and “Game Rules”.  
- 🎵 **Dynamic Soundtrack:** Background music changes between stages and boss battles.  
- 🧩 **Stage Progression:** The difficulty increases as you advance through levels.  
- 💥 **Boss Battles:** Unique bosses appear at specific score milestones.  
- 🌌 **API Integration:** Planet names are dynamically loaded from an **exoplanet API**, providing variety and authenticity.  
- 🖼️ **Background Transitions:** Smooth visual transitions enhance the sense of progression.  
- 🧠 **Skill Development:** Reinforces Python skills in event handling, collisions, GUI, sound, and game logic.

---

## ⚙️ **Technologies Used**

- 🐍 **Python 3**  
- 🎮 **Pygame** – graphics, event loop, sound system  
- 🖱️ **Tkinter** – main menu and interface  
- 🌍 **Requests** – API integration for planet names  

---

## 🪐 **About the Planet API**

The game connects to a **public exoplanet API** to generate unique planet names dynamically.  
If the API is unavailable, a **local fallback list** ensures the game continues smoothly.


