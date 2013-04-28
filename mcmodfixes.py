#!/usr/bin/python

# Fixes and mod-specific data for various mods' mcmod.info files

import fnmatch

DEP_BLACKLIST = set((
    "mod_MinecraftForge",   # we always have Forge
    "Forge", # typo(?) for mod_MinecraftForge
    "FML", # we always have FML
    "MinecraftForge", # another typo for mod_MinecraftForge
    "MinecraftForge, CodeChickenCore", # typo for CodeChickenCore, broken string instead of a real list
    "MinecraftForge,CoFHCore", # typo for ["MinecraftForge","CoFHCore"]
    "Industrialcraft", # typo for IC2
    "GUI_Api", # typo for GuiAPI and not needed on server
    "EurysCore", # replaced by SlimevoidLib?
    "Modular Powersuits", # mmmPowersuits
    "mod_NotEnoughItems", # chargepads
    ))


DEP_ADDITIONS = {
    "gregtech": ["IC2"],
    "dimensional-anchor": ["IC2"],
    "MineFactoryReloaded": ["PowerCrystalsCore"],
    "NetherOres": ["PowerCrystalsCore"],
    "PowerConverters": ["PowerCrystalsCore"],
    "FlatBedrock": ["PowerCrystalsCore"],
    "immibis-microblocks": ["ImmibisCore"],
    "SlopesAndCorners": ["SlimevoidLib"],
    "ChickenChunks": ["CodeChickenCore"],
    "EnderStorage": ["CodeChickenCore"],
    "TrailMix": ["iChunUtil"],
    "Torched": ["iChunUtil"],
    "MPSA": ["mmmPowersuits"],
    "ThermalExpansion": ["CoFHCore"],
    "OmniTools": ["CoFHCore"],
    "ElectricExpansion": ["BasicComponents"],
    "OpenCCSensors": ["ComputerCraft"],
    "Translocator": ["CodeChickenCore"],
    "miscperipherals": ["ComputerCraft"],
    "chargepads": ["NotEnoughItems"],
    "MekanismGenerators": ["Mekanism"],
    "MekanismTools": ["Mekanism"],
    "thaumicbees": ["Forestry"],
    }

MOD_IDS = {
    "PowerCrystalsCore*": ["PowerCrystalsCore"],
    "*bspkrsCore*": ["mod_bspkrsCore"], # newline in json, can't parse
    "BasicComponents*": ["BasicComponents"], # no mcmod.info
    }

FILENAME_HAS_NO_VERSION = [
    "gregtechmod.zip", # "If you are unsure about your Version, look at the "mcmod.info" inside the zip, just open it with Notepad."
    "WeaponMod.zip",
    "Barrels 1.5+.jar",
    ]

REQUIRES_EXTRACTION = {
    # mod name : extracted from this folder
    "Millenaire": "Put in mods folder", 
    "BattleTowers": "mods",
    "KenshiroMod": "mods",
    "MagicYarn": "mods",
    "Ruins": "mods",
    #"RopePlus": "mods", # not
    "BetterDungeons": "mods", # but also requires extra files .minecraft..
    }

USES_UNSHIFTED_ITEM_IDS = [
    "immibis-*",
    ]

def getExtraDeps(mod):
    for k, v in DEP_ADDITIONS.iteritems():
        if mod.startswith(k):
            return set(v)
    return set()

def fixDeps(mod, deps):
    deps = set(deps)
    deps -= DEP_BLACKLIST
    deps |= getExtraDeps(mod)

    deps = [dep.split("@")[0] for dep in deps]  # remove version constraints

    return deps


def fixModIDs(mod, ids):
    for k, v in MOD_IDS.iteritems():
        if fnmatch.fnmatch(mod, k):
            return v 

    return ids

def modNeedsRename(fn):
    for k in FILENAME_HAS_NO_VERSION:
        if fn.startswith(k):
            return True
    return False

"""Get the folder name in a mod zip which tells you to install it into the mod folders."""
def getInstructionFolder(fn):
    for k, v in REQUIRES_EXTRACTION.iteritems():
        if fn.startswith(k):
            return v
    return None


def usesUnshiftedItemIDs(fn):
    for k in USES_UNSHIFTED_ITEM_IDS:
        if fn.startswith(k):
            return True
    return False

