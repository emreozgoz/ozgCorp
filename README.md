# 🌙 DARK SANCTUM

> **Survive. Evolve. Dominate.**

A dark gothic action-roguelike survival game inspired by Vampire Survivors, but with unique tactical gameplay mechanics.

Created by **Matrix AI Team** - 18 autonomous AI agents working together in perfect harmony.

---

## 🎮 Game Features

### Core Mechanics
- **WASD Movement** - Smooth, responsive character control
- **Auto-Attack System** - Automatically target and attack nearest enemies
- **Wave-Based Spawning** - Escalating difficulty with exponentially scaling enemy counts
- **XP & Leveling** - Gain experience from kills, level up to become stronger
- **Tactical Positioning** - Enemy AI chases you, positioning matters

### Coming Soon
- **4 Active Abilities** (Q, W, E, R) - Manual skill-based combat
- **8 Character Classes** - Unique playstyles and abilities
- **Epic Boss Fights** - Major bosses every 5 minutes
- **Ability Synergies** - Combine abilities for devastating combos
- **Meta-Progression** - Persistent upgrades between runs

---

## 🎨 Dark Gothic Aesthetic

- **Deep Purple-Black** backgrounds
- **Blood Red** health bars and enemies
- **Arcane Gold** XP and leveling
- **Minimal HUD** - Focus on gameplay, not UI clutter

---

## 🛠️ Technical Architecture

Built with **Entity Component System (ECS)** for maximum performance and modularity:

- **Components** - Pure data (Position, Velocity, Health, etc.)
- **Systems** - Pure logic (Movement, Combat, Rendering, etc.)
- **World** - Coordinates everything at 60 FPS

### Tech Stack
- **Python 3.14**
- **Pygame 2.6**
- **NumPy** for math operations

---

## 🚀 Installation & Running

### Requirements
- Python 3.10+
- SDL2 libraries (installed via Homebrew on macOS)

### Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Run the game
python3 main.py
```

### Controls
- **WASD / Arrow Keys** - Move
- **Q, W, E, R** - Abilities (coming soon)
- **ESC** - Pause/Resume
- **SPACE** - Start game / Restart after death

---

## 📁 Project Structure

```
dark-sanctum/
├── main.py                    # Main game loop
├── config/
│   └── settings.py           # Game configuration & balance
├── src/
│   ├── core/
│   │   └── ecs.py           # Entity Component System
│   ├── components/
│   │   └── components.py    # All game components
│   ├── systems/
│   │   ├── movement_system.py
│   │   ├── combat_system.py
│   │   ├── spawn_system.py
│   │   └── render_system.py
│   └── entities/
│       └── factory.py       # Entity creation helpers
└── requirements.txt
```

---

## 🤖 Created By Matrix AI Team

This game was developed by **18 specialized AI agents** working autonomously:

### Core SDLC Agents (8)
1. **Requirements Analyst** - User stories & acceptance criteria
2. **System Architect** - Technical architecture & design
3. **Developer** - Code implementation
4. **QA Tester** - Testing & quality assurance
5. **Security Specialist** - Security best practices
6. **DevOps Engineer** - CI/CD & deployment
7. **Project Manager** - Sprint planning & coordination
8. **UI/UX Designer** - Visual design & user experience

### AAA Game Studio Agents (10)
9. **Game Designer** - Game mechanics & balance
10. **Technical Director** - Performance & optimization
11. **Creative Director** - Vision & artistic direction
12. **Data Analyst** - Metrics & analytics
13. **Live Ops Manager** - Post-launch operations
14. **Monetization Specialist** - Economy design
15. **Audio Director** - Sound design (coming soon)
16. **Localization Manager** - Multi-language support (coming soon)
17. **Community Manager** - Player engagement
18. **Producer** - Overall coordination

---

## 📊 Development Progress

**Sprint 1: Core MVP** ✅ COMPLETE
- [x] ECS Architecture
- [x] Player Movement (WASD)
- [x] Auto-Attack System
- [x] Wave-Based Enemy Spawning
- [x] Health & Damage System
- [x] XP & Leveling
- [x] Gothic UI/HUD
- [x] Game States (Menu, Playing, Pause, Game Over)

**Next Sprints:**
- Sprint 2: Ability System (Q/W/E/R)
- Sprint 3: Character Classes
- Sprint 4: Boss Fights
- Sprint 5: Power-ups & Pickups
- Sprint 6: Particle Effects & Polish

---

## 🎯 What Makes Dark Sanctum Different?

Unlike Vampire Survivors:

| Feature | Vampire Survivors | Dark Sanctum |
|---------|------------------|--------------|
| Combat | Passive auto-attack only | Auto-attack + 4 active abilities |
| Positioning | Less important | Tactical positioning matters |
| Characters | Generic survivor | 8 unique character classes |
| Bosses | Rare | Epic boss every 5 minutes |
| Theme | Cute pixel art | Dark gothic horror |
| Abilities | Passive synergies | Active skill combos |

---

## 📜 License

Created by Matrix AI Team for educational and demonstration purposes.

---

## 🌟 Credits

**Game Concept:** Matrix Game Designer Agent
**Architecture:** Matrix System Architect Agent
**Code:** Matrix Developer Agent
**Art Direction:** Matrix UI/UX Designer & Creative Director
**Game Design:** Matrix Game Designer Agent
**Testing:** Matrix QA Tester Agent
**Coordination:** Matrix Project Manager & Producer

**Inspired by:** Vampire Survivors by poncle
**Built with:** Python, Pygame, and lots of AI collaboration ❤️

---

**🌙 May you survive the darkness... 🌙**
