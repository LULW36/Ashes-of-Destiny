import random
import json

SAVE_FILE = "game_save.json"


# Function to check if a save file exists
def save_file_exists():
    try:
        with open(SAVE_FILE, 'r') as save_file:
            return True
    except FileNotFoundError:
        return False


# Save game progress to a file
def save_game(player):
    with open(SAVE_FILE, 'w') as save_file:
        json.dump(player, save_file)
    print("Game progress saved successfully.")


# Load game progress from a file
def load_game():
    try:
        with open(SAVE_FILE, 'r') as save_file:
            player = json.load(save_file)
            print("Game progress loaded successfully.")
            return player
    except FileNotFoundError:
        print("No saved game found. Starting a new game.")
        return None


# Function to provide introductory lore
def lore_drop():
    print("\n=========================")
    print(" The Ashen Rain Descends ")
    print("=========================")
    print("The Light has been extinguished by the Ashen Rain, and its dark clouds have blocked the sun for decades.")
    print("Chaos roams the lands of Alleria with no hope in sight.")
    print(
        "Great Kingdoms have collapsed, and inner strife among the remaining Human factions has further fractured the world.")
    print(
        "Small hamlets remain in the wake of chaos, where the last remnants of Allerian society dwell, struggling to survive.")
    print(
        "They fight off creatures emboldened by the Ashen Rain while also struggling to find food and drinkable water.")
    print("Little hope remains in Alleria.... Until you awoke....")


# Create player and set initial attributes
def create_player():
    player_name = input("Enter your character's name: ")
    message = (
        f"You faintly hear another voice almost as if it is an echo.\n"
        f"{player_name},\n"
        f"The Ashen Rain has removed the Light from this world, and darkness threatens the land.\n"
        f"I have chosen you to end this blasphemy and bring order back to my people."
    )
    print(message)

    return {
        'name': player_name,
        'health': 100,
        'mana': 100,
        'gold': 0,
        'experience': 0,
        'level': 1,
        'armor': 5,
        'attack': 10,
        'abilities': [],
        'bless_active': False,
        'bless_turns': 0,
        'in_hope_end': True,
        'inventory': [],
        'cooldowns': {
            'heroic_strike': 0,
            'holy_fire': 0,
            'bless': 0,
            'lights_vengeance': 0,
            'firebolt': 0,
            'summon_lights_protector': 0,
            'summon_archangels_of_light': 0
        },
        'summoned_archangels': [],
        'summoned_lights_protector': None
    }


# Load or create player function
def load_or_create_player():
    player = load_game()
    if player is None:
        lore_drop()  # Providing the game's introductory lore
        player = create_player()
    return player


# Initialize player only once, at the start of the game
player = load_or_create_player()

# Leveling system
max_level = 10
level_thresholds = [100, 200, 400, 700, 1000, 1400, 1800, 2200, 2700]  # XP required for each level


def level_up():
    while player['level'] < max_level and player['experience'] >= level_thresholds[player['level'] - 1]:
        player['level'] += 1
        player['health'] += 20  # Increase total health per level
        player['mana'] += 10  # Increase total mana per level
        print(
            f"Congratulations! You have reached level {player['level']}! Health increased to {player['health']} and Mana increased to {player['mana']}")
        if player['level'] == 2:
            player['abilities'].append(heroic_strike)
            print("You have learned a new ability: Heroic Strike!")
        elif player['level'] == 4:
            player['abilities'].append(holy_fire)
            print("You have learned a new ability: Holy Fire!")
        elif player['level'] == 6:
            player['abilities'].append(lights_vengeance)
            print("You have learned a new ability: Light's Vengeance!")
        elif player['level'] == 8:
            player['abilities'].append(summon_lights_protector)
            print("You have learned a new ability: Summon Light's Protector!")
        elif player['level'] == 10:
            player['abilities'].append(summon_archangels_of_light)
            print("You have learned a new ability: Summon Archangels of the Light!")


# Function to add rewards after defeating creatures
def add_rewards(enemy):
    player['gold'] += enemy['gold_reward']
    player['experience'] += enemy['xp_reward']
    level_up()


# Function to get the player's maximum health
def get_player_max_health():
    return 100 + (player['level'] - 1) * 20


# Function to get the player's maximum mana
def get_player_max_mana():
    return 100 + (player['level'] - 1) * 10


# Player Abilities
# Heroic Strike Ability
def heroic_strike():
    if player['mana'] >= 20 and player['cooldowns']['heroic_strike'] == 0:
        player['mana'] -= 20
        damage = player['attack'] + random.randint(5, 10)
        print(f"Heroic Strike deals {damage} damage to multiple enemies!")
        player['cooldowns']['heroic_strike'] = 1
        return damage, None
    else:
        if player['cooldowns']['heroic_strike'] > 0:
            print(f"Heroic Strike is on cooldown for {player['cooldowns']['heroic_strike']} more turns.")
        else:
            print("Not enough mana to cast Heroic Strike.")
        return 0, None

# Holy Fire Ability
def holy_fire():
    if player['mana'] >= 30 and player['cooldowns']['holy_fire'] == 0:
        player['mana'] -= 30
        damage = random.randint(20, 30)
        smited_turns = random.randint(1, 2)
        print(f"Holy Fire calls upon holy fire from the sky and smites the enemy, dealing {damage} damage and smiting them for {smited_turns} turns!")
        player['cooldowns']['holy_fire'] = 3
        return damage, smited_turns
    else:
        if player['cooldowns']['holy_fire'] > 0:
            print(f"Holy Fire is on cooldown for {player['cooldowns']['holy_fire']} more turns.")
        else:
            print("Not enough mana to cast Holy Fire.")
        return 0, None

# Light's Vengeance Ability
def lights_vengeance():
    if player['mana'] >= 40 and player['cooldowns']['lights_vengeance'] == 0:
        player['mana'] -= 40
        damage = random.randint(15, 25)
        smited_turns = random.randint(1, 2)
        print(f"Light's Vengeance deals {damage} damage to all enemies and smites them for {smited_turns} turns!")
        player['cooldowns']['lights_vengeance'] = 3
        return damage, smited_turns
    else:
        if player['cooldowns']['lights_vengeance'] > 0:
            print(f"Light's Vengeance is on cooldown for {player['cooldowns']['lights_vengeance']} more turns.")
        else:
            print("Not enough mana to cast Light's Vengeance.")
        return 0, None

# Summon Light's Protector Ability
def summon_lights_protector():
    if player['mana'] >= 50 and player['cooldowns']['summon_lights_protector'] == 0:
        player['mana'] -= 50
        player['cooldowns']['summon_lights_protector'] = 5
        player['summoned_lights_protector'] = {
            'name': "Light's Protector",
            'health': 200,
            'attack': 20,
            'armor': 10,
            'abilities': [
                {'name': 'Shield Bash', 'damage': 18, 'effect': 'stun'},
                {'name': 'Holy Strike', 'damage': 25, 'effect': None},
                {'name': 'Guardian Roar', 'effect': 'taunt'},
                {'name': 'Divine Smite', 'damage': 30, 'effect': 'stun' if random.random() < 0.3 else None}
            ]
        }
        print("Light's Protector has been summoned!")
        return 0, None
    else:
        print("Cannot summon Light's Protector. Either insufficient mana or already summoned.")
        return 0, None

# Summon Archangels of Light Ability
def summon_archangels_of_light():
    if player['mana'] >= 100 and player['cooldowns']['summon_archangels_of_light'] == 0:
        player['mana'] -= 100
        player['cooldowns']['summon_archangels_of_light'] = 5
        player['summoned_archangels'] = [
            {
                'name': f"Archangel of the Light {i + 1}",
                'health': 250,
                'attack': 30,
                'armor': 15,
                'abilities': [
                    {'name': 'Radiant Slash', 'damage': 35, 'effect': 'blind'},
                    {'name': 'Holy Wrath', 'damage': 40, 'effect': None},
                    {'name': 'Sanctuary', 'effect': 'shield'},
                    {'name': 'Judgment', 'damage': 50, 'effect': 'stun' if random.random() < 0.4 else None}
                ]
            } for i in range(3)
        ]
        print("Three Archangels of the Light have been summoned!")
        return 0, None
    else:
        print("Cannot summon Archangels of the Light. Either insufficient mana or already summoned.")
        return 0, None


# Function to handle invalid inputs (overlying function since some inputs were not returning outputs when using invalid input)
def get_valid_input(prompt, valid_options):
    while True:
        choice = input(prompt).strip().lower()
        if choice in valid_options:
            return choice
        print("Invalid choice. Please try again.")


# Creature Types
def goblin():
    level_multiplier = player['level'] * 0.2
    return {
        "name": "Goblin",
        "health": int(25 + 25 * level_multiplier),
        "gold_reward": int(10 + 5 * level_multiplier),
        "xp_reward": int(15 + 10 * level_multiplier),
        "attack": int(6 + 6 * level_multiplier),
        "armor": 3,
        "abilities": [
            {'name': 'Quick Slash',
             'description': 'A fast attack that deals minor damage but has a 20% chance to evade counter-attacks.'},
            {'name': 'Rabble Roar', 'description': 'Increases attack by 2 for the next two turns.'}
        ]
    }


def goblin_warleader():
    level_multiplier = player['level'] * 0.3
    health = int(70 + 70 * level_multiplier)
    return {
        "name": "Goblin Warleader",
        "health": health,
        "max_health": health,  # Add this line to define max_health
        "gold_reward": int(20 + 10 * level_multiplier),
        "xp_reward": int(30 + 20 * level_multiplier),
        "attack": int(12 + 12 * level_multiplier),
        "armor": 6,
        "abilities": [
            {'name': 'Berserker Rage',
             'description': 'Increases attack by 5 for the next turn but reduces armor by 2.'},
            {'name': 'Heavy Swing', 'description': 'Deals double attack damage but has a 20% chance of missing.'},
            {'name': 'Shield Bash', 'description': 'Deals minor damage and stuns the player for one turn.'}
        ]
    }


def troll_cultist():
    level_multiplier = player['level'] * 0.3
    return {
        "name": "Troll Cultist",
        "health": int(40 + 40 * level_multiplier),
        "gold_reward": int(15 + 8 * level_multiplier),
        "xp_reward": int(25 + 15 * level_multiplier),
        "attack": int(8 + 8 * level_multiplier),
        "armor": 3,
        "abilities": [
            {'name': 'Hex', 'description': 'Reduces player’s attack by 3 for three turns.'},
            {'name': 'Blood Siphon', 'description': 'Restores 10 health by siphoning from the player.'}
        ]
    }


def radakhan():
    level_multiplier = player['level'] * 0.4
    return {
        "name": "Radakhan, Speaker of the Ash",
        "health": int(120 + 120 * level_multiplier),
        "gold_reward": int(40 + 15 * level_multiplier),
        "xp_reward": int(50 + 25 * level_multiplier),
        "attack": int(15 + 15 * level_multiplier),
        "armor": 8,
        "abilities": [
            {'name': 'Ashen Strike', 'description': 'Deals high fire damage and inflicts burning for two turns.'},
            {'name': 'Infernal Shield', 'description': 'Increases armor by 10 for the next turn.'}
        ]
    }


def orc_warrior():
    level_multiplier = player['level'] * 0.3
    return {
        "name": "Orc Warrior",
        "health": int(60 + 60 * level_multiplier),
        "gold_reward": int(20 + 10 * level_multiplier),
        "xp_reward": int(30 + 20 * level_multiplier),
        "attack": int(12 + 12 * level_multiplier),
        "armor": 5,
        "abilities": [
            {'name': 'Battle Shout', 'description': 'Increases attack by 3 for the next two turns.'},
            {'name': 'Crushing Blow', 'description': 'Deals 1.5 times attack damage.'}
        ]
    }


def orc_shaman():
    level_multiplier = player['level'] * 0.3
    return {
        "name": "Orc Shaman",
        "health": int(50 + 50 * level_multiplier),
        "gold_reward": int(25 + 12 * level_multiplier),
        "xp_reward": int(35 + 20 * level_multiplier),
        "attack": int(10 + 10 * level_multiplier),
        "armor": 4,
        "abilities": [
            {'name': 'Lightning Bolt',
             'description': 'Deals magic damage, ignoring player armor. Has a 20% chance to stun the player for one turn.'},
            {'name': 'Healing Ward', 'description': 'Heals all allied orcs for 20 health.'}
        ]
    }


def gilgamash():
    level_multiplier = player['level'] * 0.5
    return {
        "name": "Gilgamash, Scourge of Humanity",
        "health": int(200 + 200 * level_multiplier),
        "gold_reward": int(60 + 20 * level_multiplier),
        "xp_reward": int(80 + 40 * level_multiplier),
        "attack": int(18 + 18 * level_multiplier),
        "armor": 10,
        "abilities": [
            {'name': 'Devastate',
             'description': 'Deals massive damage with a 10% chance to instantly defeat the player.'},
            {'name': 'Blood Lust',
             'description': 'Increases Gilgamash’s attack speed by 20% and attack damage by 10 for two turns.'},
            {'name': 'Infernal Strike',
             'description': 'Deals fire damage and burns the player for three turns, dealing additional damage over time.'}
        ]
    }


def kaelthuzad():
    level_multiplier = player['level'] * 0.5
    return {
        "name": "Kael'Thuzad, the Everlasting Chill of the Void",
        "health": int(250 + 250 * level_multiplier),
        "gold_reward": int(70 + 25 * level_multiplier),
        "xp_reward": int(90 + 45 * level_multiplier),
        "attack": int(20 + 20 * level_multiplier),
        "armor": 12,
        "abilities": [
            {'name': 'Frost Nova',
             'description': 'Deals AoE frost damage with a 25% chance to freeze the player for one turn.'},
            {'name': 'Frostbolt',
             'description': 'Deals frost damage and has a 25% chance to freeze the player for one turn.'},
            {'name': 'Curse of the Void', 'description': 'Reduces player’s attack and armor by 5 for three turns.'}
        ]
    }


def skeleton():
    level_multiplier = player['level'] * 0.2
    return {
        "name": "Skeleton",
        "health": int(20 + 20 * level_multiplier),
        "gold_reward": int(8 + 4 * level_multiplier),
        "xp_reward": int(10 + 8 * level_multiplier),
        "attack": int(7 + 7 * level_multiplier),
        "armor": 3,
        "abilities": [
            {'name': 'Chill Grasp',
             'description': 'Has a 20% chance to freeze the player for one turn and deals minor frost damage.'},
            {'name': 'Soul Drain',
             'description': 'Steals 10 health from the player and reduces the player’s armor by 2 for two turns.'}
        ]
    }


def demon():
    level_multiplier = player['level'] * 0.4
    return {
        "name": "Demon",
        "health": int(30 + 30 * level_multiplier),
        "gold_reward": int(25 + 10 * level_multiplier),
        "xp_reward": int(40 + 20 * level_multiplier),
        "attack": int(10 + 10 * level_multiplier),
        "armor": 4,
        "abilities": [
            {'name': 'Demonic Claw', 'description': 'Deals moderate damage with a chance to apply a bleeding effect.'},
            {'name': 'Hellfire Slash', 'description': 'Deals fire damage to the player.'}
        ]
    }


def saltheron():
    level_multiplier = player['level'] * 0.6
    return {
        "name": "Sal'Theron, Harbinger of the Ashen Rain",
        "health": int(500 + 500 * level_multiplier),
        "gold_reward": int(100 + 30 * level_multiplier),
        "xp_reward": int(120 + 60 * level_multiplier),
        "attack": int(25 + 25 * level_multiplier),
        "armor": 20,
        "abilities": [
            {'name': 'Infernal Flames', 'description': 'Deals high fire damage and burns the player for three turns.'},
            {'name': 'Dark Dominion', 'description': 'Summons four demons to attack the player.'},
            {'name': 'Void Scream', 'description': 'Reduces player attack and armor by 5 for two turns.'}
        ]
    }


# Map of Alleria with dungeons and their descriptions
map_of_alleria = {
    "Goblin Caves": {
        "description": """Before the Light was blocked by the Ashen Rain, goblins were nearly extinct, 
but now that the Light fades, a new Goblin Warband has reappeared in these dark times.""",
        "creature_types": ["Goblins", "Goblin Warleader"],
        "unlocked": True
    },

    "Troll Cavern": {
        "description": "After discovering the secret to the goblin reemergence, you find a sinister plot that leads to a nearby Cavern"
                       "that is infested by Blasphemous Troll Cultist...",
        "creature_types": ["Troll Cultist", "Troll Cult Leader"],
        "unlocked": False
    },

    "Orc Encampment": {
        "description": """After centuries of war with the Orcs, the Treatise of Gilgamon ensured a cold peace between the Humans and Orcs, 
    but now after learning the knowledge obtained from the Trolls, you find out that the Orcs have abandoned peace 
    and raised their war-banners once more. Who led them to this? The Orcs would not abandon their traditional values
    of Honor and such treachery may have been caused by something, but what would that be?""",
        "creature_types": ["Orcs", "Orc Warchief"],
        "unlocked": False
    },

    "Lich's Lair": {
        "description": """After defeating the treacherous Orc Leader, you examined a damning green glow from Gilgamash's Eyes. 
    He was not in control of his mind or actions. After you searched his person, you find a mysterious note 
    that has a strange language you have never seen before. However, from the little you can decipher from the note, 
    you noticed a set of directions that lead to a nearby lair. The only being in Alleria who even has the power 
    to control one's mind is a Lich, but they have been extinct since the last one was purged by The Holy Crusaders of legend.""",
        "creature_types": ["Lich", "Skeletons"],
        "unlocked": False
    },

    "Throne of Sal'Theron, Harbinger of the Ashen Rain": {
        "description": """After the death of the Lich, you were able to find his soul jar. Upon examining the jar, you noticed a scripture. 
    You took the soul jar to Enchanter Lothemar so that he was able to translate the incantations on it. 
    He concluded that the scripture was a binding enchantment that only a Demon Lord could conjure using dark magic. 
    Up until now, we thought Demon Lords did not exist in this plane of existence; forever battling the Light in the 
    Spheres of the Void, but we were wrong. Lothemar was able to use a counter enchantment that could trace the location 
    of its origin and its master. It traced back to the Demon Lord Sal'Theron, the 9th Arch-Demon of the Void. 
    It also showed the location of this Sal'Theron, an old ruined Ziggurat. This Demon Lord must be responsible for the Ashen Rain. 
    He must be stopped...""",
        "creature_types": ["Demons", "Demon Lord Sal'Theron"],
        "unlocked": False
    }
}


# Function to add item to inventory
def add_item_to_inventory(player, item):
    # Check if the item already exists in the inventory
    for inventory_item in player['inventory']:
        if inventory_item['name'] == item['name']:
            inventory_item['quantity'] += 1
            return
    # If the item does not exist, add it with quantity 1
    item_copy = item.copy()
    item_copy['quantity'] = 1
    player['inventory'].append(item_copy)


# Function to display the player's stats
def view_stats(player):
    print("\n--- Player Stats ---")
    print(f"Health: {player['health']}")
    print(f"Mana: {player['mana']}")
    print(f"Gold: {player['gold']}")
    print(f"Level: {player['level']}")
    print(f"Attack: {player['attack']}")
    print(f"Armor: {player['armor']}")
    print(f"Experience: {player['experience']}")
    print(f"Inventory: {player['inventory']}")


# Function to view map
def view_map():
    """Display the map with dungeon descriptions for unlocked locations."""
    print("\nMap of Alleria:")

    # Loop through dungeons and display names with descriptions for unlocked dungeons
    for dungeon, info in map_of_alleria.items():
        if info["unlocked"]:
            print(f"\n{dungeon}:")
            print(info["description"].strip())  # Display the description
        else:
            print(f"?????: ?????")

    # Ask if player wants to travel to an unlocked dungeon
    print("\nWhere would you like to travel?")
    travel_choice = input("Enter the dungeon name or 'Back' to return: ").strip()

    if travel_choice in map_of_alleria and map_of_alleria[travel_choice]["unlocked"]:
        print(f"Traveling to {travel_choice}...")
        # Start combat or other activities based on dungeon choice
        if travel_choice == "Goblin Caves":
            explore_goblin_caves()
        else:
            print("This dungeon is locked until you complete the previous one.")
    elif travel_choice.lower() == "back":
        print("Returning to the main menu...")
    else:
        print("Invalid choice or dungeon locked. Please try again.")
        view_map()


def visit_apothecary(player):
    print("\n--- Apothecary Denathrius ---")

    potions = [
        {"name": "Lesser Healing Potion", "health_restored": 25, "mana_restored": 0, "price": 8},
        {"name": "Healing Potion", "health_restored": 50, "mana_restored": 0, "price": 20},
        {"name": "Greater Healing Potion", "health_restored": 75, "mana_restored": 0, "price": 35},
        {"name": "Lesser Mana Potion", "health_restored": 0, "mana_restored": 25, "price": 8},
        {"name": "Mana Potion", "health_restored": 0, "mana_restored": 50, "price": 20},
        {"name": "Greater Mana Potion", "health_restored": 0, "mana_restored": 75, "price": 35}
    ]

    for index, potion in enumerate(potions, start=1):
        if potion['health_restored'] > 0:
            stats = f"{potion['name']} restores {potion['health_restored']} health and costs {potion['price']}g"
        else:
            stats = f"{potion['name']} restores {potion['mana_restored']} mana and costs {potion['price']}g"
        print(f"{index}. {stats}")

    print("7. Leave Apothecary")
    choice = input("Select a potion to buy or type '7' to leave: ")

    if choice.isdigit() and int(choice) in range(1, 7):
        selected_potion = potions[int(choice) - 1]

        if player['gold'] >= selected_potion['price']:
            player['gold'] -= selected_potion['price']
            print(f"You purchased {selected_potion['name']}!")
            player['inventory'].append(selected_potion)
        else:
            print("Not enough gold!")
    elif choice == '7':
        print("Leaving Apothecary...")
    else:
        print("Not a valid choice. Please try again.")


def visit_blacksmith(player):
    print("\n--- Blacksmith Belthor ---")

    items = [
        {"name": "Bronze Helmet", "health_bonus": 10, "armor_bonus": 6, "price": 30},
        {"name": "Bronze Greaves", "health_bonus": 10, "armor_bonus": 6, "price": 30},
        {"name": "Bronze Armor", "health_bonus": 10, "armor_bonus": 6, "price": 30},
        {"name": "Bronze Shield", "armor_bonus": 3, "price": 25},
        {"name": "Bronze Sword", "attack_bonus": 3, "price": 25},
        {"name": "Iron Helmet", "health_bonus": 15, "armor_bonus": 8, "price": 50},
        {"name": "Iron Greaves", "health_bonus": 15, "armor_bonus": 8, "price": 50},
        {"name": "Iron Armor", "health_bonus": 15, "armor_bonus": 8, "price": 50},
        {"name": "Iron Shield", "armor_bonus": 4, "price": 40},
        {"name": "Iron Sword", "attack_bonus": 4, "price": 45},
        {"name": "Plate-Scale Helmet", "health_bonus": 20, "armor_bonus": 12, "price": 70},
        {"name": "Plate-Scale Greaves", "health_bonus": 20, "armor_bonus": 12, "price": 70},
        {"name": "Plate-Scale Armor", "health_bonus": 20, "armor_bonus": 12, "price": 70},
        {"name": "Steel Shield", "armor_bonus": 5, "price": 55},
        {"name": "Steel Sword", "attack_bonus": 6, "price": 65},
        {"name": "Mithril Helmet", "health_bonus": 25, "armor_bonus": 15, "price": 100},
        {"name": "Mithril Greaves", "health_bonus": 25, "armor_bonus": 15, "price": 100},
        {"name": "Mithril Armor", "health_bonus": 25, "armor_bonus": 15, "price": 100},
        {"name": "Mithril Shield", "armor_bonus": 6, "price": 90},
        {"name": "Mithril Sword", "attack_bonus": 8, "price": 85},
        {"name": "Ashenbane Helmet", "health_bonus": 35, "armor_bonus": 20, "price": 150},
        {"name": "Ashenbane Greaves", "health_bonus": 35, "armor_bonus": 20, "price": 150},
        {"name": "Ashenbane Armor", "health_bonus": 35, "armor_bonus": 20, "price": 150},
        {"name": "Ashenbane Shield", "armor_bonus": 8, "price": 140},
        {"name": "Ashenbane Sword", "attack_bonus": 10, "price": 130},
        {"name": "Champion of the Light Helmet", "health_bonus": 45, "armor_bonus": 25, "price": 500},
        {"name": "Champion of the Light Greaves", "health_bonus": 45, "armor_bonus": 25, "price": 500},
        {"name": "Champion of the Light Armor", "health_bonus": 45, "armor_bonus": 25, "price": 500},
        {"name": "Malegos, Protector of the Light", "armor_bonus": 10, "health_bonus": 25, "reflect_chance": 0.2, "price": 450},
        {"name": "Azuregos, Blessed Blade of The Light", "attack_bonus": 12, "health_bonus": 20, "smite_chance": 0.2, "price": 480}
    ]

    for index, item in enumerate(items, start=1):
        stats_parts = []
        if item.get('health_bonus', 0) > 0:
            stats_parts.append(f"Health: {item['health_bonus']}")
        if item.get('armor_bonus', 0) > 0:
            stats_parts.append(f"Armor: {item['armor_bonus']}")
        if item.get('attack_bonus', 0) > 0:
            stats_parts.append(f"Attack: {item['attack_bonus']}")
        stats = ' '.join(stats_parts)
        print(f"{index}. {item['name']} - {stats} - {item['price']}g")

    while True:
        print("Select an item to purchase or type '0' to leave.")
        choice = input("Enter item number: ").strip()

        if choice.isdigit() and int(choice) in range(1, len(items) + 1):
            selected_item = items[int(choice) - 1]

            if player['gold'] >= selected_item['price']:
                player['gold'] -= selected_item['price']
                print(f"You purchased {selected_item['name']}!")
                # Add item to inventory
                add_item_to_inventory(player, selected_item)
            else:
                print("Not enough gold!")
        elif choice == '0':
            print("Leaving Blacksmith...")
            break
        else:
            print("Invalid choice. Please try again.")


# Function to visit Enchanter Lothemar
def visit_enchanter(player):
    print("\n--- Enchanter Lothemar ---")
    print("1. Scroll of Fiery Enchant - 40g (Enchants Sword with 1 Fire Damage, 20% chance to burn enemy)")
    print("2. Scroll of Conflagration - 80g (Enchants Sword with 2 Fire Damage, 40% chance to burn enemy)")
    print("3. Scroll of Hellfire - 120g (Enchants Sword with 3 Fire Damage, 60% chance to burn enemy)")
    print("4. Scroll of Frostbite - 50g (Enchants Sword with 1 Frost Damage, 20% chance to freeze enemy)")
    print("5. Scroll of Deep Freeze - 100g (Enchants Sword with 2 Frost Damage, 40% chance to freeze enemy)")
    print("6. Scroll of Absolute Zero - 150g (Enchants Sword with 3 Frost Damage, 60% chance to freeze enemy)")
    print("7. Scroll of Arcane Spark - 60g (Enchants Sword with 1 Arcane Damage, 20% chance to reduce enemy mana)")
    print("8. Scroll of Arcane Surge - 120g (Enchants Sword with 2 Arcane Damage, 40% chance to reduce enemy mana)")
    print("9. Scroll of Arcane Blast - 180g (Enchants Sword with 3 Arcane Damage, 60% chance to reduce enemy mana)")
    print("10. Crusader's Blessing - 500g (Enchants Sword with 5 Holy Damage, 20% chance to heal player)")
    print("11. Crusader's Wrath - 1000g (Enchants Sword with 8 Holy Damage, 40% chance to heal player)")
    print("12. Crusader's Fury - 1500g (Enchants Sword with 12 Holy Damage, 60% chance to heal player)")
    print("13. Leave Enchanter Lothemar")

    choice = input("Select an enchantment to buy or type '13' to leave: ")

    if choice.isdigit() and int(choice) in range(1, 13):
        enchants = [
            {"name": "Fiery Enchant", "price": 40, "damage": 1, "type": "fire", "effect": "burn", "chance": 20,
             "burn_damage": 2, "burn_turns": 2},
            {"name": "Conflagration", "price": 80, "damage": 2, "type": "fire", "effect": "burn", "chance": 40,
             "burn_damage": 3, "burn_turns": 3},
            {"name": "Hellfire", "price": 120, "damage": 3, "type": "fire", "effect": "burn", "chance": 60,
             "burn_damage": 4, "burn_turns": 3},
            {"name": "Frostbite", "price": 50, "damage": 1, "type": "frost", "effect": "freeze", "chance": 20},
            {"name": "Deep Freeze", "price": 100, "damage": 2, "type": "frost", "effect": "freeze", "chance": 40},
            {"name": "Absolute Zero", "price": 150, "damage": 3, "type": "frost", "effect": "freeze", "chance": 60},
            {"name": "Arcane Spark", "price": 60, "damage": 1, "type": "arcane", "effect": "mana burn", "chance": 20},
            {"name": "Arcane Surge", "price": 120, "damage": 2, "type": "arcane", "effect": "mana burn", "chance": 40},
            {"name": "Arcane Blast", "price": 180, "damage": 3, "type": "arcane", "effect": "mana burn", "chance": 60},
            {"name": "Crusader's Blessing", "price": 500, "damage": 5, "type": "holy", "effect": "heal", "chance": 20},
            {"name": "Crusader's Wrath", "price": 1000, "damage": 8, "type": "holy", "effect": "heal", "chance": 40},
            {"name": "Crusader's Fury", "price": 1500, "damage": 12, "type": "holy", "effect": "heal", "chance": 60}
        ]

        selected_enchant = enchants[int(choice) - 1]

        if player['gold'] >= selected_enchant['price']:
            player['gold'] -= selected_enchant['price']
            print(f"You purchased {selected_enchant['name']}!")
            player['inventory'].append(selected_enchant)
        else:
            print("Not enough gold!")
    elif choice == '13':
        print("Leaving Enchanter...")
    else:
        print("Not a valid choice. Please try again.")


# Menu Function for Hope's End
# Menu Function for Hope's End
def show_menu():
    while player['in_hope_end']:
        print("\n--- Hope's End The Last Bastion of the Light ---")
        print("1. View Inventory")
        print("2. View Stats")
        print("3. Rest")
        print("4. Visit Apothecary")
        print("5. Visit Blacksmith")
        print("6. Visit Enchanter")
        print("7. View Map")
        print("8. Save Game")
        print("9. Exit Game")

        print("Remember to save your game often!\nYou can only save your game in Hope's End.\nIf you have been defeated, remember to rest to regain your health and mana before attempting your next challenge.")

        choice = input("Select an option: ").strip()

        if choice == '1':
            view_inventory(player)
        elif choice == '2':
            view_stats(player)
        elif choice == '3':
            rest()
        elif choice == '4':
            visit_apothecary(player)
        elif choice == '5':
            visit_blacksmith(player)
        elif choice == '6':
            visit_enchanter(player)
        elif choice == '7':
            view_map()
        elif choice == '8':
            save_game(player)
        elif choice == '9':
            print("Exiting the game...")
            break
        else:
            print("Invalid choice. Please try again.")


# Function for Dungeon Menu outside of combat
def show_dungeon_menu():
    while True:
        print("\n--- Dungeon Menu ---")
        print("1. View Inventory")
        print("2. View Stats")
        print("3. View Abilities")
        print("4. Return to Hope's End")
        print("5. Exit Menu")

        choice = input("Select an option (1-5): ").strip().lower()

        if choice == '1':
            view_inventory(player)
        elif choice == '2':
            view_stats(player)
        elif choice == '3':
            view_abilities()
        elif choice == '4':
            warning = input("Warning: Returning to Hope's End will reset dungeon progress. Are you sure? (yes/no): ").strip().lower()
            if warning == 'yes':
                player['in_hope_end'] = True
                print("You return to Hope's End. The dungeon will reset.")
                break  # Exit the loop to return to Hope's End
            else:
                print("Continuing in the dungeon.")
        elif choice == '5':
            # Exit the menu and return to the previous interaction
            print("Exiting the dungeon menu...")
            break
        else:
            print("Invalid choice. Please try again.")

    # After breaking out of the loop, return to Hope's End main menu if the player chose to return
    if player['in_hope_end']:
        show_menu()


# Show menu in combat
def show_dungeon_menu_in_combat():
    while True:
        print("\n--- Dungeon Menu (Combat) ---")
        print("1. View Inventory")
        print("2. View Stats")
        print("3. View Abilities")
        print("4. Exit Menu")

        choice = input("Select an option: ").strip().lower()

        if choice == '1':
            view_inventory(player)
        elif choice == '2':
            view_stats(player)
        elif choice == '3':
            view_abilities()
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")


# Function to view abilities and their descriptions
def view_abilities():
    print("\n--- Player Abilities ---")
    abilities = {
        'heroic_strike': {
            'description': "A powerful melee attack dealing damage to multiple enemies.",
            'damage': "5-10 + base attack",
            'mana_cost': 20
        },
        'frostbolt': {
            'description': "A ranged spell dealing frost damage and freezing the target.",
            'damage': "12-20",
            'mana_cost': 30
        },
        'lights_vengeance': {
            'description': "Deals damage to all enemies and smites them, reducing their combat effectiveness.",
            'damage': "15-25",
            'mana_cost': 40
        },
        'summon_lights_protector': {
            'description': "Summons a powerful protector to aid in combat.",
            'damage': "Summons a protector with its own attacks",
            'mana_cost': 50
        }
    }

    for ability in player['abilities']:
        ability_name = ability.__name__
        if ability_name in abilities:
            ability_info = abilities[ability_name]
            print(f"\nAbility: {ability_name}")
            print(f"Description: {ability_info['description']}")
            print(f"Damage: {ability_info['damage']}")
            print(f"Mana Cost: {ability_info['mana_cost']}")
        else:
            print(f"\nAbility: {ability_name} - Description not found.")


# Function for Rest to restore health and mana
def rest():
    player['health'] = get_player_max_health()
    player['mana'] = get_player_max_mana()
    print("You rest and recover your health and mana to their maximum.")



def view_inventory(player):
    print("--- Inventory ---")  # Display inventory header
    if not player['inventory']:
        print("Your inventory is empty.")
        return

    consolidated_inventory = {}
    for item in player['inventory']:
        if item['name'] in consolidated_inventory:
            consolidated_inventory[item['name']]['quantity'] += 1
        else:
            consolidated_inventory[item['name']] = item.copy()
            consolidated_inventory[item['name']]['quantity'] = 1

    for index, (name, item) in enumerate(consolidated_inventory.items(), start=1):
        stats_parts = []
        if 'health_restored' in item or 'mana_restored' in item:
            if item.get('health_restored', 0) > 0:
                stats_parts.append(f"Health Restored: {item['health_restored']}")
            if item.get('mana_restored', 0) > 0:
                stats_parts.append(f"Mana Restored: {item['mana_restored']}")
        elif 'enchant' in item:
            enchantment = item['enchant']
            stats_parts.append(f"Enchantment: {enchantment['name']} ({enchantment['type']} Damage: {enchantment['damage']}, Effect Chance: {enchantment['chance']}%)")
        else:
            if item.get('health_bonus', 0) > 0:
                stats_parts.append(f"Health: {item['health_bonus']}")
            if item.get('armor_bonus', 0) > 0:
                stats_parts.append(f"Armor: {item['armor_bonus']}")
            if item.get('attack_bonus', 0) > 0:
                stats_parts.append(f"Attack: {item['attack_bonus']}")
        stats = ' '.join(stats_parts)
        quantity = f"Quantity: {item['quantity']}"
        equipped_status = " (Equipped)" if item.get('equipped', False) else ""
        print(f"{index}. {item['name']} - {stats} - {quantity}{equipped_status}")

    print("0. Return to Main Menu")
    while True:
        choice = input("Select an item to use/equip or type '0' to return: ").strip()

        if choice == '0':
            print("Returning to main menu...")
            break
        elif choice.isdigit() and int(choice) in range(1, len(consolidated_inventory) + 1):
            selected_item = list(consolidated_inventory.values())[int(choice) - 1]
            handle_inventory_item(player, selected_item)  # Ensures that potions are used when selected
        else:
            print("Invalid choice. Please try again.")




def handle_inventory_item(player, item):
    if 'health_restored' in item or 'mana_restored' in item:
        use_potion(player, item)
    elif 'attack_bonus' in item or 'armor_bonus' in item:
        equip_gear(player, item)
    elif 'enchant' in item:
        use_enchantment(player, item)
    else:
        print("This item cannot be used.")

def use_potion(player, potion):
    health_restored_percentage = potion.get('health_restored', 0)
    mana_restored_percentage = potion.get('mana_restored', 0)

    # Adjust health and mana based on the potion's properties
    if health_restored_percentage > 0:
        player['health'] = min(get_player_max_health(), player['health'] + health_restored_percentage)
        print(f"You used {potion['name']}. Health restored by {health_restored_percentage}. Current health: {player['health']}")
    if mana_restored_percentage > 0:
        player['mana'] = min(get_player_max_mana(), player['mana'] + mana_restored_percentage)
        print(f"You used {potion['name']}. Mana restored by {mana_restored_percentage}. Current mana: {player['mana']}")

    # Update the quantity of the potion in inventory
    for inventory_item in player['inventory']:
        if inventory_item['name'] == potion['name']:
            inventory_item['quantity'] = inventory_item.get('quantity', 1)  # Ensure 'quantity' is set
            if inventory_item['quantity'] > 1:
                inventory_item['quantity'] -= 1
            else:
                player['inventory'].remove(inventory_item)
            break


def equip_gear(player, gear):
    for inventory_item in player['inventory']:
        if inventory_item['name'] == gear['name']:
            if inventory_item.get('equipped', False):
                # Unequip the gear
                if 'attack_bonus' in inventory_item:
                    player['attack'] -= inventory_item['attack_bonus']
                if 'armor_bonus' in inventory_item:
                    player['armor'] -= inventory_item['armor_bonus']
                if 'health_bonus' in inventory_item:
                    player['health'] -= inventory_item['health_bonus']
                inventory_item['equipped'] = False
                print(f"You unequipped {inventory_item['name']}.")
            else:
                # Equip the gear
                if 'attack_bonus' in inventory_item:
                    player['attack'] += inventory_item['attack_bonus']
                    print(f"You equipped {inventory_item['name']}. Attack increased by {inventory_item['attack_bonus']}. Current attack: {player['attack']}")
                if 'armor_bonus' in inventory_item:
                    player['armor'] += inventory_item['armor_bonus']
                    print(f"You equipped {inventory_item['name']}. Armor increased by {inventory_item['armor_bonus']}. Current armor: {player['armor']}")
                if 'health_bonus' in inventory_item:
                    player['health'] += inventory_item['health_bonus']
                    print(f"You equipped {inventory_item['name']}. Health increased by {inventory_item['health_bonus']}. Current health: {player['health']}")
                inventory_item['equipped'] = True
            return
    print("This gear is not in your inventory.")



def use_enchantment(enchantment):
    if 'enchant' in enchantment:
        for item in player['inventory']:
            if 'attack_bonus' in item and 'Sword' in item['name']:
                item_name = item['name']
                if item_name == "Azuregos, Blessed Blade of The Light":
                    # Apply enchantment effects but keep the original name
                    if enchantment['enchant'] == 'Fiery':
                        item['fire_damage'] = 1
                    elif enchantment['enchant'] == 'Conflagration':
                        item['fire_damage'] = 2
                    elif enchantment['enchant'] == 'Hellfire':
                        item['fire_damage'] = 3
                    elif enchantment['enchant'] == 'Frostbite':
                        item['frost_damage'] = 1
                    elif enchantment['enchant'] == 'Deep Freeze':
                        item['frost_damage'] = 2
                    elif enchantment['enchant'] == 'Absolute Zero':
                        item['frost_damage'] = 3
                    elif enchantment['enchant'] == 'Arcane Spark':
                        item['arcane_damage'] = 1
                    elif enchantment['enchant'] == 'Arcane Surge':
                        item['arcane_damage'] = 2
                    elif enchantment['enchant'] == 'Arcane Blast':
                        item['arcane_damage'] = 3
                    elif enchantment['enchant'] == "Crusader's Blessing":
                        item['holy_damage'] = 5
                    elif enchantment['enchant'] == "Crusader's Wrath":
                        item['holy_damage'] = 8
                    elif enchantment['enchant'] == "Crusader's Fury":
                        item['holy_damage'] = 12
                else:
                    # For other swords, rename them with the enchantment and apply effects
                    if enchantment['enchant'] == 'Fiery':
                        item['name'] = f"Fiery {item_name}"
                        item['fire_damage'] = 1
                    elif enchantment['enchant'] == 'Conflagration':
                        item['name'] = f"Conflagrated {item_name}"
                        item['fire_damage'] = 2
                    elif enchantment['enchant'] == 'Hellfire':
                        item['name'] = f"Hellfired {item_name}"
                        item['fire_damage'] = 3
                    elif enchantment['enchant'] == 'Frostbite':
                        item['name'] = f"Frostbitten {item_name}"
                        item['frost_damage'] = 1
                    elif enchantment['enchant'] == 'Deep Freeze':
                        item['name'] = f"Deep Frozen {item_name}"
                        item['frost_damage'] = 2
                    elif enchantment['enchant'] == 'Absolute Zero':
                        item['name'] = f"Absolute Zero {item_name}"
                        item['frost_damage'] = 3
                    elif enchantment['enchant'] == 'Arcane Spark':
                        item['name'] = f"Arcane Spark {item_name}"
                        item['arcane_damage'] = 1
                    elif enchantment['enchant'] == 'Arcane Surge':
                        item['name'] = f"Arcane Surge {item_name}"
                        item['arcane_damage'] = 2
                    elif enchantment['enchant'] == 'Arcane Blast':
                        item['name'] = f"Arcane Blast {item_name}"
                        item['arcane_damage'] = 3
                    elif enchantment['enchant'] == "Crusader's Blessing":
                        item['name'] = f"Blessed {item_name}"
                        item['holy_damage'] = 5
                    elif enchantment['enchant'] == "Crusader's Wrath":
                        item['name'] = f"Wrathful {item_name}"
                        item['holy_damage'] = 8
                    elif enchantment['enchant'] == "Crusader's Fury":
                        item['name'] = f"Furious {item_name}"
                        item['holy_damage'] = 12


# Boss Dialogue Function
def boss_dialogue(boss_name):
    if boss_name == "Goblin Warleader":
        print("Goblin Warleader: You think you can challenge the Goblin Warband?")
        print(
            "Fools like you have tried before, but now that the Light fades and the Ashen Rain darkens the skies, our strength grows!")
    elif boss_name == "Radakhan, Speaker of the Ash":
        print("Radakhan: You dare to interrupt our sacred rituals?")
        print("The Ashen Rain is a gift, a harbinger of the new world!")
        print(
            "The trolls will cleanse these lands under the falling ash, and you will be nothing but a sacrifice for our cause!")
    elif boss_name == "Gilgamash, Scourge of Humanity":
        print("Gilgamash: You dare enter my hall, human?")
        print("You think you can stop this? The Ashen Rain is beyond you.")
        print(
            "We have forsaken the old treaties, and under the dark sky, we orcs will forge a new era of blood and fire.")
        print("You will not live to see it!")
    elif boss_name == "Kael'Thuzad, the Everlasting Chill of the Void":
        print("Kael'Thuzad: Ah, a mortal fool thinks they can challenge me.")
        print("The Ashen Rain has brought power beyond imagination, resurrecting me from the abyss.")
        print(
            "The skies weep ashes because the void is merging with this plane, and soon all will serve under its chilling grasp.")
    elif boss_name == "Sal'Theron, Harbinger of the Ashen Rain":
        print("Sal'Theron: So, you are the one who has been meddling in my affairs.")
        print("The Ashen Rain is not merely a curse—it is my will, bending this plane to the Void.")
        print("You cannot stop the inevitable, mortal.")
        print("The Light has abandoned this world, and I shall see it consumed in ash and darkness!")


# Function to control bosses and handle their dialogue and loot
def handle_boss_encounter(final_boss):
    boss_dialogue(final_boss['name'])
    combat(final_boss)
    if player['health'] > 0:
        boss_loot(final_boss['name'])


# Function to provide clue loot to provide context to world and the plot line
def boss_loot(boss_name):
    loot = []
    if boss_name == "Goblin Warleader":
        loot = ["Goblin Warleader's Note"]
        print("You find a note on the Goblin Warleader.")
        print(
            "It reveals that the goblins were created by the Troll Cultists and hints at an alliance with the trolls in the nearby cavern.")
        print("This is a lead on where to travel next.")
    elif boss_name == "Radakhan, Speaker of the Ash":
        loot = ["Radakhan's Ritual Tome"]
        print("Radakhan drops a ritual tome.")
        print(
            "It mentions a powerful ally named Gilgamash in the Orc Encampment. This to you is strange knowing that Orcs despise honorless troll vermin...You must investigate this anomaly.")
        print("This is a lead on where to travel next.")
    elif boss_name == "Gilgamash, Scourge of Humanity":
        loot = ["Fragment of a Strange Note"]
        print("Gilgamash carried a fragment of a note.")
        print("It speaks of dark forces controlling the Orcs.")
        print("It also shows a location of a nearby lair, but what resides there?")
        print("This is a lead on where to travel next.")
    elif boss_name == "Kael'Thuzad, the Everlasting Chill of the Void":
        loot = ["Soul Jar"]
        print("After sifting through the Lich's Ashes you discover a Soul Jar.")
        print("There is a binding enchantment written on the Jar that only a powerful demon could create.")
        print("You call upon the light for guidance, and it is revealed to you who and where the creator is.")
        print("The Demon Lord Sal'Theron...")
        print("This is a lead on where to travel next.")
    elif boss_name == "Sal'Theron, Harbinger of the Ashen Rain":
        loot = ["Orb of the Void"]
        print("Sal'Theron dropped an orb pulsating with dark energy.")
        print("This is the key to stopping the Ashen Rain and restoring light to Alleria.")
        print("You call upon the light to cleanse and destroy the orb.")
        print("Holy fire encases your hands and destroys the orb.")
        print("The Ashen rain and the clouds that fill the sky begin to dissipate.")
        print("By the glory of the Light, you have finally cast out the darkness that encompassed Alleria.")


import random

# Ability menu while in combat; shows unlocked abilites and cooldown if ability used
def choose_ability():
    def display_abilities():
        print("\n--- Player Abilities ---")
        for index, ability in enumerate(player['abilities'], start=1):
            ability_name = ability.__name__
            description = abilities_info[ability_name]['description']
            cooldown = player['cooldowns'][ability_name]
            if cooldown > 0:
                print(f"{index}. {ability_name.replace('_', ' ').title()} (Cooldown: {cooldown} turns remaining) - {description}")
            else:
                print(f"{index}. {ability_name.replace('_', ' ').title()} - {description}")

    abilities_info = {
        'heroic_strike': {'description': 'A powerful melee attack that deals additional damage to multiple enemies.'},
        'holy_fire': {'description': 'Calls upon holy fire from the sky to deal significant damage and smite the enemy, reducing their effectiveness.'},
        'lights_vengeance': {'description': 'Deals damage to all enemies and smites them, reducing their combat abilities.'},
        'summon_lights_protector': {'description': 'Summons a powerful protector with unique abilities to aid in combat, including stun and taunt effects.'},
        'summon_archangels_of_light': {'description': 'Summons three archangels with strong attacks and supportive abilities to assist in battle.'}
    }

    display_abilities()
    choice = input("Enter the number of the ability to use: ").strip()
    if choice.isdigit() and 1 <= int(choice) <= len(player['abilities']):
        selected_ability = player['abilities'][int(choice) - 1]
        if player['cooldowns'][selected_ability.__name__] == 0:
            ability_damage, ability_effect = selected_ability()
            player['cooldowns'][selected_ability.__name__] = abilities_info[selected_ability.__name__].get('cooldown', 1)
            return ability_damage, ability_effect
        else:
            print("That ability is on cooldown. Using basic attack instead.")
            return 0, None
    else:
        print("Invalid choice. Using basic attack instead.")
        return 0, None   # Return no damage and no effect if an invalid choice is made


# Implementation of decrement_cooldowns
def decrement_cooldowns():
    for key in player['cooldowns']:
        if player['cooldowns'][key] > 0:
            player['cooldowns'][key] -= 1


def combat(enemy):
    # Boss dialogue before combat begins
    if "name" in enemy and enemy['name'] in ["Goblin Warleader", "Radakhan, Speaker of the Ash",
                                             "Gilgamash, Scourge of Humanity",
                                             "Kael'Thuzad, the Everlasting Chill of the Void",
                                             "Sal'Theron, Harbinger of the Ashen Rain"]:
        boss_dialogue(enemy['name'])

    while enemy['health'] > 0 and player['health'] > 0:
        # If it's a boss, give dialogue based on health thresholds
        if "name" in enemy and enemy['name'] in ["Goblin Warleader", "Radakhan, Speaker of the Ash",
                                                 "Gilgamash, Scourge of Humanity",
                                                 "Kael'Thuzad, the Everlasting Chill of the Void",
                                                 "Sal'Theron, Harbinger of the Ashen Rain"]:
            if enemy['health'] < (enemy['max_health'] * 0.5) and not enemy.get('dialogue_50%', False):
                # Boss-specific mid-fight dialogues
                print(f"{enemy['name']}: You will not defeat me!")
                enemy['dialogue_50%'] = True

        # Player's turn to attack or use ability
        while True:
            print("\n--- Your Turn ---")
            action = input(
                "Do you want to use an ability, attack, or open the menu? (ability/attack/menu): ").strip().lower()

            if action == 'menu':
                show_dungeon_menu_in_combat()
                continue  # Allow player to make another decision after viewing the menu
            elif action == 'ability':
                use_ability = True
                break
            elif action == 'attack':
                use_ability = False
                break
            else:
                print("Invalid choice. Please type 'ability', 'attack', or 'menu'.")

        if use_ability:
            # Allow summoning during combat if the player is at the required level
            if player['level'] >= 8:
                summon_choice = input(
                    "Do you want to summon Light's Protector or Archangels of Light? (yes/no): ").strip().lower()
                if summon_choice == 'yes':
                    if player['level'] >= 8 and player['cooldowns']['summon_lights_protector'] == 0 and not player.get(
                            'summoned_lights_protector_used', False):
                        summon_lights_protector()
                        player['summoned_lights_protector_used'] = True
                        player['summoned_lights_protector'] = True
                    elif player['level'] >= 10 and player['cooldowns'][
                        'summon_archangels_of_light'] == 0 and not player.get('summoned_archangels_used', False):
                        summon_archangels_of_light()
                        player['summoned_archangels_used'] = True
                        player['summoned_archangels'] = True
                    else:
                        print(
                            "You cannot summon now. Either the ability is on cooldown or it has already been used once this combat.")
                        print("Summons can only be used once per combat.")
                else:
                    ability_damage, ability_effect = choose_ability()
                    if ability_damage > 0:
                        effective_damage = max(ability_damage - enemy['armor'], 0)
                        enemy['health'] -= effective_damage
                        print(
                            f"You deal {effective_damage} damage to the {enemy['name']} using an ability. Remaining health: {enemy['health']}")
                        if ability_effect == 'stun':
                            enemy['stunned'] = 1
            else:
                # If player is not at level 8 or above, proceed with other abilities
                ability_damage, ability_effect = choose_ability()
                if ability_damage > 0:
                    effective_damage = max(ability_damage - enemy['armor'], 0)
                    enemy['health'] -= effective_damage
                    print(
                        f"You deal {effective_damage} damage to the {enemy['name']} using an ability. Remaining health: {enemy['health']}")
                    if ability_effect == 'stun':
                        enemy['stunned'] = 1
        else:
            # Basic attack if no ability is used
            base_damage = random.randint(5, 10)
            if random.random() < 0.3:
                damage = (player['attack'] + base_damage) * 2
                print("Critical hit!")
            else:
                damage = player['attack'] + base_damage

            effective_damage = max(damage - enemy['armor'], 0)
            enemy['health'] -= effective_damage
            print(
                f"You deal {effective_damage} damage to the {enemy['name']}. Remaining health: {max(0, enemy['health'])}")

            # Apply enchantment effects if weapon is enchanted
            if 'enchantments' in player:
                for enchantment in player['enchantments']:
                    if enchantment['type'] == 'fire' and random.randint(1, 100) <= enchantment['chance']:
                        enemy['health'] -= enchantment['burn_damage']
                        print(f"The {enemy['name']} takes {enchantment['burn_damage']} fire damage from burning!")
                    elif enchantment['type'] == 'frost' and random.randint(1, 100) <= enchantment['chance']:
                        enemy['stunned'] = 1
                        print(f"The {enemy['name']} is frozen and cannot move!")
                    elif enchantment['type'] == 'arcane' and random.randint(1, 100) <= enchantment['chance']:
                        enemy['mana'] = max(enemy.get('mana', 0) - 10, 0)
                        print(f"The {enemy['name']} loses 10 mana from arcane burn!")
                    elif enchantment['type'] == 'holy' and random.randint(1, 100) <= enchantment['chance']:
                        heal_amount = enchantment['damage']
                        player['health'] = min(player['max_health'], player['health'] + heal_amount)
                        print(f"You heal for {heal_amount} health from holy enchantment!")

            # Apply special item effects
            if 'Malegos, Protector of the Light' in [item['name'] for item in player['inventory']]:
                if random.random() < 0.2:
                    reflected_damage = effective_damage * 0.5
                    enemy['health'] -= reflected_damage
                    print(f"The {enemy['name']} takes {reflected_damage} damage from Malegos' reflection!")

            if 'Azuregos, Blessed Blade of The Light' in [item['name'] for item in player['inventory']]:
                if random.random() < 0.2:
                    smite_damage = 20
                    enemy['health'] -= smite_damage
                    print(f"Azuregos smites the {enemy['name']} for {smite_damage} holy damage!")

        # Handle Light's Protector's turn
        if player.get('summoned_lights_protector'):
            print(f"\n--- Light's Protector's Turn ---")
            control_lights_protector()

        # Handle Archangels' turn
        if player.get('summoned_archangels'):
            print(f"\n--- Archangels' Turn ---")
            control_archangels()

        if enemy['health'] <= 0:
            print(f"You have defeated the {enemy['name']}!")
            player['gold'] += enemy['gold_reward']
            player['experience'] += enemy['xp_reward']
            print(f"You have gained {enemy['xp_reward']} experience points and {enemy['gold_reward']} gold!")
            level_up()
            break

        # Enemy's turn to attack or use ability
        if 'stunned' not in enemy or enemy['stunned'] == 0:
            enemy_damage = random.randint(10, 20) + enemy['attack']
            effective_enemy_damage = max(enemy_damage - player['armor'], 0)
            player['health'] -= effective_enemy_damage
            print(
                f"The {enemy['name']} deals {effective_enemy_damage} damage to you. Your remaining health: {max(0, player['health'])}")
        elif enemy['stunned'] > 0:
            enemy['stunned'] -= 1
            print(f"The {enemy['name']} is stunned and cannot attack this turn.")

        if player['health'] <= 0:
            print("You have been defeated!")
            player['in_hope_end'] = True
            print("You return to Hope's End.")
            break

    # Reset summoned creatures after combat ends
    player['summoned_lights_protector'] = None
    player['summoned_archangels'] = None
    player['summoned_lights_protector_used'] = False
    player['summoned_archangels_used'] = False


# Function to clear a room and give the player a choice to continue or go to the main menu
def clear_room():
    print("You have cleared the room!")
    while True:
        choice = input(
            "Would you like to continue to the next room or open the menu? (Type 'continue' to proceed or 'menu' to open the menu): ").strip().lower()
        if choice == 'continue':
            break
        elif choice == 'menu':
            # Display the dungeon menu and allow the player to perform actions
            show_dungeon_menu()
        else:
            print("Invalid choice. Please type 'continue' or 'menu'.")


def explore_goblin_caves():
    print("\nEntering the Goblin Caves...")
    for room_number, room_data in goblin_caves_rooms.items():
        # Show room description
        if room_number == 1:
            room_data['description'] = (
                "You enter The Fungal Hollow.\n"
                "The Fungal Hollow is damp and dark.\n"
                "The air is thick with the musty odor of wet earth and rotting vegetation.\n"
                "Stalactites hang precariously from the ceiling, dripping water into small puddles that dot the uneven stone floor.\n"
                "The walls are lined with faintly glowing fungi, casting a sickly green light that barely illuminates the room.\n"
                "Shadows dance in the corners, and you hear the faint rustle of unseen creatures.\n"
                "A chill runs down your spine as you step further into the gloom, your footsteps echoing off the stone walls."
            )
        elif room_number == 2:
            room_data['description'] = (
                "You enter The Echoing Chamber.\n"
                "The Echoing Chamber is larger and colder.\n"
                "The walls are covered in crude goblin carvings, depicting chaotic scenes of battle and celebration.\n"
                "Bones and remnants of past victims are scattered across the floor, crunching underfoot as you move.\n"
                "The distant sound of goblin laughter echoes through the tunnels, making your heart pound.\n"
                "A flickering torch lies discarded in one corner, its light casting fleeting shadows that make the carvings seem almost alive.\n"
                "The sense of danger is palpable, and every instinct tells you to turn back, but you press on."
            )
        elif room_number == 3:
            room_data['description'] = (
                "You enter The Altar of Blood.\n"
                "The Altar of Blood is a grim, oppressive space that feels almost alive with dark energy.\n"
                "The walls are splattered with old, dried blood, and strange symbols have been scratched into the stone.\n"
                "Symbols that seem to hum faintly with a dark power.\n"
                "A crude altar stands in the middle of the room, adorned with bones and rotting offerings.\n"
                "The air is thick and suffocating, carrying the scent of decay.\n"
                "As you step closer, the flickering torchlight reveals several goblins crouched in the shadows, their eyes glinting with malice.\n"
                "You can hear their low growls as they prepare to attack."
            )
        elif room_number == 4:
            room_data['description'] = (
                "You enter The Crystal Cavern.\n"
                "The Crystal Cavern is a cavernous chamber with jagged stone walls and a high ceiling that seems to stretch endlessly into darkness.\n"
                "The air is cold and damp, and the floor is littered with broken weapons, shattered shields, and old goblin totems.\n"
                "Strange glowing crystals are embedded in the walls, casting a dim, ethereal blue light that makes the shadows seem to dance and sway.\n"
                "You hear the guttural murmurs of goblins before you even see them.\n"
                "There are many, their eyes reflecting the eerie glow as they step out from the shadows, weapons raised and ready for battle."
            )
        elif room_number == 5:
            room_data['description'] = (
                "You enter The Warleader's Sanctum.\n"
                "The Warleader's Sanctum is vast, with a high ceiling that disappears into darkness.\n"
                "Torches line the walls, their flickering flames barely providing enough light to see.\n"
                "In the center of the room stands the Goblin Warleader, a hulking figure adorned in makeshift armor crafted from bones and scraps of metal.\n"
                "His eyes glow with a dangerous intensity, and he grips a massive, jagged blade.\n"
                "Around him, a circle of goblin skulls rests on the ground, each one marked with strange, glowing runes.\n"
                "The air is thick with the scent of sulfur and blood, and an eerie silence falls over the room as the Warleader fixes his gaze on you.\n"
                "A growl rumbling from deep within his chest."
            )
        print(f"\nRoom {room_number}:\n{room_data['description']}")

        # Engage each creature in combat
        for creature in room_data['creatures']:
            print(f"A {creature['name']} appears with {creature['health']} health!")
            combat(creature)
            if player['health'] <= 0:
                print("You have been defeated. Returning to Hope's End...")
                player['in_hope_end'] = True
                return

        # Room cleared
        print(f"\nYou have cleared Room {room_number} of the Goblin Caves!")

        # Call clear_room function at the end of each room, except the final room
        if room_number != max(goblin_caves_rooms.keys()):
            clear_room()  # End of the dungeon, encounter Goblin Warleader

    final_room = goblin_caves_rooms[max(goblin_caves_rooms.keys())]
    final_boss = final_room['creatures'][0]
    print(f"\nFinal Challenge: {final_boss['name']} appears with {final_boss['health']} health!")
    combat(final_boss)
    if player['health'] > 0:
        print("\nCongratulations! You have conquered the Goblin Caves and defeated the Goblin Warleader!")
        player['experience'] += final_boss['xp_reward']
        player['gold'] += final_boss['gold_reward']
        level_up()
    else:
        print("You have been defeated by the Goblin Warleader. Returning to Hope's End...")
        player['in_hope_end'] = True


# Update room definitions with more goblins in each room

goblin_caves_rooms = {
    1: {
        "description": "",
        "creatures": [goblin()]
    },
    2: {
        "description": "",
        "creatures": [goblin(), goblin()]
    },
    3: {
        "description": "",
        "creatures": [goblin(), goblin(), goblin()]
    },
    4: {
        "description": "",
        "creatures": [goblin(), goblin(), goblin(), goblin()]
    },
    5: {
        "description": "",
        "creatures": [goblin_warleader()]
    }
}


def explore_troll_caverns():
    print("\nEntering the Troll Caverns...")
    for room_number, room_data in troll_cavern_rooms.items():
        # Show room description
        if room_number == 1:
            room_data['description'] = (
                "You enter The Shadowed Hollow. The Shadowed Hollow is filled with thick shadows that seem to shift and move. "
                "The walls are rough, covered in strange etchings that glow faintly in the dark. The air is damp, carrying the "
                "scent of mildew and something metallic, like blood. You hear distant chanting echoing through the corridors, "
                "and the ground beneath your feet is uneven, forcing you to step carefully."
            )
        elif room_number == 2:
            room_data['description'] = (
                "You enter The Bloodstone Chamber. The walls of this chamber are covered in blood-red crystals that pulse with a dull light. "
                "The air is heavy, and an unsettling energy fills the room. Bones are scattered across the floor, and you hear the deep, guttural "
                "laugh of trolls echoing through the chamber. Shadows flicker across the walls, making it hard to tell where the trolls might be hiding."
            )
        elif room_number == 3:
            room_data['description'] = (
                "You enter The Ritual Grounds. The Ritual Grounds are a grim space, with dark symbols painted in blood on the walls and floor. "
                "Several stone pillars are arranged in a circle, each adorned with crude offerings—bones, trinkets, and what looks like human remains. "
                "In the center of the room, a group of Troll Cultists are gathered, their eyes glowing with an unnatural light as they chant in unison."
            )
        elif room_number == 4:
            room_data['description'] = (
                "You enter The Forsaken Den. The Forsaken Den is a cold, oppressive space. The walls are covered in thick, dark moss, and the air is frigid, "
                "making each breath visible. Broken weapons and shattered shields are scattered across the floor, remnants of past battles. "
                "You hear the distant growls of trolls, and the atmosphere is filled with an eerie sense of foreboding."
            )
        elif room_number == 5:
            room_data['description'] = (
                "You enter The Obsidian Hall. The Obsidian Hall is an imposing room with high ceilings, the walls lined with black, glass-like stone. "
                "The floor is covered in jagged obsidian shards, and the air is thick with the scent of sulfur. Torches burn with a green flame, casting "
                "shadows that seem to dance across the walls. You can feel a powerful presence nearby, as if the very room is alive with dark energy."
            )
        elif room_number == 6:
            room_data['description'] = (
                "You enter The Radakhan, Speaker of the Ash’s Court. Speaker's Ashen Court is dimly lit by flickering torches. The walls are covered in crude "
                "tapestries depicting scenes of battle and dark rituals. At the far end of the room, a massive stone throne sits atop a raised platform, "
                "occupied by the Radakhan, Speaker of the Ash. His eyes glint with malice as he rises, his massive frame casting a shadow over the entire room."
            )
        print(f"\nRoom {room_number}:\n{room_data['description']}")

        # Engage each creature in combat
        for creature in room_data['creatures']:
            print(f"A {creature['name']} appears with {creature['health']} health!")
            combat(creature)
            if player['health'] <= 0:
                print("You have been defeated. Returning to Hope's End...")
                player['in_hope_end'] = True
                return

        # Room cleared
        print(f"\nYou have cleared Room {room_number} of the Troll Caverns!")

        # Call clear_room function at the end of each room, except the final room
        if room_number != max(goblin_caves_rooms.keys()):
            clear_room()  # End of the dungeon, encounter Goblin Warleader

    # End of the dungeon, encounter Radakhan, Speaker of the Ash
    final_room = troll_cavern_rooms[max(troll_cavern_rooms.keys())]
    final_boss = final_room['creatures'][0]
    print(f"\nFinal Challenge: {final_boss['name']} appears with {final_boss['health']} health!")
    combat(final_boss)
    if player['health'] > 0:
        print("\nCongratulations! You have conquered the Troll Caverns and defeated the Radakhan, Speaker of the Ash!")
        player['experience'] += final_boss['xp_reward']
        player['gold'] += final_boss['gold_reward']
        level_up()
    else:
        print("You have been defeated by the Radakhan, Speaker of the Ash. Returning to Hope's End...")
        player['in_hope_end'] = True


# Define rooms for Troll Caverns
troll_cavern_rooms = {
    1: {
        "description": "",
        "creatures": [troll_cultist()]
    },
    2: {
        "description": "",
        "creatures": [troll_cultist(), troll_cultist()]
    },
    3: {
        "description": "",
        "creatures": [troll_cultist(), troll_cultist(), troll_cultist()]
    },
    4: {
        "description": "",
        "creatures": [troll_cultist(), troll_cultist(), troll_cultist(), troll_cultist()]
    },
    5: {
        "description": "",
        "creatures": [troll_cultist(), troll_cultist(), troll_cultist(), troll_cultist(), troll_cultist()]
    },
    6: {
        "description": "",
        "creatures": [radakhan()]
    }
}


# Define rooms for Orc Encampment
def explore_orc_encampment():
    print("\nEntering the Orc Encampment...")
    for room_number, room_data in orc_encampment_rooms.items():
        # Show room description
        if room_number == 1:
            room_data['description'] = (
                "You enter The Battle Tents. The Battle Tents are filled with the smell of sweat and steel. "
                "Rough-hewn tents line the area, with orc warriors sharpening their blades. The clanging of metal and "
                "the guttural conversations in the harsh orcish language make this a dangerous place to be."
            )
        elif room_number == 2:
            room_data['description'] = (
                "You enter The Warchief's Training Grounds. The Training Grounds are an open field where orc warriors "
                "practice their combat skills. Large wooden dummies and piles of discarded weapons litter the area. "
                "You can hear the harsh barks of a Warchief commanding his soldiers."
            )
        elif room_number == 3:
            room_data['description'] = (
                "You enter The Forge of the Ancients. The Forge is a sacred place to the orcs, where they craft their weapons "
                "and armor. The air is hot and filled with smoke. Massive anvils are scattered across the area, with orc "
                "blacksmiths hammering away, creating weapons for battle."
            )
        elif room_number == 4:
            room_data['description'] = (
                "You enter The Sacred Shrine. The Shrine is a place of deep reverence. The walls are adorned with carvings "
                "of past battles and the orc gods. A powerful orc shaman stands before the shrine, chanting to the spirits."
            )
        elif room_number == 5:
            room_data['description'] = (
                "You enter The Barracks. The Barracks are crowded with orc soldiers resting and preparing for battle. The "
                "air is tense, and you can see multiple orc warriors sharpening their weapons, ready to defend their encampment."
            )
        elif room_number == 6:
            room_data['description'] = (
                "You enter The Blood Pit. This is where orcs test their strength in brutal combat against each other. The ground "
                "is stained with blood, and the roars of the crowd echo as orc warriors fight ferociously to prove themselves."
            )
        elif room_number == 7:
            room_data['description'] = (
                "You enter The War Council Chamber. This is where the orc leaders gather to discuss their battle plans. A large "
                "table stands in the center, covered in maps and war markers. Several orc warleaders are present, their eyes "
                "narrowing as they notice your presence."
            )
        elif room_number == 8:
            room_data['description'] = (
                "You enter The Warchief's Hall. It is an intimidating room, with a high ceiling and walls covered in war banners."
                " In the center stands Gilgamash, Scourge of Humanity. His massive form looms over everything."
                " His eyes are filled with fury, and he grips a massive war axe."
            )

        print(f"\nRoom {room_number}:{room_data['description']}")

        # Engage each creature in combat
        for creature in room_data['creatures']:
            print(f"A {creature['name']} appears with {creature['health']} health!")
            combat(creature)
            if player['health'] <= 0:
                print("You have been defeated. Returning to Hope's End...")
                player['in_hope_end'] = True
                return

        # Room cleared
        print(f"\nYou have cleared Room {room_number} of the Orc Encampment!")

        # Call clear_room function at the end of each room, except the final room
        if room_number != max(orc_encampment_rooms.keys()):
            clear_room()

    # End of the dungeon, encounter Orc Warchief
    final_room = orc_encampment_rooms[max(orc_encampment_rooms.keys())]
    final_boss = final_room['creatures'][0]
    print(f"\nFinal Challenge: {final_boss['name']} appears with {final_boss['health']} health!")
    combat(final_boss)
    if player['health'] > 0:
        print("\nCongratulations! You have conquered the Orc Encampment and defeated Gilgamesh, Scourge of Humanity!")
        player['experience'] += final_boss['xp_reward']
        player['gold'] += final_boss['gold_reward']
        level_up()
    else:
        print("You have been defeated by Gilgamesh, Scourge of Humanity. Returning to Hope's End...")
        player['in_hope_end'] = True


orc_encampment_rooms = {
    1: {
        "description": "",
        "creatures": [orc_warrior()]
    },
    2: {
        "description": "",
        "creatures": [orc_warrior(), orc_warrior()]
    },
    3: {
        "description": "",
        "creatures": [orc_warrior(), orc_warrior(), orc_shaman()]
    },
    4: {
        "description": "",
        "creatures": [orc_shaman(), orc_shaman(), orc_warrior(), orc_warrior()]
    },
    5: {
        "description": "",
        "creatures": [orc_warrior(), orc_warrior(), orc_warrior(), orc_shaman(), orc_shaman()]
    },
    6: {
        "description": "",
        "creatures": [orc_warrior(), orc_warrior(), orc_shaman(), orc_shaman(), orc_warrior(), orc_warrior()]
    },
    7: {
        "description": "",
        "creatures": [orc_warrior(), orc_shaman(), orc_warrior(), orc_warrior(), orc_shaman(), orc_warrior(),
                      orc_warrior()]
    },
    8: {
        "description": "",
        "creatures": [gilgamash()]
    }
}


# Define rooms for Lich's Lair
def explore_lich_lair():
    print("\nEntering the Lich's Lair...")
    for room_number, room_data in lich_lair_rooms.items():
        # Show room description
        if room_number == 1:
            room_data['description'] = (
                "You enter The Haunted Vestibule. The air is thick with the stench of decay. Shadows flicker across the cracked stone walls, "
                "and eerie whispers seem to echo from nowhere. The atmosphere is oppressive, and a feeling of dread creeps over you."
            )
        elif room_number == 2:
            room_data['description'] = (
                "You enter The Hall of the Damned. The walls are lined with grotesque statues of undead creatures. The floor is littered with "
                "old bones, and an eerie green mist swirls across the ground. The faint sounds of distant moans can be heard, sending chills down your spine."
            )
        elif room_number == 3:
            room_data['description'] = (
                "You enter The Necrotic Laboratory. Strange alchemical tools and bubbling cauldrons are scattered across stone tables. "
                "The room reeks of strange chemicals, and half-formed skeletons lie in various stages of assembly. Dark runes glow dimly on the walls."
            )
        elif room_number == 4:
            room_data['description'] = (
                "You enter The Crypt of Whispers. Rows of sarcophagi line the walls, their lids partially open as if disturbed. "
                "The air is cold, and your breath fogs as you move. Whispers seem to emanate from the sarcophagi, urging you to turn back."
            )
        elif room_number == 5:
            room_data['description'] = (
                "You enter The Chamber of Souls. Spectral figures drift through the air, their hollow eyes watching your every move. "
                "A cold wind swirls through the room, carrying with it the faint cries of the damned. The walls are adorned with ancient sigils that glow faintly."
            )
        elif room_number == 6:
            room_data['description'] = (
                "You enter The Bone Pile Cavern. The floor is covered in heaps of bones, and the ceiling is lost in darkness. "
                "The bones shift and crunch underfoot as you move, and you hear the unsettling sound of them shifting on their own."
            )
        elif room_number == 7:
            room_data['description'] = (
                "You enter The Shadowed Hallway. The light seems to be swallowed by the darkness here. "
                "Shapes move just out of sight, and a sense of imminent danger hangs in the air."
            )

        elif room_number == 8:
            room_data['description'] = (
                "You enter The Forgotten Library. Rows upon rows of ancient books and scrolls line the walls, "
                "many of them covered in cobwebs. A strange, pulsating light glows from a cracked crystal set into the ceiling. "
                "The air is heavy with the weight of forgotten knowledge, and you can almost hear the voices of scholars long gone."
            )
        elif room_number == 9:
            room_data['description'] = (
                "You enter The Lich's Throne Room. A massive, ornate throne stands against the far wall, covered in dark runes that pulse with energy. "
                "The Lich, Kael'Thuzad, the Everlasting Chill of the Void, stands before it, his skeletal form emanating a chilling aura."
            )
        print(f"\nRoom {room_number}: {room_data['description']}")

        # Engage each creature in combat
        for creature in room_data['creatures']:
            print(f"A {creature['name']} appears with {creature['health']} health!")
            combat(creature)
            if player['health'] <= 0:
                print("You have been defeated. Returning to Hope's End...")
                player['in_hope_end'] = True
                return

        # Room cleared
        print(f"\nYou have cleared Room {room_number} of the Lich's Lair!")

        # Call clear_room function at the end of each room, except the final room
        if room_number != max(lich_lair_rooms.keys()):
            clear_room()

    # End of the dungeon, encounter the Lich
    final_room = lich_lair_rooms[max(lich_lair_rooms.keys())]
    final_boss = final_room['creatures'][0]
    print(f"\nFinal Challenge: {final_boss['name']} appears with {final_boss['health']} health!")
    combat(final_boss)
    if player['health'] > 0:
        print(
            "\nCongratulations! You have conquered the Lich's Lair and defeated Kael'Thuzad, the Everlasting Chill of the Void!")
        player['experience'] += final_boss['xp_reward']
        player['gold'] += final_boss['gold_reward']
        level_up()
    else:
        print("You have been defeated by Kael'Thuzad. Returning to Hope's End...")
        player['in_hope_end'] = True


lich_lair_rooms = {
    1: {
        "description": "",
        "creatures": [skeleton()]
    },
    2: {
        "description": "",
        "creatures": [skeleton(), skeleton()]
    },
    3: {
        "description": "",
        "creatures": [skeleton(), skeleton(), skeleton()]
    },
    4: {
        "description": "",
        "creatures": [skeleton(), skeleton(), skeleton(), skeleton()]
    },
    5: {
        "description": "",
        "creatures": [skeleton(), skeleton(), skeleton(), skeleton(), skeleton()]
    },
    6: {
        "description": "",
        "creatures": [skeleton(), skeleton(), skeleton(), skeleton(), skeleton(), skeleton()]
    },
    7: {
        "description": "",
        "creatures": [skeleton(), skeleton(), skeleton(), skeleton(), skeleton(), skeleton(), skeleton()]
    },
    8: {
        "description": "",
        "creatures": [skeleton(), skeleton(), skeleton(), skeleton(), skeleton(), skeleton(), skeleton(), skeleton()]
    },
    9: {
        "description": "The Lich's Throne Room.",
        "creatures": [kaelthuzad()]
    }
}


def explore_throne_of_saltheron():
    print("\nEntering the Throne of Sal'Theron, Harbinger of the Ashen Rain...")
    for room_number in range(1, 12):
        # Generate room description based on floor number
        if room_number == 1:
            room_description = (
                "You stand at the base of the Ziggurat, staring up at the enormous, crumbling structure. "
                "The dark stone is etched with glowing, malevolent runes, pulsating with demonic energy. "
                "The oppressive atmosphere radiates from the ziggurat, as if the entire structure is possessed by a dark force. "
                "A sense of dread fills you as you take in the sheer size of the ziggurat, which stretches almost a mile into the sky. "
                "You can feel the demonic void energies emanating from it, urging you to turn back. But you press on, determined to face whatever awaits within."
            )
        elif room_number == 2:
            room_description = (
                "You climb 400 yards up the side of the Ziggurat. The path is narrow, and the stones beneath your feet feel loose. "
                "The wind howls around you, carrying with it the faint screams of lost souls. The energy in the air is palpable, "
                "each breath you take seeming to pull more of the darkness into your lungs. You press on, wary of every step."
            )
        elif room_number == 3:
            room_description = (
                "You ascend another 800 yards. The dark stone stairs are slick with some unknown, viscous substance. "
                "The oppressive demonic presence grows stronger, and strange, ghostly figures seem to flicker at the edges of your vision. "
                "The path ahead twists sharply, and you know that a single misstep could send you hurtling into the void below."
            )
        elif room_number == 4:
            room_description = (
                "You have now climbed 1,200 yards. The atmosphere becomes even heavier, and the void energies seem to be pressing against you from all sides. "
                "The dark whispers have grown louder, and the sensation of being watched is almost unbearable. "
                "The ziggurat seems to be testing your resolve, daring you to continue upwards."
            )
        elif room_number == 5:
            room_description = (
                "You climb to 1,600 yards. The sky above is obscured by swirling black clouds, and flashes of eerie green lightning illuminate the path. "
                "You can feel the malevolence of the ziggurat, and the dark power within it seems to seep into your very bones. "
                "The journey is exhausting, both physically and mentally, but you press on, driven by determination."
            )
        elif room_number == 6:
            room_description = (
                "You reach 2,000 yards. The steps have become narrower, and the wind threatens to knock you off balance. "
                "The dark energy is overwhelming, and you can feel it trying to worm its way into your thoughts, filling your mind with despair. "
                "You focus on the summit, pushing forward despite the relentless assault on your spirit."
            )
        elif room_number == 7:
            room_description = (
                "You ascend to 2,400 yards. The air is thick with the stench of sulfur, and the path is littered with charred remains. "
                "The void energies pulse rhythmically, almost like a heartbeat, and the walls of the ziggurat seem to move and shift as if alive. "
                "You can hear the distant growls of demonic entities, and you know that the trials ahead will only grow more difficult."
            )
        elif room_number == 8:
            room_description = (
                "You climb to 2,800 yards. The oppressive energy seems to weigh down on you more than ever, and each step feels like a monumental effort. "
                "The swirling darkness around you seems to close in, and the whispers have become a cacophony of voices, taunting you to turn back. "
                "You push forward, refusing to give in to the fear and doubt."
            )
        elif room_number == 9:
            room_description = (
                "You reach 3,200 yards. The demonic energy is so intense that it feels like the air is vibrating. "
                "The path is treacherous, with jagged stones jutting out at odd angles. You can see strange symbols carved into the stone, glowing faintly with a dark light. "
                "The sense of danger is overwhelming, but you keep moving, knowing that the summit is drawing closer."
            )
        elif room_number == 10:
            room_description = (
                "You ascend to 3,600 yards. The summit is now visible above you, though still distant. The dark haze that surrounds it seems impenetrable. "
                "The path is almost nonexistent, with only a narrow ledge to walk on. The void energies pulse with a sinister rhythm, and you can feel your resolve being tested. "
                "Every step is a challenge, but you are determined to see this through."
            )
        elif room_number == 11:
            room_description = (
                "You reach 4,000 yards, the final stretch before the summit. The air is thick with malevolence, and the very stones beneath your feet seem to hum with dark power. "
                "The whispers have become deafening, and you feel the weight of countless eyes watching your every move. The summit looms above, the Throne of Sal'Theron waiting for you. "
                "With one last deep breath, you steel yourself for what lies ahead."
            )
        print(f"\nYard {room_number * 400 // 11}: {room_description}")

        # Determine number of demons in the area
        demon_count = room_number
        demons = [demon() for _ in range(demon_count)]

        # Engage each demon in combat
        for idx, demon_instance in enumerate(demons, start=1):
            print(
                f"A {demon_instance['name']} appears with {demon_instance['health']} health! (Demon {idx} of {demon_count})")
            combat(demon_instance)
            if player['health'] <= 0:
                print("You have been defeated. Returning to Hope's End...")
                player['in_hope_end'] = True
                return

        # Area cleared
        print(f"\nYou have cleared {room_number * 400 // 11} yards of the Ziggurat!")

        # Call clear_room function at the end of each area, except the final area
        if room_number != 11:
            clear_room()

    # End of the dungeon, encounter Demon Lord Sal'Theron
    final_boss = saltheron()
    print(f"\nFinal Challenge: {final_boss['name']} appears with {final_boss['health']} health!")
    combat(final_boss)
    if player['health'] > 0:
        print(
            "\nCongratulations! You have conquered the Throne of Sal'Theron and defeated Sal'Theron, Harbinger of the Ashen Rain!")
        player['experience'] += final_boss['xp_reward']
        player['gold'] += final_boss['gold_reward']
        level_up()
    else:
        print("You have been defeated by Sal'Theron. Returning to Hope's End...")
        hero_name = player.get('name', 'Hero')
        print(
            f"You have done it, {hero_name}! You have overthrown the demon lord and have purged Alleria from the Ashen Rain and the clouds that have blocked the sun for decades! "
            f"Your name will be recorded in legend for centuries to come, and no matter where you venture next, you will be lauded as a true champion of the light!")
        # Ask if player wants to start a new game or exit
        while True:
            choice = input("Would you like to start a new game or exit? (new/exit): ").strip().lower()
            if choice == 'new':
                print("Starting a new game...")
                # Code to start a new game would go here
                break
            elif choice == 'exit':
                print("Exiting the game. Farewell, champion!")
                break
            else:
                print("Invalid choice. Please type 'new' to start a new game or 'exit' to exit the game.")
        player['in_hope_end'] = True


# Main function to start the game
def main():
    show_menu()


# Entry Point
if __name__ == "__main__":
    main()