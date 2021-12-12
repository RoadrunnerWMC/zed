# 8/19/17
# Zed: Zelda EDitor
# (Phantom Hourglass and Spirit Tracks)
# By RoadrunnerWMC
# License: GNU GPL v3


import json
import os, os.path
import struct
import sys

import ndspy.lz10
import ndspy.narc
import ndspy.rom

import common
import zclb_zcib


ST_ROM_IN = '../Testing/Zelda - Spirit Tracks.nds'
ST_ROM_OUT = '../Testing/Zelda - Spirit Tracks - Testing.nds'


PROPERTY_NAMES = ['name', 'title',
                  'unk14',
                  'unk19', 'nameID', 'unk1B',
                  'topScreenMode', 'unk1E', 'unk1F',
                  'sdatGroupID', 'unk22', 'unk23',
                  'mapDrawID', 'unk25', 'unk26', 'unk27',
                  'dungeonID',
                  'vehicleCourse', 'initUnk16',
                  'bmgID',
                  'initUnk1C', 'initUnk1E',
                  'initUnk20', 'initUnk22',
                  'initUnk24', 'initUnk26',
                  ]


def listInit2Json(entries):
    L = []
    for e in entries:
        eDict = {}
        L.append(eDict)
        for name in PROPERTY_NAMES:
            eDict[name] = getattr(e, name)
        eDict['maps'] = []
        for m in e.maps:
            eDict['maps'].append({'id': m.mapID, 'unk01': m.unk01, 'unk02': m.unk02})
    return L


def json2ListInit(entries):
    L = []
    for eDict in entries:
        e = zclb_zcib.CourseListInitCourseEntry()
        L.append(e)
        for name in PROPERTY_NAMES:
            setattr(e, name, eDict[name])
        for mDict in eDict['maps']:
            m = zclb_zcib.CourseListInitMapEntry()
            m.mapID = mDict['id']
            m.unk01 = mDict['unk01']
            m.unk01 = mDict['unk01']
            e.maps.append(m)
    return L



def main():

    argv = sys.argv
    #argv = [None, 'export', 'temp.json']
    if len(argv) < 3:
        print('Not enough arguments :|')
        print(f'Usage: {argv[0]} export filename.json')
        print(f'       {argv[0]} import filename.json')
        return

    exportFile = importFile = False

    if argv[1] == 'export':
        exportFile = True
    elif argv[1] == 'import':
        importFile = True
    else:
        raise ValueError(argv[1])

    ioName = argv[2]

    gameRomFilenames = []
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

        # Load the copy from the rom
        courseEntries = zclb_zcib.loadCourseListAndInit(game, courseList, courseInit)


        # Export if needed
        if exportFile:
            entriesSerialized = listInit2Json(courseEntries)
            with open(ioName, 'w', encoding='utf-8') as f:
                json.dump(entriesSerialized, f, indent=4, ensure_ascii=False)


        # Import if needed
        if importFile:
            with open(ioName, 'r', encoding='utf-8') as f:
                entriesSerialized = json.load(f)
            courseEntries = json2ListInit(entriesSerialized)


        # Resave courselist/courseinit
        courseListNew, courseInitNew = zclb_zcib.saveCourseListAndInit(game, courseEntries)
        if 'Course/courseinit.cib' in rom.filenames:
            rom.files[rom.filenames['Course/courseinit.cib']] = courseInitNew
        if 'Map/courselist.clb' in rom.filenames:
            rom.files[rom.filenames['Map/courselist.clb']] = courseListNew
        elif 'Course/courselist.clb' in rom.filenames:
            rom.files[rom.filenames['Course/courselist.clb']] = courseListNew


        romDataOut = rom.save()
        with open(romOut, 'wb') as f:
            f.write(romDataOut)


if __name__ == '__main__':
    main()
