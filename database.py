import csv
import json
import random

from pprint import pprint

from constants import *

ITEM_TYPES_FILE = "data/diablo/ItemTypes.tsv"
ARMOR_FILE = "data/diablo/Armor.tsv"
WEAPONS_FILE = "data/diablo/Weapons.tsv"
MAGIC_PREFIX_FILE = "data/diablo/MagicPrefix.tsv"
MAGIC_SUFFIX_FILE = "data/diablo/MagicSuffix.tsv"

ITEM_TYPE_COLUMNS = ("Code", "Equiv1", "Equiv2")
MAGIC_COLUMNS = ("itype1", "itype2", "itype3", "itype4", "itype5", "itype6", "itype7")
INVALID_NAMES = ("null", "blank")

def load_item_types(source_file, columns):
    item_types = {}

    with open(source_file, "r") as f:
        reader = csv.DictReader(f, delimiter="\t")

        for item in reader:
            for column in columns:
                item_code = item.get(column).strip()

                if len(item_code) == 0:
                    continue

                item_types[item_code] = item

    return item_types

def load_items(source_file):
    items = []

    with open(source_file, "r") as f:
        reader = csv.DictReader(f, delimiter="\t")

        for item in reader:
            item_name = item.get("name").strip()
            item_type = item.get("type").strip()

            if len(item_name) == 0 or item_name in INVALID_NAMES:
                continue

            if len(item_type) == 0:
                continue

            items.append(item)

    return items

def load_item_addons(source_file, columns):
    item_addons = {}

    with open(source_file, "r") as f:
        reader = csv.DictReader(f, delimiter="\t")

        for addon in reader:
            addon_name = addon.get("Name").strip()
            class_specific = addon.get("classspecific").strip()
            mod_found = False

            for i in range(1, 3):
                mod_code = addon.get(f"mod{i}code").strip()

                if not ADDON_TYPES.get(mod_code):
                    continue
                else:
                    mod_found = True
                    break

            if not mod_found:
                continue

            if len(addon_name) == 0 or addon_name.lower() in INVALID_NAMES:
                continue

            if len(class_specific) > 0:
                continue

            for column in columns:
                item_code = addon.get(column).strip()

                if len(item_code) == 0:
                    continue

                addons = item_addons.get(item_code, [])
                addons.append(addon)
                item_addons[item_code] = addons

    return item_addons

def generate_addon_pool(item_type, all_addons):
    addons = []
    item_codes = []

    for column in ITEM_TYPE_COLUMNS:
        code = item_type.get(column)

        if len(code) == 0:
            continue

        item_codes.append(code)

    for code in item_codes:
        for addon in all_addons.get(code, []):
            if addon in addons:
                continue

            exclusion_found = False

            for i in range(1, 5):
                exclusion_type = addon.get(f"etype{i}", "").strip()

                if len(exclusion_type) == 0:
                    continue

                if exclusion_type in item_codes:
                    exclusion_found = True
                    break

            if exclusion_found:
                continue

            addons.append(addon)

    return addons

def generate_item_name(item, prefixes, suffixes):
    item_name = item.get("name")

    if len(prefixes) > 0:
        item_name = " ".join([prefix.get("Name") for prefix in prefixes] + [item_name])

    if len(suffixes) > 0:
        item_name = " ".join([item_name] + [suffix.get("Name") for suffix in suffixes])

    return item_name

def generate_addon_stats(addon):
    stats = []

    for i in range(1, 3):
        mod_code = addon.get(f"mod{i}code").strip()
        if len(mod_code) == 0:
            continue
        
        mod_params = ADDON_TYPES.get(mod_code)
        if not mod_params:
            continue

        mod_name, mod_denominator = mod_params.split("|")
        mod_param = addon.get(f"mod{i}param")
        mod_min_val = addon.get(f"mod{i}min").strip("-")
        mod_max_val = addon.get(f"mod{i}max").strip("-")
        mod_denom_prefix = mod_denominator
        mod_denom_suffix = ""

        if mod_denominator == "0":
            mod_denom_prefix = ""
        elif mod_denominator == "+%":
            mod_denom_prefix = "+"
            mod_denom_suffix = "%"
        elif mod_denominator == "%":
            mod_denom_prefix = ""
            mod_denom_suffix = "%"

        if mod_param and mod_param != "0":
            stats.append(f"{mod_name} {mod_denom_prefix}{mod_param}{mod_denom_suffix}")
        elif mod_min_val == mod_max_val:
            stats.append(f"{mod_name} {mod_denom_prefix}{mod_min_val}{mod_denom_suffix}")
        else:
            stats.append(f"{mod_name} {mod_denom_prefix}{mod_min_val}-{mod_max_val}{mod_denom_suffix}")

    return stats

def generate_weapon_stats(item):
    stats = []

    if item.get("2handed") == "1":
        stats.append(f"Damage: {item.get('2handmindam')}-{item.get('2handmaxdam')}")
    else:
        stats.append(f"Damage: {item.get('mindam')}-{item.get('maxdam')}")
    
    return stats

def generate_armor_stats(item):
    stats = []
    defense_min = item.get('minac')
    defense_max = item.get('maxac')

    if defense_min == defense_max:
        stats.append(f"Defense: {defense_min}")
    else:
        stats.append(f"Defense: {defense_min}-{defense_max}")
    
    return stats

def generate_item_stats(item, prefixes, suffixes):
    stats = []
    main_stats = []
    item_category = None
    item_code = item.get("type")

    if item_code in WEAPON_CODES:
        item_category = ITEM_CATEGORY_OFFENSIVE
        main_stats.extend(generate_weapon_stats(item))
    elif item_code in ARMOR_CODES:
        item_category = ITEM_CATEGORY_DEFENSIVE
        main_stats.extend(generate_armor_stats(item))

    for prefix in prefixes:
        stats.extend(generate_addon_stats(prefix))

    for suffix in suffixes:
        stats.extend(generate_addon_stats(suffix))

    return {
        "category": item_category,
        "main_stats": main_stats,
        "stats": stats,
    }

def generate_item(items, item_types, prefixes, suffixes):
    item = random.choice(items)
    item_code = item.get("type")
    item_type = item_types.get(item_code)
    item_level = int(item.get("level"))
    prefix_pool = generate_addon_pool(item_type, prefixes)
    suffix_pool = generate_addon_pool(item_type, suffixes)
    total_prefixes = 0
    total_suffixes = 0
    prefixes = []
    suffixes = []

    if item_level <= 30:
        total_prefixes = random.choice([0, 1])
        total_suffixes = random.choice([0, 1])
    elif item_level > 30 and item_level <= 50:
        total_prefixes = random.choice([0, 2])
        total_suffixes = random.choice([0, 2])
    elif item_level > 50 and item_level <= 70:
        total_prefixes = random.choice([0, 3])
        total_suffixes = random.choice([0, 3])
    else:
        total_prefixes = random.choice([0, 4])
        total_suffixes = random.choice([0, 4])

    if prefix_pool:
        for i in range(total_prefixes):
            if len(prefix_pool) == 0: break
            prefix = random.choice(prefix_pool)
            prefix_group = prefix.get("group")
            prefixes.append(prefix)
            prefix_pool = list(filter(lambda p: p.get("group") != prefix_group, prefix_pool))

    if suffix_pool:
        for i in range(total_suffixes):
            if len(suffix_pool) == 0: break
            suffix = random.choice(suffix_pool)
            suffix_group = suffix.get("group")
            suffixes.append(suffix)
            suffix_pool = list(filter(lambda p: p.get("group") != suffix_group, suffix_pool))

    rarity = RARITY_COMMON
    total_affixes = len(prefixes) + len(suffixes)

    if total_affixes >= 3:
        rarity = RARITY_LEGENDARY
    elif total_affixes >= 2:
        rarity = RARITY_RARE
    elif total_affixes >= 1:
        rarity = RARITY_MAGIC

    base_item = {
        "name": generate_item_name(item, prefixes, suffixes),
        "type": item_type.get("ItemType"),
        "tier": rarity,
    }

    base_item.update(generate_item_stats(item, prefixes, suffixes))

    return base_item

ITEM_TYPES = load_item_types(ITEM_TYPES_FILE, ITEM_TYPE_COLUMNS)
MAGIC_PREFIXES = load_item_addons(MAGIC_PREFIX_FILE, MAGIC_COLUMNS)
MAGIC_SUFFIXES = load_item_addons(MAGIC_SUFFIX_FILE, MAGIC_COLUMNS)
WEAPONS = load_items(WEAPONS_FILE)
ARMOR = load_items(ARMOR_FILE)

def generate_random_armor():
    return generate_item(ARMOR, ITEM_TYPES, MAGIC_PREFIXES, MAGIC_SUFFIXES)

def generate_random_weapon():
    return generate_item(WEAPONS, ITEM_TYPES, MAGIC_PREFIXES, MAGIC_SUFFIXES)

if __name__ == "__main__":
    print("Loaded item types:", len(ITEM_TYPES.keys()))
    print("Loaded weapons:", len(WEAPONS))
    print("Loaded armor:", len(ARMOR))
    print("=======================")

    ITEMS = []

    for i in range(100):
        ITEMS.append(generate_item(WEAPONS, ITEM_TYPES, MAGIC_PREFIXES, MAGIC_SUFFIXES))

    print("Generated 100 weapons")

    for i in range(100):
        ITEMS.append(generate_item(ARMOR, ITEM_TYPES, MAGIC_PREFIXES, MAGIC_SUFFIXES))

    print("Generated 100 armor")
    print("=======================")

    with open("data/loot.json", "w") as f:
        f.write(json.dumps({"items": ITEMS}, indent=4))
