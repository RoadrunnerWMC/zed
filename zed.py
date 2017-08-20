# 8/19/17
# Zed: Zelda EDitor
# (Phantom Hourglass and Spirit Tracks)
# By RoadrunnerWMC
# License: GNU GPL v3

import os, os.path
import struct

import lz10
import narc


ROOT_ST = '../RETAIL/st/root'
ROOT_PH = '../RETAIL/ph/root'


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


def getOnlyItemFrom(dict):
    key = next(iter(dict))
    return key, dict[key]


def parseZmb(zmb):
    """
    Parse a ZMB (Zelda Map Binary) file.
    """
    stuff = [] # FIXME: TESTING ONLY

    magic, fileLen, version, unk10, unk14, unk18, unk1C = \
        struct.unpack_from('<8s6I', zmb)
    assert magic == b'MAPB'[::-1] + b'ZMB1'[::-1]
    assert fileLen == len(zmb)
    assert unk10 == unk14 == unk18 == unk1C == 0x01020304

    # "version" is 9 in Phantom Hourglass and 11 in Spirit Tracks.
    # It's probably actually "sectionCount", but this way, we can also
    # use it to account for other differences between the games.

    offset = 0x20

    def sectionHeader(expectedMagic):
        """
        Helper function to read a standard section header and verify
        that the magic is as expected.
        """
        magic, len, count, unk0A = struct.unpack_from('<4sIHh', zmb, offset)
        assert magic == expectedMagic[::-1] # (reverse it because little-endian)
        return len, count, unk0A


    # LDLB section (version 11-only)
    if version >= 11:
        ldlbLen, ldlbCount, ldlbUnk0A = sectionHeader(b'LDLB')
        assert ldlbUnk0A == -1
        assert ldlbLen == 12 + 0x08 * ldlbCount

        offset += ldlbLen

    # ROMB section
    rombLen, rombCount, rombUnk0A = sectionHeader(b'ROMB')
    assert rombUnk0A in (0x00, 0x30)
    assert rombLen == 12 + rombCount * 0xC0 # But it's more complicated than a simple table.

    offset += rombLen

    # ROOM section
    roomLen, roomCount, roomUnk0A = sectionHeader(b'ROOM')
    assert roomLen == 0x20
    assert roomCount == 1
    assert roomUnk0A == 0x0304

    offset += roomLen

    # ARAB section
    arabLen, arabCount, arabUnk0A = sectionHeader(b'ARAB')
    assert arabUnk0A == -1
    assert arabLen == 12 + arabCount * (0x0C if version == 9 else 0x10)

    for i in range(arabCount):
        # Struct length is different depending on version.
        if version == 9:
            unk00, unk04, unk08 = \
                struct.unpack_from('<3I', zmb, offset + 12 + 0x0C * i)
        else:
            unk00, unk04, unk08, unk0C = \
                struct.unpack_from('<4I', zmb, offset + 12 + 0x10 * i)

    offset += arabLen

    # RALB section
    ralbLen, ralbCount, ralbUnk0A = sectionHeader(b'RALB')
    assert ralbUnk0A == -1

    # Sadly, ralbCount seems to be a lie. Or something.

    offset += ralbLen

    # WARP section
    warpLen, warpCount, warpUnk0A = sectionHeader(b'WARP')
    assert warpUnk0A == -1
    assert warpLen == 12 + 0x18 * warpCount

    for i in range(warpCount):
        unk00, destination, unk14 = \
            struct.unpack_from('<I16sI', zmb, offset + 12 + 0x18 * i)
        destination = destination.rstrip(b'\0').decode('ascii')
        # unk14 seems to be multiple values.

    offset += warpLen

    # CAME section
    cameLen, cameCount, cameUnk0A = sectionHeader(b'CAME')
    assert cameUnk0A == -1
    assert cameLen == 12 + 0x1C * cameCount

    for i in range(cameCount):
        unk00, unk04, unk08, unk0C, unk10, unk14, unk18 = \
            struct.unpack_from('<7I', zmb, offset + 12 + 0x1C * i)

    offset += cameLen

    # CMPT section (version 11-only)
    if version >= 11:
        cmptLen, cmptCount, cmptUnk0A = sectionHeader(b'CMPT')
        assert cmptUnk0A == -1
        assert cmptLen == 12 + 0x10 * cmptCount

        for i in range(cmptCount):
            unk00, unk04, unk08, unk0C = \
                struct.unpack_from('<4I', zmb, offset + 12 + 0x10 * i)

        offset += cmptLen

    # PLYR section
    plyrLen, plyrCount, plyrUnk0A = sectionHeader(b'PLYR')
    assert plyrUnk0A == 0x0304
    assert plyrLen == 12 + plyrCount * (0x10 if version == 9 else 0x14)

    offset += plyrLen

    # MPOB section ("map objects")
    mpobLen, mpobCount, mpobUnk0A = sectionHeader(b'MPOB')
    assert mpobUnk0A == -1
    assert mpobLen == 12 + 0x1C * mpobCount

    for i in range(mpobCount):
        objType, x, y, unk06, unk08, unk0C, unk10, unk14, unk18 = \
            struct.unpack_from('<4sBBH5I', zmb, offset + 12 + 0x1C * i)
        if version == 9:
            objType, = struct.unpack_from('<I', objType)
            objType = f'({objType})'
        else:
            objType = objType[::-1].decode('ascii')

        stuff.append((False, objType, x << 4, y << 4))

    offset += mpobLen

    # NPCA section (actors)
    npcaLen, npcaCount, npcaUnk0A = sectionHeader(b'NPCA')
    assert npcaUnk0A == -1
    assert npcaLen == 12 + 0x20 * npcaCount

    for i in range(npcaCount):
        actorID, x, y, zPos, rot, unk0C, unk10, unk14, unk18, unk1C = \
            struct.unpack_from('<4s4h5I', zmb, offset + 12 + 0x20 * i)
        actorID = actorID[::-1].decode('ascii')

        # unk18 is related to dialogue/script
        # unk1C can make actors disappear

        stuff.append((True, actorID, x, y))


    IMGW, IMGH = 1024, 1024
    IMGW += 80; IMGH += 80
    import PIL.Image, PIL.ImageDraw, PIL.ImageFont
    image = PIL.Image.new('RGBA', (IMGW, IMGH), (0,0,0,0))
    draw = PIL.ImageDraw.Draw(image)
    font = PIL.ImageFont.truetype('/usr/share/fonts/truetype/noto/NotoMono-Regular.ttf', 10)

    wantPrint = False

    if stuff:
        minX = minY = 0xFFFF
        maxX = maxY = 0
        for isActor, name, xPos, yPos in stuff:
            if xPos < minX: minX = xPos
            if yPos < minY: minY = yPos
            if xPos > maxX: maxX = xPos
            if yPos > maxY: maxY = yPos
        maxX += 1; maxY += 1

        canvasX = minX
        canvasY = minY
        canvasW = canvasH = max(maxX - canvasX, maxY - canvasY)

        def canvasPos(x, y):
            return (1024 * (x - canvasX) / canvasW,
                    1024 * (y - canvasY) / canvasH)

        draw.text(canvasPos(minX, minY), f'({minX}, {minY})', (0,255,0,255), font=font)
        draw.text(canvasPos(maxX, minY), f'({maxX}, {minY})', (0,255,0,255), font=font)
        draw.text(canvasPos(minX, maxY), f'({minX}, {maxY})', (0,255,0,255), font=font)
        draw.text(canvasPos(maxX, maxY), f'({maxX}, {maxY})', (0,255,0,255), font=font)

        for isActor, name, xPos, yPos in stuff:
            assert (xPos >> 4) <= 256
            assert (yPos >> 4) <= 256
            color = (0,0,0,255) if isActor else (255,0,0,255)

            x, y = canvasPos(xPos, yPos)

            draw.text((x, y), name, color, font=font)
            # if (xPos >> 4) >= 245 or (yPos >> 4) >= 245:
            #     wantPrint = True


    return image, wantPrint


def main():
    gameFolders = []
    gameFolders.append(ROOT_PH)
    gameFolders.append(ROOT_ST)
    for gameRoot in gameFolders:

        courseInitPath = os.path.join(gameRoot, 'Course/courseinit.cib')
        if os.path.isfile(courseInitPath):
            with open(courseInitPath, 'rb') as f:
                courseInit = f.read()
        else:
            courseInit = None

        courseListPath1 = os.path.join(gameRoot, 'Map/courselist.clb')
        courseListPath2 = os.path.join(gameRoot, 'Course/courselist.clb')
        if os.path.isfile(courseListPath1):
            with open(courseListPath1, 'rb') as f:
                courseList = f.read()
        else:
            with open(courseListPath2, 'rb') as f:
                courseList = f.read()

        courses = parseCourselist(courseInit, courseList)

        for courseName, courseFilename in courses:
            courseFolder = os.path.join(gameRoot, 'Map', courseFilename)
            if not os.path.isdir(courseFolder): continue

            # Get stuff from course.bin
            with open(os.path.join(courseFolder, 'course.bin'), 'rb') as f:
                courseBin = f.read()
            courseNarc = narc.load(lz10.decompress(courseBin))

            # The zab is always the only file in the "arrange" folder
            _, zab = getOnlyItemFrom(courseNarc['folders']['arrange']['files'])

            # Grab the zob files
            motypeZob = courseNarc['folders']['objlist']['files']['motype.zob']
            motype1Zob = courseNarc['folders']['objlist']['files']['motype_1.zob']
            npctypeZob = courseNarc['folders']['objlist']['files']['npctype.zob']
            npctype1Zob = courseNarc['folders']['objlist']['files']['npctype_1.zob']

            # tex/mapModel.nsbtx only exists in Phantom Hourglass,
            # and, even there, not in every course.bin
            if 'mapModel.nsbtx' in courseNarc['folders']['tex']['files']:
                mapModel = courseNarc['folders']['tex']['files']['mapModel.nsbtx']
            else:
                mapModel = None

            # Load map**.bin's

            for mapNumber in range(100):
                mapBinFn = os.path.join(courseFolder, 'map%02d.bin' % mapNumber)
                if not os.path.isfile(mapBinFn): continue

                with open(mapBinFn, 'rb') as f:
                    mapBin = f.read()
                mapNarc = narc.load(lz10.decompress(mapBin))

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
                if mapNarc['folders']['mcb']['files']:
                    _, mcbFile = getOnlyItemFrom(mapNarc['folders']['mcb']['files'])
                else:
                    mcbFile = None

                # Load the model
                # (can be nonexistent in either game)
                # (can be a NSBTA instead of a NSBMD in Spirit Tracks)
                model = None
                isTA = False
                if mapNarc['folders']['nsbmd']['files']:
                    nsbmdFilename, model = getOnlyItemFrom(mapNarc['folders']['nsbmd']['files'])
                    isTA = nsbmdFilename.endswith('.nsbta')
                
                # Load the camera files (Spirit Tracks-only)
                cameraFiles = {}
                if 'zbcd' in mapNarc['folders']:
                    for camFilename, camFiledata in mapNarc['folders']['zbcd']['files'].items():
                        cameraFiles[int(camFilename[-7:-5])] = camFiledata
                
                # Load the ZCB and ZMB files
                _, zcbFile = getOnlyItemFrom(mapNarc['folders']['zcb']['files'])
                _, zmbFile = getOnlyItemFrom(mapNarc['folders']['zmb']['files'])

                # Load the ZOBs
                moTypes = []
                for zobNum in range(10):
                    for zobFile in mapNarc['folders']['zob']['files']:
                        if zobFile.startswith('motype_') and zobFile.endswith(f'_{zobNum}.zob'):
                            break
                    else:
                        break
                    moTypes.append(mapNarc['folders']['zob']['files'][zobFile])
                npcTypes = []
                for zobNum in range(10):
                    for zobFile in mapNarc['folders']['zob']['files']:
                        if zobFile.startswith('npctype_') and zobFile.endswith(f'_{zobNum}.zob'):
                            break
                    else:
                        break
                    npcTypes.append(mapNarc['folders']['zob']['files'][zobFile])
                assert len(moTypes) in (2, 10)
                assert len(npcTypes) in (2, 10)

                courseImg, printName = parseZmb(zmbFile)
                courseImg.save(f'courses/{courseFilename}_%02d.png' % mapNumber)
                if printName: print(courseFilename)


if __name__ == '__main__':
    main()