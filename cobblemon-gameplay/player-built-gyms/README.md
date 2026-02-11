---
icon: dumbbell
---

# Player Built Gyms

## 🏟️ Gym Builder’s Guide: Brecher’s Trainers

Want to become a Gym Leader? Use Brecher’s Trainers to create a persistent challenge for other players. This mod uses specialized blocks and wands to automate battles and rewards.

### 🛠️ Phase 1: Creating Your Trainers

Before you place a block, make sure you have the Pokémon team you want the NPC to use in your current party.

1. Place a Trainer Spawner:
   * Normal: Standard gym trainers.
   * Leader: The final boss of your gym.
2. Assign the Team: Right-click the spawner with an empty hand to "mirror" your current party onto the block.
3. Spawn the NPC: Right-click the block again to make the trainer appear.
4. Customize:
   * Name: Use a Nametag (named at an anvil) on the spawner.
   * Appearance: Use an Ogrepon Mask (named with a player name) to change their skin. _(Example: Name a mask "AshKetchum" to give the NPC that skin)._

***

### 🔗 Phase 2: Wiring the Gym

A "working" gym needs a brain to know when it's been completed and when to reset.

#### 1. The Gym Controller (The Brain)

Place this at the end of your gym. Use the Linking Wand to connect all your Trainer Spawners and Puzzle Blocks to this controller. It tracks the progress of the player.

#### 2. Completion Triggers & Rewards

* Completion Trigger: Link this to your Leader Spawner. When the leader is defeated, this block emits a Redstone signal.
* Reward Dispenser: Place this near the exit. Connect it to the Redstone signal from your Completion Trigger. Load it with your Custom Badge or loot!

#### 3. Resetting for the Next Player

Place a Reset Block at the gym exit. When a player walks over it (or interacts with it), it tells the Gym Controller to reset all trainers and puzzles for the next challenger.

***

### 🏆 The League System

Your gym isn't just an island—it's part of the server's economy!

* League Points (LP): Players earn these by defeating your trainers.
* League Vendors: You can set up NPCs where players spend LP.
  * _Example Command:_ `/brecher_trainers vendor spawn ~ ~ ~ basic_shop "Gym Shop"`
* Badge Box: Don't forget to give players a Badge Box so they can show off their victories!

***

#### Quick Troubleshooting

* Trainer won't spawn? Ensure there are at least 2 air blocks above the spawner.
* Redstone not firing? Check your Linking Wand connections. You must click the Spawner first, then the Trigger/Controller.
* Need a reset? Use the Reset Wand to manually clear a gym if a player gets stuck.
