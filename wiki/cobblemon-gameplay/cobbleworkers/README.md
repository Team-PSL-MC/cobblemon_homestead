# 🛠️ The Ultimate Cobbleworkers Guide

In Cobblemon Homestead, your Pokémon are the backbone of your infrastructure. This guide explains how to set up workers, which Pokémon can perform tasks, and how the server settings affect them.

---

# 🚀 Getting Started

To begin automating your base, you will need the **Pasture Block** from the Cobblemon mod.

### 1. Place a Pasture Block
This defines the area where your Pokémon will work.

### 2. Assign Workers
Only Pokémon inside the Pasture Block will perform tasks.

### 3. Storage
Pokémon will automatically deposit all harvested materials into nearby valid inventories:
- Chests
- Barrels
- Other supported containers

---

# 🌾 Farming & Botanical Harvesting

Workers in this category handle the lifecycle of natural resources.

## Apricorns *(Bug Type)*

Scyther, Beedrill, Leavanny, Parasect, Heracross, Pinsir, Scizor, Volcarona, Ninjask, Galvantula, Trevenant, Scolipede, Golisopod, Vikavolt, Centiskorch, Kleavor, Shuckle

## Crops *(Grass Type)*

Leavanny, Parasect, Torterra, Venusaur, Victreebel, Meganium, Gogoat, Eldegoss, Sunflora, Roserade, Ludicolo, Breloom, Sceptile, Serperior, Leafeon, Scyther

## Berries *(Grass Type)*

Torterra, Venusaur, Scyther, Beedrill, Munchlax, Greedent, Skwovet, Cherrim, Bounsweet, Snover, Vileplume, Bellossom, Whimsicott, Tropius, Florges, Shuckle

## Mints *(Fairy Type)*

Sylveon, Gardevoir, Togekiss, Mawile, Florges, Grimmsnarl, Impidimp, Morgrem, Ribombee, Hatterene, Primarina, Shiinotic, Whimsicott, Slurpuff, Aromatisse

## Nether Wart *(Ghost Type)*

Misdreavus, Banette, Trevenant, Spiritomb, Mismagius, Chandelure, Cofagrigus, Runerigus, Dhelmise, Decidueye, Phantump, Gourgeist, Sableye, Dusknoir, Lampent

## Honey *(No Type Required)*

Combee, Vespiquen, Ribombee, Beedrill, Teddiursa

---

# ⛏️ Mining & Resource Generation

## 💎 Amethyst *(Rock)*

Sableye, Carbink, Gigalith, Boldore, Crustle

## 🪨 Tumblestone *(Steel)*

Aron, Aggron, Magnemite, Lucario, Bronzong, Steelix, Excadrill, Copperajah, Metagross, Bastiodon, Gigalith, Probopass, Rhyperior, Scizor, Perrserker

## 🏺 Archeology *(Ground)*

Baltoy, Sandslash, Claydol, Flygon, Mudsdale, Excadrill, Golurk, Runerigus, Sigilyph, Armaldo

---

# 🌋 Fluid & Environmental Generation

## Lava Generators

Camerupt, Magmar, Slugma, Coalossal, Centiskorch, Torkoal, Magcargo, Magmortar, Heatran, Turtonator, Groudon, Iron-Moth

Cooldown: **90 seconds**

## Water Generators

Squirtle, Totodile, Mudkip, Piplup, Lapras, Wailmer, Ducklett, Wooper, Dewgong, Seel, Horsea, Staryu, Slowpoke, Tentacool, Shellder

Cooldown: **90 seconds**

## Snow Generators

Snover, Abomasnow, Cryogonal, Alolan Vulpix, Frosmoth, Glaceon

Cooldown: **90 seconds**

---

# ⚙️ Industrial Utilities & Logistics

## Furnace Fuel

Torkoal, Magcargo, Darmanitan, Rapidash, Chandelure

- Fuel generation cooldown: **80 seconds**
- Burn time added: **80 seconds**
- Required type: **Fire**

## Brewing Stand Fuel

Turtonator, Druddigon, Noivern, Flygon, Haxorus

- Fuel generation cooldown: **80 seconds**
- Brewing fuel added: **5**

## Irrigation

Squirtle, Totodile, Oshawott, Froakie, Vaporeon, Marill, Politoed, Pelipper, Quagsire, Swampert, Ludicolo, Milotic, Gastrodon, Azumarill, Cloyster

Radius: **1 block**

## Floor Cleaning / Item Gathering *(Psychic)*

Alakazam, Metagross, Reuniclus, Orbeetle, Abra, Gardevoir, Sigilyph, Beheeyem, Claydol, Espathra, Chimecho, Natu, Elgyem, Bronzong, Slowking

---

# 🚑 Support & Exploration

## Field Medics

Chansey, Audino, Comfey, Blissey, Hatenna, Hattrem, Cresselia, Alcremie, Miltank, Alomomola, Toxapex, Clefable, Togekiss, Milotic, Florges, Vaporeon, Clawitzer

### Valid Healing Moves

- Wish  
- Softboiled  
- Moonlight  
- Recover  
- Roost  
- Heal Bell  
- Aromatherapy  
- Synthesis  
- Rest  
- Life Dew  
- Heal Pulse  
- Lunar Blessing  
- Aqua Ring  
- Milk Drink  
- Floral Healing  

### Healing Effects

- Regeneration Duration: **20 seconds**
- Regeneration Level: **Regeneration I**
- **Chansey & Blissey can heal nearby players**

---

## Aerial Scouts

Corviknight, Noctowl, Talonflame, Altaria, Pidgeot, Staraptor, Kilowattrel, Mandibuzz, Swellow, Dragonite, Ninjask, Togekiss

Cooldown: **80 seconds**

Scouts generate exploration maps for structures like:
- Fossils
- Ruins
- Shipwrecks
- Mineshafts
- Cobblemon ruins

---

## Fishing Loot

Wishiwashi, Feebas, Inkay, Dhelmise, Bruxish, Shellder, Cloyster, Staryu, Starmie, Corsola, Lanturn, Relicanth, Wimpod, Clamperl, Luvdisc, Octillery, Whiscash, Basculin, Gorebyss

Cooldown: **60 seconds**

---

## Fire Safety

Mudkip, Piplup, Oshawott, Froakie, Blastoise, Feraligatr, Empoleon, Samurott, Greninja, Golduck, Poliwrath, Kingler, Seadra, Gyarados, Mantine

Extinguish radius: **1 block**

---

# ⚙️ Server Worker Mechanics

Worker scanning values:

- Blocks scanned per tick: **15**
- Search radius: **8 blocks**
- Search height: **5 blocks**

Higher values improve efficiency but increase server load.

---

# 🌟 Best Multi-Purpose Worker Pokémon

If you only have a few pasture slots, these Pokémon cover **the most jobs**.

## Top Tier Workers

**Scyther**
- Apricorns
- Crops
- Berries

**Beedrill**
- Apricorns
- Berries
- Honey

**Togekiss**
- Mints
- Healing
- Aerial scouting

**Florges**
- Berries
- Mints
- Healing

**Trevenant**
- Apricorns
- Nether Wart

**Centiskorch**
- Apricorns
- Lava generation

**Metagross**
- Tumblestone
- Floor cleaning

**Vaporeon**
- Irrigation
- Healing

---

# 🧠 Example 6-Slot Worker Team

A highly efficient base team:

1. **Scyther** — farming backbone  
2. **Beedrill** — berries + honey  
3. **Metagross** — mining + item collection  
4. **Vaporeon** — irrigation + healing  
5. **Torkoal** — furnace fuel  
6. **Togekiss** — healing + scouting

This setup covers:

- Farming
- Mining
- Fuel
- Healing
- Exploration
- Resource automation
