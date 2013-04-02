#!/usr/bin/python

MC_VERSION = "1.5.1"
FORGE_VERSION = "7.7.1.624"

TEST_SERVER_ROOT = "temp-server"
TEST_SERVER_FILE = "minecraft_server+forge.jar"
TEST_SERVER_CMD = "java -mx2G -jar %s nogui"
ANALYZER_FILENAME = "ModAnalyzer-1.0-SNAPSHOT.jar"

ALL_MODS_DIR = "allmods"
DATA_DIR = "data"

import os, urllib, zipfile, urllib2, tempfile, shutil

def setupServer(serverFilename):
    mcZip = getURLZip("http://assets.minecraft.net/%s/minecraft_server.jar" % (MC_VERSION.replace(".", "_"),))
    forgeZip = getURLZip("http://files.minecraftforge.net/minecraftforge/minecraftforge-universal-%s-%s.zip" % (MC_VERSION, FORGE_VERSION))

    with zipfile.ZipFile(serverFilename, "w") as serverZip:
        for member in set(mcZip.namelist()) - set(forgeZip.namelist()):
            # vanilla classes, not overwritten
            serverZip.writestr(member, mcZip.read(member))
            print "M",member

        for member in set(forgeZip.namelist()) - set(mcZip.namelist()):
            # Forge classes
            serverZip.writestr(member, forgeZip.read(member))
            print "F",member

        for member in set(forgeZip.namelist()) & set(mcZip.namelist()):
            # overwrites - Forge > vanilla
            serverZip.writestr(member, forgeZip.read(member))
            print "O",member
    print "Server setup at",serverFilename

def getURLZip(url):
    f = tempfile.mktemp()
    print "Retrieving %s..." % (url,)
    urllib.urlretrieve(url, f)
    return zipfile.ZipFile(f, 'r')

def runServer():
    print "Starting server..."
    d = os.getcwd()
    os.chdir(TEST_SERVER_ROOT)
    os.system(TEST_SERVER_CMD % (TEST_SERVER_FILE,))
    os.chdir(d)
    print "Server terminated"

def analyzeMod(fn):
    # clean
    modsFolder = os.path.join(TEST_SERVER_ROOT, "mods")
    if os.path.exists(modsFolder):
        shutil.rmtree(modsFolder)
    os.mkdir(modsFolder)
    configFolder = os.path.join(TEST_SERVER_ROOT, "config")
    if os.path.exists(configFolder):
        shutil.rmtree(configFolder)

    # install analyzer
    shutil.copyfile(os.path.join("target", ANALYZER_FILENAME), os.path.join(modsFolder, ANALYZER_FILENAME))

    # install mod
    shutil.copyfile(fn, os.path.join(modsFolder, os.path.basename(fn)))

    # running the server will load the analyzer, then quit
    runServer()

    # save
    if not os.path.exists(DATA_DIR):
        os.mkdir(DATA_DIR)
    shutil.copy(os.path.join(TEST_SERVER_ROOT, "mod-analysis.csv"), os.path.join(DATA_DIR, "info-" + os.path.basename(fn) + ".csv"))

def getMods():
    if not os.path.exists(ALL_MODS_DIR):
        os.mkdir(ALL_MODS_DIR)
    mods = []
    for m in sorted(os.listdir(ALL_MODS_DIR)):
        if m.startswith("."): continue
        mods.append(os.path.join(ALL_MODS_DIR, m))
    return mods

def main():
    # setup analyzer
    os.system("mvn initialize -P -built")
    os.system("mvn package")

    # setup server
    server = os.path.join(TEST_SERVER_ROOT, TEST_SERVER_FILE)
    if not os.path.exists(server):
        if not os.path.exists(TEST_SERVER_ROOT):
            os.mkdir(TEST_SERVER_ROOT)
        setupServer(server)
    print "Using server at:",server

    for mod in getMods():
        analyzeMod(mod)


if __name__ == "__main__":
    main()
