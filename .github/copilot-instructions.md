# TBA - Copilot Instructions

## Project Overview
**TBA** (Bug dans la Matrice) is a text-based adventure game set in a multiverse version of ESIEE. Players navigate 6+ locations, collect items, interact with NPCs, and complete quests to repair the "glitched" reality through assembling a machine and deploying patches.

## Architecture

### Core Components
- **[game.py](../game.py)**: Main engine - orchestrates rooms, player, commands, main loop
- **[player.py](../player.py)**: Player state manager with `Stats`, `InventoryManager`, `QuestsTracker` (patches, quest flags)
- **[room.py](../room.py)**: Location data - name, description, exits, items, NPCs, optional locks
- **[actions.py](../actions.py)**: All gameplay mechanics - movement, dialogue, item handling, quests
- **[config.py](../config.py)**: Game configuration - room layouts, items, NPCs, all starting state
- **[command.py](../command.py)**: Command structure (name, help text, action function, param count)
- **[character.py](../character.py)**: NPC representation with cycling dialogue messages
- **[item.py](../item.py)**: Item definition (name, description, weight)
- **[fortnite_game.py](../fortnite_game.py)**: Mini-game for patch quest (text-based Fortnite)

### Data Flow
1. Game initialization loads config → creates rooms, player, commands
2. Main loop: parse user input → execute matching command action
3. Actions modify game state (player position, inventory, quests)
4. Quests tracked via `player.quests.quests` dict; patches via `player.quests.patch_*` attributes

## Critical Patterns & Conventions

### Accessing Quest/Patch State
```python
# ✅ CORRECT - accessing quest dict through QuestsTracker
game.player.quests.quests['quest_name'] = 'completed'
game.player.quests.quests.get('quest_name')

# ✅ CORRECT - patch progression (direct attributes)
game.player.quests.patch_hardware = min(100, game.player.quests.patch_hardware + 25)

# ❌ WRONG - these will fail
game.player.quests['quest_name']  # No __getitem__ on QuestsTracker
game.player.patch_hardware  # Doesn't exist at player level
```

### NPC Dialogue Integration
1. Add character to [config.py](../config.py) `pnj_config` dict
2. Add NPC handling in `Actions.talk()` if special behavior needed
3. Use `_talk_` prefix for dialogue handler methods (e.g., `_talk_bde`, `_talk_courivaud`)
4. NPCs have cycling messages via `Character.get_msg()`

### Quest Structure
- Quests tracked as strings: `'started'`, `'completed'`, boolean flags, or True
- Multi-stage quests use multiple dict keys (e.g., `piece_assistetud_obtained`, `piece_salle_3142_obtained`)
- After machine assembly → patch quest chain begins (see [actions.py#L386-L396](../actions.py#L386-L396))

### Item Inventory Management
```python
# Check capacity before taking item
if game.player.inventory.can_carry(item):
    game.player.inventory.items[item_name] = item
    room.items.remove(item_name)

# Track weight: items dict maps names → Item objects with .weight attribute
current_weight = sum(it.weight for it in game.player.inventory.items.values())
```

## Quest Chain: Fortnite/Patch Workflow

**Trigger**: After `machine_assembled` quest completed, talking to Courivaud starts `patch_python_quest`.

**Steps**:
1. Player must go to Junior Entreprise and talk to `etudiant_junior`
2. If `patch_python_quest == 'started'`, student proposes Fortnite match
3. Player runs `play_fortnite_minigame()` → returns boolean (won/lost)
4. If won: `patch_python_quest` → `'completed'`, `patch_social += 30`
5. Revisit Courivaud → confirms completion

**Key Files**:
- [fortnite_game.py](../fortnite_game.py): Mini-game implementation
- [actions.py](../actions.py) `_talk_etudiant_junior()`: Quest logic
- [config.py](../config.py): `etudiant_junior` NPC definition

## Commands & Testing

### Run Game
```bash
python main.py
```

### Run Tests
```bash
python -m pytest tests/
```

### Available Commands (partial list)
- `talk <npc>` - Interact with NPC
- `go <direction>` - Move between rooms
- `take <item>` / `drop <item>` - Item management
- `assemble` - Build machine (Salle Blanche only, requires 3 pieces)
- `fortnite` - Play mini-game (Junior location, during patch quest)
- `cheat_assemble` - Skip to machine assembly state

### Debug Mode
Set `DEBUG = True` in [config.py](../config.py#L7) for verbose output

## Common Tasks

### Adding a New Quest
1. Define boolean/string key in `game.player.quests.quests`
2. Trigger in appropriate action (e.g., `_talk_courivaud`)
3. Check state with `.get()` before progressing
4. Update in test files if behavior-critical

### Adding an NPC Interaction
1. Create character in [config.py](../config.py) → `pnj_config`
2. Add room reference to `rooms_config[room_key]['pnj']`
3. Handle in `Actions.talk()` with `elif name == 'npc_id':`
4. Optional: Create `_talk_npc_id()` helper for complex logic

### Modifying Room/Item Layout
All changes in [config.py](../config.py) - game loads this once at startup. Changes require restart.

## Notes for AI Agents
- **French game**: All text output is in French; maintain consistency
- **State isolation**: Each player instance separate; no global state persistence
- **Weighted inventory**: Track `item.weight` when adding/removing items
- **NPC cycling**: Each call to `character.get_msg()` advances dialogue index
- **No file I/O**: Game runs entirely in memory
