WEAPON_CODES = ("weap", "mele", "abow", "ajav", "aspe", "axe", "bow", "club", "h2h", "h2h2", "hamm", "jave", "knif", "mace", "orb", "pole", "scep", "spea", "staf", "swor", "taxe", "tkni", "tpot", "wand", "xbow")
ARMOR_CODES = ("shie", "shld", "armo", "boot", "glov", "belt", "helm")

ADDON_TYPES = dict((
    ("abs-cold", "Absorb Cold|+"),
    ("abs-fire", "Absorb Fire|+"),
    ("abs-ltng", "Absorb Lightning|+"),
    ("abs-cold%", "Absorb Cold %|+%"),
    ("abs-fire%", "Absorb Fire %|+%"),
    ("abs-ltng%", "Absorb Lightning %|+%"),
    ("abs-cold/lvl", "Absorb Cold/Level|+"),
    ("abs-fire/lvl", "Absorb Fire/Level|+"),
    ("abs-mag", "Magic Absorb|+"),
    ("ac%", "Defense|%"),
    ("ac-miss", "Defense Vs Missiles|+"),
    ("ac/lvl", "Defense/Level|+"),
    ("allskills", "All Skills|+"),
    ("att%", "Attack Rating %|+%"),
    ("att", "Attack Rating|+"),
    ("att/lvl", "Attack Rating/Level|+"),
    ("balance2", "Faster Hit Recovery|%"),
    ("block", "Increased Chance of Blocking|%"),
    ("block2", "Faster Block Rate|%"),
    ("cast1", "Faster Cast Rate|%"),
    ("crush", "Crushing Blow|%"),
    ("deadly", "Deadly Strike|+%"),
    ("deadly/lvl", "Deadly Strike/Level|+%"),
    ("dmg-ac", "To Monster Defense Per Hit|-"),
    ("dmg-demon", "Damage To Demons|+%"),
    ("dmg-min", "Damage Min|+"),
    ("dmg-norm", "Adds Damage|+"),
    ("dmg-to-mana", "Damage To Mana|%"),
    ("dmg-undead", "Damage To Undead|+%"),
    ("dmg/lvl", "Maximum Damage/Level|+"),
    ("dmg%", "Enhanced Maximum Damage|+%"),
    ("dmg%/lvl", "Enhanced Maximum Damage/Level|+%"),
    ("ease", "Requirements|%"),
    ("fireskill", "Fire Skill|+"),
    ("freeze", "Hit Freezes Target|+"),
    ("gold%", "Extra Gold|%"),
    ("gold%/lvl", "Extra Gold/Level|%"),
    ("hp", "Life|+"),
    ("hp%", "Max Life|%"),
    ("hp/lvl", "Life/Level|+"),
    ("ignore-ac", "Ignore Target Defense|0"),
    ("indestruct", "Indestructible|0"),
    ("knock", "Knockback|0"),
    ("lifesteal", "Life Steal|%"),
    ("mag%", "Magic Find|+%"),
    ("mag%/lvl", "Magic Find/Level|+%"),
    ("mana", "Mana|+"),
    ("mana%", "Maximum Mana|%"),
    ("mana/lvl", "Mana/Level|+"),
    ("manasteal", "Mana Steal|%"),
    ("move2", "Faster Run/Walk|+%"),
    ("nofreeze", "Cannot Be Frozen|0"),
    ("noheal", "Prevent Monster Heal|0"),
    ("openwounds", "Open Wounds|%"),
    ("reduce-ac", "Target Defense|-%"),
    ("red-dmg", "Damage Reduced By|1"),
    ("red-dmg%", "Damage Reduction|%"),
    ("red-mag", "Magic Damage Reduced By|1"),
    ("regen-mana", "Regenerate Mana|+%"),
    ("rep-quant", "Replenish Quantity|1"),
    ("res-all", "All Resistances|+%"),
    ("res-all-max", "Maximum All Resistances|+%"),
    ("res-fire-max", "Maximum Fire Resist|+%"),
    ("res-cold-max", "Maximum Cold Resist|+%"),
    ("res-ltng-max", "Maximum Lightning Resist|+%"),
    ("res-pois-max", "Maximum Poison Resist|+%"),
    ("res-ltng/lvl", "Resist Lightning/Level|+%"),
    ("res-fire", "Resist Fire|+%"),
    ("res-cold", "Resist Cold|+%"),
    ("res-ltng", "Resist Lightning|+%"),
    ("res-mag", "Magic Resist|+%"),
    ("res-pois", "Resist Poison|+%"),
    ("slow", "Slows Target|%"),
    # ("sock", "Socketed|1"),
    ("swing2", "Increased Attack Speed|+%"),
    ("str", "Strength|+"),
    ("str/lvl", "Str/Level|+"),
    ("dex", "Dexterity|+"),
    ("dex/lvl", "Dex/Level|+"),
    ("vit", "Vitality|+"),
    ("vit/lvl", "Vit/Level|+"),
    ("enr", "Energy|+"),
    ("stupidity", "Hit Blinds Target|+"),

    #   Class Skills
    ("ama", "Skills Amazon|+"),
    ("ass", "Skills Assassin|+"),
    ("bar", "Skills Barbarian|+"),
    ("dru", "Skills Druid|+"),
    ("nec", "Skills Necromancer|+"),
    ("pal", "Skills Paladin|+"),
    ("sor", "Skills Sorceress|+"),

    #  1.10 'Passive' Elemental Mastery
    ("extra-fire", "Skill Damage: Fire|+%"),
    ("extra-ltng", "Skill Damage: Lightning|+%"),
    ("extra-cold", "Skill Damage: Cold|+%"),
    ("extra-pois", "Skill Damage: Poison|+%"),

    #  1.10 -XX% To Enemy Elemental Resistance
    ("pierce-fire", "Pierce Resistance: Fire|-%"),
    ("pierce-ltng", "Pierce Resistance: Lightning|-%"),
    ("pierce-cold", "Pierce Resistance: Cold|-%"),
    ("pierce-pois", "Pierce Resistance: Poison|-%"),
))