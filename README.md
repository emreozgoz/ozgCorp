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

### Character Classes (5 Unique)
1. **Shadow Knight** - Balanced warrior (HP: 100, DMG: 10, SPD: 250)
   - Passive: Shadow Step - Dash cooldown -25%
2. **Blood Mage** - Glass cannon caster (HP: 70, DMG: 15, SPD: 220)
   - Passive: Blood Magic - Abilities +50% damage
3. **Void Guardian** - Tank defender (HP: 150, DMG: 7, SPD: 200)
   - Passive: Iron Will - Take 25% less damage
4. **Necromancer** - Death cultist (HP: 85, DMG: 12, SPD: 230)
   - Passive: Soul Harvest - Weapons deal +10% damage per kill (5 stacks)
5. **Tempest Ranger** - Swift archer (HP: 90, DMG: 9, SPD: 270)
   - Passive: Wind Walker - Projectile weapons fire 30% faster

### Enemy Types (4 + 5 Bosses)
1. **Basic Enemy** - Standard threat (60% spawn rate)
2. **Imp** - Fast swarmer (20% spawn rate) - 1.5x speed, low HP
3. **Golem** - Tank blocker (15% spawn rate) - 3x HP, slow
4. **Wraith** - Ranged shooter (5% spawn rate) - Keeps distance, fires projectiles
5. **5 Unique Bosses** (every 5 waves with rotation):
   - 💀 **Blood Titan** (Wave 5) - Tank boss (10x HP, 2x damage)
   - 👤 **Void Reaver** (Wave 10) - Teleports + invulnerability
   - ❄️ **Frost Colossus** (Wave 15) - Slow aura (50% in 300px)
   - ☠️ **Plague Herald** (Wave 20) - Summons 3 imps
   - 🔥 **Inferno Lord** (Wave 25+) - Rage mode (<30% HP)

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

**✅ GAME COMPLETE - v2.0 RELEASED - 17 SPRINTS DELIVERED**

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

**Sprint 7: Weapon Upgrade System** ✅
- Vampire Survivors-style weapon progression
- 5 Unique weapons with full functionality:
  - ⚔️ Shadow Blade - Orbiting melee swords (1-3 blades)
  - 🔮 Arcane Seeker - Homing magic missiles (1-5 missiles)
  - ⚡ Chain Lightning - Enemy-bouncing lightning (5-bounce chains)
  - 🧪 Blessed Vial - Damaging ground puddles (AoE DoT)
  - 🧄 Garlic Aura - Defensive damage aura (60-150px radius)
- Level-up choice screen with 3 random weapon cards
- WeaponInventory tracks equipped weapons (5 levels each)
- WeaponFireSystem fires weapons automatically
- Beautiful level-up UI with weapon stats and descriptions
- Each weapon has unique behavior and visual identity

**Sprint 8: Meta-Progression & Statistics** ✅
- Comprehensive statistics tracking system
- Persistent high score system (JSON storage)
- 10 unlockable achievements:
  - First Blood, Slayer, Massacre (kill milestones)
  - Survivor, Endurance (survival time)
  - Boss Slayer, Titan Killer (boss kills)
  - Ability Master, Power Collector (action counts)
  - Wave Warrior (progression)
- Real-time achievement unlocking with notifications
- Score calculation algorithm (kills, level, wave, time, etc.)
- Enhanced game over screen with:
  - Detailed session statistics (2 columns)
  - Final score display
  - NEW HIGH SCORE indicator
  - Top 5 high scores leaderboard
- Lifetime statistics tracking:
  - Total games played
  - All-time kills, damage, playtime
  - Highest level/wave records
- dark_sanctum_stats.json persistent storage

**Sprint 9: Pause Menu & Game Flow** ✅
- Comprehensive pause menu system
- Resume, Restart, Settings, Main Menu options
- Dark gothic pause overlay
- Smooth state transitions
- Keyboard navigation (Arrow keys + Enter)

**Sprint 10: Multiple Game Maps** ✅
- 3 Unique environments with hazards:
  - 🏰 Blood Cathedral - Blood pools (poison damage)
  - 🌲 Cursed Forest - Shadow trees (vision obstruction)
  - ☠️ Bone Wastes - Bone spikes (physical damage)
- Map selection screen before character selection
- Environmental hazards with damage-over-time
- Unique visual themes per map

**Sprint 11: Expanded Weapon Arsenal** ✅
- 3 New weapons added (Total: 8 base weapons):
  - 🗡️ Death's Scythe - Massive rotating melee
  - ❄️ Frost Orb - Ice projectiles with slow
  - 🔱 Crimson Spear - Piercing blood lances
- Enhanced weapon variety for builds
- Unique mechanics per weapon type

**Sprint 12: Weapon Evolution System** ✅
- Vampire Survivors-style weapon evolutions
- 3 Evolved weapons unlocked at Level 5:
  - 💀 Reaper's Embrace (from Shadow Blade)
  - 🌌 Cosmic Annihilation (from Arcane Seeker)
  - ✨ Sacred Ward (from Garlic Aura)
- Evolved weapons have 2-4x base stats
- Special evolution UI with golden borders
- "⚡ EVOLUTION ⚡" banner on level-up
- Automatic evolution priority in choices

**Sprint 13: Audio Enhancement** ✅
- Volume control system:
  - Master volume (0.0-1.0)
  - SFX volume control
  - Music volume control
- Audio toggle on/off
- Volume multiplier system (base × sfx × master)
- 6 procedural sound effects:
  - Player hit, Enemy death
  - Ability cast, Boss spawn
  - Level up, Projectile fire
- Lightweight procedural generation (no audio files)

**Sprint 14: Content Expansion - Massive Arsenal** ✅
- 2 New character classes (Total: 5):
  - 💀 Necromancer - Soul Harvest (+10% damage per kill, 5 stacks)
  - 🌪️ Tempest Ranger - Wind Walker (30% faster projectiles)
- 5 New base weapons (Total: 13):
  - 👻 Soul Reaver - Life-drain projectiles
  - 🦴 Bone Storm - Rapid orbiting bones
  - 📖 Cursed Tome - Explosive sigils
  - 🗡️ Venom Fang - Rapid poison daggers
  - 🌑 Void Lance - Massive piercing projectiles
- 2 New weapon evolutions (Total: 5):
  - ⚡ Storm Bringer (from Chain Lightning)
  - ❄️ Absolute Zero (from Frost Orb)
- Total: 18 weapons (13 base + 5 evolved)

**Sprint 15: Boss Variety System** ✅
- 5 Unique boss types with rotation:
  - 💀 Blood Titan (Wave 5) - Classic tank boss
  - 👤 Void Reaver (Wave 10) - Fast assassin
  - ❄️ Frost Colossus (Wave 15) - Tankiest boss
  - ☠️ Plague Herald (Wave 20) - Summoner
  - 🔥 Inferno Lord (Wave 25+) - Enrage mechanic
- Boss rotation system (different boss each encounter)
- Unique visual identity per boss (color, glow, size)
- Boss-specific stat multipliers (HP, damage, speed)
- Guaranteed power-up drop from all bosses
- Boss rotation cycles after Wave 25

**Sprint 16: Environmental Hazards** ✅ (Previously Sprint 10)
- 3 Unique maps with hazards:
  - 🏰 Dark Sanctum - No hazards (tutorial map)
  - ⛪ Blood Cathedral - Blood pools (5 dmg/s)
  - 🗝️ Cursed Crypts - Spike traps (20 dmg every 2s)
- Environmental damage system
- Spike trap timing mechanics (2s active, 2s inactive)
- Map-based achievement unlocking
- Strategic positioning challenges

**Sprint 17: Boss Abilities - Epic Mechanics** ✅
- 4 Unique boss special abilities:
  - 👤 Void Reaver: Teleport every 3s + 0.5s invulnerability
  - ❄️ Frost Colossus: 50% slow aura (300px radius)
  - ☠️ Plague Herald: Summon 3 imps every 5s
  - 🔥 Inferno Lord: Rage mode at <30% HP (+50% damage/speed)
- Boss ability system with cooldown tracking
- Unique tactics required per boss
- Visual/audio feedback for all abilities
- Each boss provides different challenge

---

## 🎯 What Makes Dark Sanctum Different?

Unlike Vampire Survivors:

| Feature | Vampire Survivors | Dark Sanctum |
|---------|------------------|--------------|
| Combat | Passive auto-attack only | Auto-attack + 4 active abilities |
| Positioning | Less important | Tactical positioning matters |
| Characters | Generic survivor | 5 unique character classes |
| Weapons | ~15 weapons | 18 total (13 base + 5 evolved) |
| Maps | Single map | 3 maps with environmental hazards |
| Bosses | Rare, repetitive | 5 unique bosses with special abilities |
| Theme | Cute pixel art | Dark gothic horror |
| Abilities | Passive synergies | Active skill combos (Q/W/E/R) |
| Progression | Weapon upgrades only | Weapons + Evolutions + Achievements + Stats |

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
