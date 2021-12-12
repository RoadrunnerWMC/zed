# 8/19/17
# Zed: Zelda EDitor
# (Phantom Hourglass and Spirit Tracks)
# By RoadrunnerWMC
# License: GNU GPL v3


import os, os.path
import struct

import ndspy.lz10
import ndspy.narc
import ndspy.rom

import common
import zab
import zcb
import zclb_zcib
import zmb
import zob


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





def main():

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

        courseEntries = zclb_zcib.loadCourseListAndInit(game, courseList, courseInit)


        # assert courseList == courseListNew
        # assert courseInit == courseInitNew

        # printed = set()
        # for name in rom.filenames['Npc'].files:
        #     # print(name)
        #     # continue
        #     if name == 'Tex.bin':
        #         print('Tex.bin  (??)')
        #         continue
        #     spl = name.split('.')[0]
        #     if spl in printed: continue
        #     printed.add(spl)

        #     allLikeThis = []
        #     for name2 in rom.filenames['Npc'].files:
        #         if name2.split('.')[0] == spl:
        #             allLikeThis.append('.' + name2.split('.')[-1])
        #     allLikeThis.sort()

        #     while len(spl) < 20:
        #         spl += ' '
        #     print(spl + f' ({", ".join(allLikeThis)})')

        # temp = set()
        # for name in rom.filenames['MapObj'].files:
        #     temp.add(name.split('.')[0])
        #     continue
        #     if not name.endswith('.bin'): continue
        #     print(name)
        #     try:
        #         os.makedirs('/home/user/zed/Testing/stEvent/' + name)
        #     except FileExistsError: pass

        #     f = rom.files[rom.filenames['Event/' + name]]
        #     narcNames, narcFiles = ndspy.narc.load(ndspy.lz10.decompress(f))

        #     for f in narcNames.folders:
        #         os.makedirs('/home/user/zed/Testing/stEvent/' + name + '/' + f)
        #         for f2 in narcNames[f].files:
        #             with open('/home/user/zed/Testing/stEvent/' + name + '/' + f + '/' + f2, 'wb') as f3:
        #                 f3.write(narcFiles[narcNames[f + '/' + f2]])
        #         #print(narcNames[f].folders)
        #         #print(narcNames[f].files)
        #     print(narcNames.files)
        #     #raise

        # print(temp)

        # raise

        for entry in courseEntries:
            courseFilename = entry.name
            courseName = entry.title

            courseFolderName = 'Map/' + courseFilename
            if courseFolderName not in rom.filenames: continue
            courseFolder = rom.filenames[courseFolderName]

            # Get stuff from course.bin
            courseBin = rom.files[courseFolder['course.bin']]
            courseNarcNames, courseNarcFiles = \
                ndspy.narc.load(ndspy.lz10.decompress(courseBin))
            resaveCourse = False

            # The zab is always the only file in the "arrange" folder
            zabFile = courseNarcFiles[courseNarcNames['arrange'].firstID]
            zabObj = zab.ZAB(game, zabFile)

            # Grab the zob files
            motypeZob = zob.ZOB(game, courseNarcFiles[courseNarcNames['objlist/motype.zob']])
            motype1Zob = zob.ZOB(game, courseNarcFiles[courseNarcNames['objlist/motype_1.zob']])
            npctypeZob = zob.ZOB(game, courseNarcFiles[courseNarcNames['objlist/npctype.zob']])
            npctype1Zob = zob.ZOB(game, courseNarcFiles[courseNarcNames['objlist/npctype_1.zob']])

            # tex/mapModel.nsbtx only exists in Phantom Hourglass,
            # and, even there, not in every course.bin
            mapModelID = courseNarcNames['tex/mapModel.nsbtx']
            if mapModelID is None:
                mapModel = None
            else:
                mapModel = courseNarcFiles[mapModelID]

            # Load map**.bin's

            for mapNumber in range(100):
                mapBinFn = 'map%02d.bin' % mapNumber
                if mapBinFn not in courseFolder: continue

                mapBin = rom.files[courseFolder[mapBinFn]]
                mapNarcNames, mapNarcFiles = \
                    ndspy.narc.load(ndspy.lz10.decompress(mapBin))

                # SUBFOLDERS OF MAP.BIN
                # mcb: PH: one optional {courseFilename}_{mapNumber}.mcb file
                #      ST: empty folder
                # nsbmd: PH: one optional {courseFilename}_{mapNumber}.nsbmd file
                #        ST: one optional {courseFilename}_{mapNumber}.nsbmd file
                #            OR
                #            one optional {courseFilename}_{mapNumber}.nsbta file
                # zbcd: PH: (no such folder)
                #       ST: optional cam_**.zbcd files
                # zcb: one required {courseFilename}_{mapNumber}.zcb file
                # zmb: one required {courseFilename}_{mapNumber}.zmb file
                # zob: PH: motype_{mapNumber}_0.zob,
                #          motype_{mapNumber}_1.zob,
                #          npctype_{mapNumber}_0.zob,
                #          npctype_{mapNumber}_1.zob,
                #      ST: Same as above, but it goes through _9
                #          (for a total of 20 files)

                # Load the optional MCB (Phantom Hourglass-only)
                mcbFolder = mapNarcNames['mcb']
                if mcbFolder.files:
                    mcbFile = mapNarcFiles[mcbFolder.firstID]
                else:
                    mcbFile = None

                # Load the model
                # (can be nonexistent in either game)
                # (can be a NSBTA instead of a NSBMD in Spirit Tracks)
                model = None
                isTA = False
                nsbmdFolder = mapNarcNames['nsbmd']
                if nsbmdFolder.files:
                    model = mapNarcFiles[nsbmdFolder.firstID]
                    isTA = nsbmdFolder.files[0].endswith('.nsbta')
                
                # Load the camera files (Spirit Tracks-only)
                cameraFiles = {}
                if 'zbcd' in mapNarcNames:
                    zbcdFolder = mapNarcNames['zbcd']
                    for camFileNum, camFilename in enumerate(zbcdFolder.files):
                        cameraFiles[int(camFilename[-7:-5])] = \
                            mapNarcFiles[zbcdFolder.firstID + camFileNum]
                
                # Load the ZCB and ZMB files
                #if courseFilename not in ['f_first', 'f_htown', 'd_main', 'e3_dungeon']: continue
                zcbFile = mapNarcFiles[mapNarcNames['zcb'].firstID]
                zmbFile = mapNarcFiles[mapNarcNames['zmb'].firstID]
                #print(f'{courseFilename}/%02d' % mapNumber)
                map = zmb.ZMB(game, zmbFile)
                if map.CAME:
                    print(f'{len(map.CAME)}: {courseFilename}/%02d' % mapNumber)
                collisions = zcb.ZCB(game, zcbFile)
                # if map.CMPT:
                #     ...

                # Load the ZOBs
                moTypes = []
                for zobNum in range(10):
                    for zobFile in mapNarcNames['zob'].files:
                        if zobFile.startswith('motype_') and zobFile.endswith(f'_{zobNum}.zob'):
                            break
                    else:
                        break
                    moTypes.append(zob.ZOB(game, mapNarcFiles[mapNarcNames.idOf('zob/' + zobFile)]))
                npcTypes = []
                for zobNum in range(10):
                    for zobFile in mapNarcNames['zob'].files:
                        if zobFile.startswith('npctype_') and zobFile.endswith(f'_{zobNum}.zob'):
                            break
                    else:
                        break
                    npcTypes.append(zob.ZOB(game, mapNarcFiles[mapNarcNames.idOf('zob/' + zobFile)]))

                if game == common.Game.PhantomHourglass:
                    assert len(moTypes) == 2
                    assert len(npcTypes) == 2
                else:
                    assert len(moTypes) == 10
                    assert len(npcTypes) == 10


                # # TESTING
                # sortedActorsList = [n.type for n in map.actors]
                # for q, z in enumerate(npcTypes):
                #     indexArray = [sortedActorsList.index(e) for e in z.entries]
                #     print(indexArray)
                #     assert indexArray == sorted(indexArray)
                #     print(z.entries)
                # print(sortedActorsList)
                # print()


                zmbFile2 = map.save(game)
                resaveMap = (zmbFile != zmbFile2)
                assert not resaveMap
                #map.renderPNG().save(f'courses/{courseFilename}_%02d.png' % mapNumber)

                if resaveMap:
                    mapNarcFiles[mapNarcFiles.index(zmbFile)] = zmbFile2

                    newMapBin = ndspy.lz10.compress(ndspy.narc.save(mapNarcNames, mapNarcFiles))
                    rom.files[courseFolder[mapBinFn]] = newMapBin


            if resaveCourse:
                newCourseBin = ndspy.lz10.compress(ndspy.narc.save(courseNarcNames, courseNarcFiles))
                rom.files[courseFolder['course.bin']] = newCourseBin


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
