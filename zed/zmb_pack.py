# 8/19/17
# Zed: Zelda EDitor
# (Phantom Hourglass and Spirit Tracks)
# By RoadrunnerWMC
# License: GNU GPL v3


import collections
import json
import os, os.path
import struct
import sys

import ndspy.lz10
import ndspy.narc
import ndspy.rom

import common
import zmb


PH_ROM_IN = '../Testing/Zelda - Phantom Hourglass.nds'
PH_ROM_OUT = '../Testing/Zelda - Phantom Hourglass - Testing.nds'
ST_ROM_IN = '../Testing/Zelda - Spirit Tracks.nds'
ST_ROM_OUT = '../Testing/Zelda - Spirit Tracks - Testing.nds'



courseNames = {}
if os.path.isfile('courses.txt'):
    with open('courses.txt', 'r', encoding='utf-8') as f:
        d = f.read()
    for L in d.splitlines():
        if not L: continue
        courseNames[L.split(':')[0].strip()] = L.split(':')[1].strip()


def parseCourselist(courseInit, courseList):
    initExists = courseInit is not None

    if initExists:
        assert courseInit.startswith(b'ZCIB')
    assert courseList.startswith(b'ZCLB')

    finalList = []

    if initExists:
        zcibMagic, initUnk04, entriesCountInit1, entriesCountInit2 = struct.unpack_from('<4s3I', courseInit)
    zclbMagic, listUnk04, entriesCount1, entriesCount2 = struct.unpack_from('<4s3I', courseList)

    initOffset = listOffset = 0x10
    for i in range(entriesCount1):
        if initExists:
            initEntryLength = struct.unpack_from('<I', courseInit, initOffset)[0]
            entryName = courseInit[initOffset + 4 : initOffset + 0x14].rstrip(b'\0').decode('shift-jis')
        else:
            initEntryLength = 0
            entryName = ''

        listEntryLength = struct.unpack_from('<I', courseList, listOffset)[0]
        entryFile = courseList[listOffset + 4 : listOffset + 0x14].rstrip(b'\0').decode('shift-jis')

        finalList.append((entryName, entryFile))

        initOffset += initEntryLength
        listOffset += listEntryLength

    return finalList



def main():

    argv = sys.argv

    exportFile = importFile = False

    # if argv[1] == 'export':
    #     exportFile = True
    # elif argv[1] == 'import':
    #     importFile = True
    # else:
    #     raise ValueError(argv[1])

    # ioName = argv[2]

    exportFile = True
    ioName = 'f_first/0'

    gameRomFilenames = []
    #gameRomFilenames.append((common.Game.PhantomHourglass, PH_ROM_IN, PH_ROM_OUT))
    gameRomFilenames.append((common.Game.SpiritTracks,     ST_ROM_IN, ST_ROM_OUT))
    for game, romIn, romOut in gameRomFilenames:
        with open(romIn, 'rb') as f:
            romData = f.read()
        rom = ndspy.rom.NintendoDSRom(romData)

        if 'Course/courseinit.cib' in rom.filenames:
            courseInit = rom.files[rom.filenames['Course/courseinit.cib']]
        else:
            courseInit = None

        if 'Map/courselist.clb' in rom.filenames:
            courseList = rom.files[rom.filenames['Map/courselist.clb']]
        elif 'Course/courselist.clb' in rom.filenames:
            courseList = rom.files[rom.filenames['Course/courselist.clb']]
        else:
            raise RuntimeError('Are you sure this is a Zelda rom?')

        courses = parseCourselist(courseInit, courseList)

        for courseName, courseFilename in courses:
            #print(courseFilename)
            if ioName.split('/')[0] != courseFilename: continue

            courseFolderName = 'Map/' + courseFilename
            if courseFolderName not in rom.filenames: continue
            courseFolder = rom.filenames[courseFolderName]

            # Get stuff from course.bin
            courseBin = rom.files[courseFolder['course.bin']]
            courseNarcNames, courseNarcFiles = \
                ndspy.narc.load(ndspy.lz10.decompress(courseBin))
            resaveCourse = False

            # Load map**.bin's

            for mapNumber in range(100):
                if int(ioName.split('/')[1]) != mapNumber: continue
                mapBinFn = 'map%02d.bin' % mapNumber
                if mapBinFn not in courseFolder: continue

                mapBin = rom.files[courseFolder[mapBinFn]]
                mapNarcNames, mapNarcFiles = \
                    ndspy.narc.load(ndspy.lz10.decompress(mapBin))

                # Load the ZCB and ZMB files
                zmbFile = mapNarcFiles[mapNarcNames['zmb'].firstID]
                map = zmb.ZMB(game, zmbFile)


                if exportFile:
                    files = {}

                    niceName = courseNames.get(courseFilename, courseFilename)
                    print(f'Exporting map {mapNumber} from {niceName}...')

                    def saveSection(L):
                        return b''.join(x.save(game) for x in L)
                    def savePaths(L):
                        outData = bytearray()
                        def pad():
                            while len(outData) % 0x24: outData.extend(b'\0')
                        for p in L:
                            outData.extend(p.save(game))
                            pad()
                            for n in p.nodes:
                                outData.extend(n.save(game))
                                pad()
                            outData.extend(b'w' * 0x24)
                        outData = outData[:-0x24]
                        return outData

                    meta = collections.OrderedDict()
                    files['LDLB'] = saveSection(map.LDLB)
                    files['ROMB'] = map.rombData
                    meta['ROMB'] = collections.OrderedDict()
                    meta['ROMB']['count'] = map.rombCount
                    meta['ROMB']['unk_0A'] = map.rombUnk0A
                    meta['ROOM'] = collections.OrderedDict()
                    meta['ROOM']['unk_0C'] = map.roomUnk0C
                    meta['ROOM']['skybox_type'] = map.skyboxType
                    meta['ROOM']['draw_distance'] = map.drawDistance
                    meta['ROOM']['unk_10'] = map.roomUnk10
                    meta['ROOM']['music_id'] = map.musicID
                    meta['ROOM']['lighting_type'] = map.lightingType
                    meta['ROOM']['unk_14'] = map.roomUnk14
                    meta['ROOM']['unk_15'] = map.roomUnk15
                    meta['ROOM']['unk_16'] = map.roomUnk16
                    meta['ROOM']['unk_18'] = map.roomUnk18
                    meta['ROOM']['unk_19'] = map.roomUnk19
                    meta['ROOM']['unk_1A'] = map.roomUnk1A
                    meta['ROOM']['unk_1B'] = map.roomUnk1B
                    meta['ROOM']['unk_1C'] = map.roomUnk1C
                    meta['ROOM']['unk_1D'] = map.roomUnk1D
                    meta['ROOM']['unk_1E'] = map.roomUnk1E
                    files['ARAB'] = saveSection(map.locations)
                    files['RALB'] = savePaths(map.paths)
                    files['WARP'] = saveSection(map.exits)
                    files['CAME'] = saveSection(map.CAME)
                    files['CMPT'] = saveSection(map.CMPT)
                    files['PLYR'] = saveSection(map.entrances)
                    files['MPOB'] = saveSection(map.mapObjects)
                    files['NPCA'] = saveSection(map.actors)

                    for fn, data in files.items():
                        with open(f'zmb_export/{fn}.bin', 'wb') as f:
                            f.write(data)
                    with open(f'zmb_export/meta.json', 'w', encoding='utf-8') as f:
                        json.dump(meta, f, indent=4)

                if importFile:
                    print(f'Importing map {mapNumber} to {courseNames[courseFilename]}...')

                    files = {}
                    for section in ['LDLB', 'ROMB', 'ARAB', 'RALB', 'WARP', 'CAME', 'CMPT', 'PLYR', 'MPOB', 'NPCA']:
                        with open(f'zmb_export/{section}.bin', 'rb') as f:
                            files[section] = f.read()
                    with open(f'zmb_export/meta.json', 'r', encoding='utf-8') as f:
                        meta = json.load(f)

                    def makeSection(t, d, width):
                        L = []
                        for i in range(len(d) // width):
                            d2 = d[i * width : i * width + width]
                            L.append(t(game, d2))
                        return L
                    def makePaths(d):
                        L = []
                        i = 0
                        while i < len(d):
                            if game == common.Game.PhantomHourglass:
                                header = d[i:i+12]
                            else:
                                header = d[i:i+8]
                            path = zmb.Path(game, header)
                            i += 0x24
                            for j in range(header[1]):
                                if game == common.Game.PhantomHourglass:
                                    nodeLen = 0x0C
                                else:
                                    nodeLen = d[i + 0x12]
                                nodeData = d[i:i+nodeLen]
                                node = zmb.PathNode(game, nodeData)
                                path.nodes.append(node)
                                i += 0x24
                            i += 0x24 # the separator line
                            L.append(path)
                        return L

                    map.LDLB = makeSection(zmb.LDLB, files['LDLB'], 8)
                    map.rombData = files['ROMB']
                    map.rombCount = meta['ROMB']['count']
                    map.rombUnk0A = meta['ROMB']['unk_0A']
                    map.roomUnk0C = meta['ROOM']['unk_0C']
                    map.skyboxType = meta['ROOM']['skybox_type']
                    map.drawDistance = meta['ROOM']['draw_distance']
                    map.roomUnk10 = meta['ROOM']['unk_10']
                    map.musicID = meta['ROOM']['music_id']
                    map.lightingType = meta['ROOM']['lighting_type']
                    map.roomUnk14 = meta['ROOM']['unk_14']
                    map.roomUnk15 = meta['ROOM']['unk_15']
                    map.roomUnk16 = meta['ROOM']['unk_16']
                    map.roomUnk18 = meta['ROOM']['unk_18']
                    map.roomUnk19 = meta['ROOM']['unk_19']
                    map.roomUnk1A = meta['ROOM']['unk_1A']
                    map.roomUnk1B = meta['ROOM']['unk_1B']
                    map.roomUnk1C = meta['ROOM']['unk_1C']
                    map.roomUnk1D = meta['ROOM']['unk_1D']
                    map.roomUnk1E = meta['ROOM']['unk_1E']
                    map.ARAB = makeSection(zmb.ARAB, files['ARAB'],
                        0x0C if game == common.Game.PhantomHourglass else 0x10)
                    map.paths = makePaths(files['RALB'])
                    map.exits = makeSection(zmb.Exit, files['WARP'], 0x18)
                    map.CAME = makeSection(zmb.CAME, files['CAME'], 0x1C)
                    map.CMPT = makeSection(zmb.CMPT, files['CMPT'], 0x10)
                    map.entrances = makeSection(zmb.Entrance, files['PLYR'],
                        0x10 if game == common.Game.PhantomHourglass else 0x14)
                    map.mapObjects = makeSection(zmb.MapObject, files['MPOB'], 0x1C)
                    map.actors = makeSection(zmb.Actor, files['NPCA'], 0x20)

                    mapNarcFiles[mapNarcFiles.index(zmbFile)] = map.save(game)

                    newMapBin = ndspy.lz10.compress(ndspy.narc.save(mapNarcNames, mapNarcFiles))
                    rom.files[courseFolder[mapBinFn]] = newMapBin


            if importFile:
                newCourseBin = ndspy.lz10.compress(ndspy.narc.save(courseNarcNames, courseNarcFiles))
                rom.files[courseFolder['course.bin']] = newCourseBin


        romDataOut = rom.save()
        with open(romOut, 'wb') as f:
            f.write(romDataOut)


if __name__ == '__main__':
    main()
