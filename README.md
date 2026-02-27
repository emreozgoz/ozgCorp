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

### Combat System
- **4 Active Abilities** (Q, W, E, R) - Manual skill-based tactical combat
  - **Q - Shadow Dash**: Teleport with invulnerability
  - **W - Blood Nova**: AoE damage explosion
  - **E - Arcane Missiles**: 3 homing projectiles
  - **R - Time Freeze**: Slow all enemies (Ultimate)
- **Boss Fights** - Epic Blood Titan every 5 waves (10x health, 2x damage)
- **Particle Effects** - Satisfying visual feedback on hits and deaths

### Character Classes (3 Unique)
1. **Shadow Knight** - Balanced warrior (HP: 100, DMG: 10, SPD: 250)
   - Passive: Shadow Step - Dash cooldown -25%
2. **Blood Mage** - Glass cannon caster (HP: 70, DMG: 15, SPD: 220)
   - Passive: Blood Magic - Abilities +50% damage
3. **Void Guardian** - Tank defender (HP: 150, DMG: 7, SPD: 200)
   - Passive: Iron Will - Take 25% less damage

### Enemy Types (4 + Boss)
1. **Basic Enemy** - Standard threat (60% spawn rate)
2. **Imp** - Fast swarmer (20% spawn rate) - 1.5x speed, low HP
3. **Golem** - Tank blocker (15% spawn rate) - 3x HP, slow
4. **Wraith** - Ranged shooter (5% spawn rate) - Keeps distance, fires projectiles
5. **Blood Titan** - Boss (every 5 waves) - 10x HP, 2x damage, special glow

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

**✅ GAME COMPLETE - 6 SPRINTS DELIVERED**

**Sprint 1: Core MVP** ✅
- ECS Architecture
- Player Movement (WASD)
- Auto-Attack System
- Wave-Based Enemy Spawning
- Health & Damage System
- XP & Leveling
- Gothic UI/HUD
- Game States (Menu, Playing, Pause, Game Over)

**Sprint 2: Ability System** ✅
- 4 Active Abilities (Q/W/E/R)
- Shadow Dash (mobility + invulnerability)
- Blood Nova (AoE damage)
- Arcane Missiles (homing projectiles)
- Time Freeze (mass slow)
- Ability UI with cooldown tracking

**Sprint 3: Boss & Polish** ✅
- Blood Titan boss (every 5 waves)
- Boss health bar system
- Particle effects (death, level up)
- Visual polish (glow effects)
- Boss glow indicators

**Sprint 4: Character Classes** ✅
- 3 Unique Classes
- Character Selection Screen
- Class-specific stats
- Unique passive abilities
- Replayability through variety

**Sprint 5: Final Polish** ✅
- Enhanced game over stats
- Wave counter tracking
- Survival timer
- Character info display
- Complete game loop

**Sprint 6: Enhanced Content** ✅
- Procedural sound effect system (pygame mixer)
- 3 New enemy types with unique behaviors:
  - Fast Enemy (Imp) - Quick, swarming
  - Tank Enemy (Golem) - Slow, high HP
  - Ranged Enemy (Wraith) - Kiting, projectiles
- Power-up drops (15% chance):
  - Health (green) - Restore 25 HP
  - Damage Boost (orange) - +5 damage
  - XP Orb (gold) - Instant 50 XP
- Varied enemy spawning (60% basic, 20% fast, 15% tank, 5% ranged)
- Audio feedback for all actions

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
