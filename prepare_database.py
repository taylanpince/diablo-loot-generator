import csv
import random

from pprint import pprint

from constants import ADDON_TYPES, WEAPON_CODES, ARMOR_CODES

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

            if len(addon_name) == 0 or addon_name.lower() in INVALID_NAMES:
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

    for column in ITEM_TYPE_COLUMNS:
        code = item_type.get(column)

        if len(code) == 0:
            continue

        for addon in all_addons.get(code, []):
            # TODO: Check for exclusion types (etype1, etype2, ...)
            addons.append(addon)

    return addons

def generate_item_name(item, prefix, suffix):
    item_name = item.get("name")

    if prefix:
        item_name = " ".join([prefix.get("Name"), item_name])

    if suffix:
        item_name = " ".join([item_name, suffix.get("Name")])

    return item_name

def print_addon_stats(addon):
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
            print(f"{mod_name} {mod_denom_prefix}{mod_param}{mod_denom_suffix}")
        elif mod_min_val == mod_max_val:
            print(f"{mod_name} {mod_denom_prefix}{mod_min_val}{mod_denom_suffix}")
        else:
            print(f"{mod_name} {mod_denom_prefix}{mod_min_val}-{mod_max_val}{mod_denom_suffix}")

def print_weapon_stats(item, prefix, suffix):
    if item.get("2handed") == "1":
        print(f"Damage: {item.get('2handmindam')}-{item.get('2handmaxdam')}")
    else:
        print(f"Damage: {item.get('mindam')}-{item.get('maxdam')}")

def print_armor_stats(item, prefix, suffix):
    defense_min = item.get('minac')
    defense_max = item.get('maxac')

    if defense_min == defense_max:
        print(f"Defense: {defense_min}")
    else:
        print(f"Defense: {defense_min}-{defense_max}")

def print_item_stats(item, prefix, suffix):
    item_code = item.get("type")

    if item_code in WEAPON_CODES:
        print_weapon_stats(item, prefix, suffix)
    elif item_code in ARMOR_CODES:
        print_armor_stats(item, prefix, suffix)

    if prefix:
        print_addon_stats(prefix)

    if suffix:
        print_addon_stats(suffix)

def generate_item(items, item_types, prefixes, suffixes):
    item = random.choice(items)
    item_code = item.get("type")
    item_type = item_types.get(item_code)
    prefix_pool = generate_addon_pool(item_type, prefixes)
    suffix_pool = generate_addon_pool(item_type, suffixes)
    prefix = None
    suffix = None

    if prefix_pool:
        prefix = random.choice(prefix_pool)

    if suffix_pool:
        suffix = random.choice(suffix_pool)

    item_name = generate_item_name(item, prefix, suffix)

    print(item_name)
    print(item_type.get("ItemType"))

    print_item_stats(item, prefix, suffix)

ITEM_TYPES = load_item_types(ITEM_TYPES_FILE, ITEM_TYPE_COLUMNS)
MAGIC_PREFIXES = load_item_addons(MAGIC_PREFIX_FILE, MAGIC_COLUMNS)
MAGIC_SUFFIXES = load_item_addons(MAGIC_SUFFIX_FILE, MAGIC_COLUMNS)
WEAPONS = load_items(WEAPONS_FILE)
ARMOR = load_items(ARMOR_FILE)

print("Loaded item types:", len(ITEM_TYPES.keys()))
print("Loaded weapons:", len(WEAPONS))
print("Loaded armor:", len(ARMOR))
print("=======================")

for i in range(100):
    generate_item(ARMOR, ITEM_TYPES, MAGIC_PREFIXES, MAGIC_SUFFIXES)
    print("=======================")
