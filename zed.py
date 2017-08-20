# 8/19/17
# Zed: Zelda EDitor
# (Phantom Hourglass and Spirit Tracks)
# By RoadrunnerWMC
# License: GNU GPL v3

import collections
import os, os.path
import struct

import fnttool


# Nintendo DS standard file header:
NDS_STD_FILE_HEADER = struct.Struct('<4sIIHH')
# - Magic
# - Unk (0x0100FEFF or 0x0100FFFE; maybe a BOM or something?)
# - File size (including this header)
# - Size of this header (16)
# - Number of blocks

ROOT_ST = '../RETAIL/st/root'
ROOT_PH = '../RETAIL/ph/root'


def loadNarc(data):
    """
    Load a NARC from data
    """
    # Read the standard header
    magic, unk04, filesize, headersize, numblocks = \
        NDS_STD_FILE_HEADER.unpack_from(data, 0)

    if magic != b'NARC':
        raise ValueError("Wrong magic (should be b'NARC', instead found "
                         f'{magic})')

    # Read the file allocation block
    fatbMagic, fatbSize, fileCount = struct.unpack_from('<4sII', data, 0x10)
    assert fatbMagic == b'FATB'[::-1]

    fileSlices = []
    for i in range(fileCount):
        startOffset, endOffset = struct.unpack_from('<II', data, 0x1C + 8 * i)
        fileSlices.append((startOffset, endOffset - startOffset))

    # Read the file name block
    fntbOffset = 0x10 + fatbSize
    fntbMagic, fntbSize = struct.unpack_from('<4sI', data, fntbOffset)
    assert fntbMagic == b'FNTB'[::-1]

    # Get the data from the file data block before continuing
    fimgOffset = fntbOffset + fntbSize
    fimgMagic, gmifSize = struct.unpack_from('<4sI', data, fimgOffset)
    assert fimgMagic == b'FIMG'[::-1]
    rawDataOffset = fimgOffset + 8

    # Parse the filenames and files

    names = fnttool.fnt2Dict(data[fntbOffset + 8 : fntbOffset + fntbSize])

    def makeFolder(info):
        root = {}
        root['folders'] = collections.OrderedDict()
        root['files'] = collections.OrderedDict()

        for fname, fdict in info.get('folders', {}).items():
            root['folders'][fname] = makeFolder(fdict)

        id = info['first_id']
        for file in info.get('files', []):
            start, length = fileSlices[id]
            start += rawDataOffset
            fileData = data[start : start+length]
            root['files'][file] = fileData
            id += 1

        return root

    return makeFolder(names)


def decompress_LZ10(data):
    assert data[0] == 0x10

    # This code is ported from NSMBe, which was converted from Elitemap.
    dataLen = struct.unpack_from('<I', data)[0] >> 8

    out = bytearray(dataLen)
    inPos, outPos = 4, 0

    while dataLen > 0:
        d = data[inPos]; inPos += 1

        if d:
            for i in range(8):
                if d & 0x80:
                    thing, = struct.unpack_from('>H', data, inPos); inPos += 2

                    length = (thing >> 12) + 3
                    offset = thing & 0xFFF
                    windowOffset = outPos - offset - 1

                    for j in range(length):
                        out[outPos] = out[windowOffset]
                        outPos += 1; windowOffset += 1; dataLen -= 1

                        if dataLen == 0:
                            return bytes(out)

                else:
                    out[outPos] = data[inPos]
                    outPos += 1; inPos += 1; dataLen -= 1

                    if dataLen == 0:
                        return bytes(out)

                d <<= 1
        else:
            for i in range(8):
                out[outPos] = data[inPos]
                outPos += 1; inPos += 1; dataLen -= 1

                if dataLen == 0:
                    return bytes(out)

    return bytes(out)


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

    # MPOB section
    mpobLen, mpobCount, mpobUnk0A = sectionHeader(b'MPOB')
    assert mpobUnk0A == -1
    assert mpobLen == 12 + 0x1C * mpobCount

    for i in range(mpobCount):
        objType, unk04, unk08, unk0C, unk10, unk14, unk18 = \
            struct.unpack_from('<4s6I', zmb, offset + 12 + 0x1C * i)
        if version == 9:
            objType, = struct.unpack_from('<I', objType)
            objType = f'({objType})'
        else:
            objType = objType[::-1].decode('ascii')

    offset += mpobLen

    # NPCA section
    npcaLen, npcaCount, npcaUnk0A = sectionHeader(b'NPCA')
    assert npcaUnk0A == -1
    assert npcaLen == 12 + 0x20 * npcaCount

    for i in range(npcaCount):
        npcType, xPos, yPos, zPos, rot, unk0C, unk10, unk14, unk18, unk1C = \
            struct.unpack_from('<4s4h5I', zmb, offset + 12 + 0x20 * i)
        npcType = npcType[::-1].decode('ascii')

        # unk18 is related to dialogue/script
        # unk1C can make NPCs disappear


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
            courseNarc = loadNarc(decompress_LZ10(courseBin))

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

            for i in range(100):
                mapBinFn = os.path.join(courseFolder, 'map%02d.bin' % i)
                if not os.path.isfile(mapBinFn): continue

                with open(mapBinFn, 'rb') as f:
                    mapBin = f.read()
                mapNarc = loadNarc(decompress_LZ10(mapBin))

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
                for i in range(10):
                    for zobFile in mapNarc['folders']['zob']['files']:
                        if zobFile.startswith('motype_') and zobFile.endswith(f'_{i}.zob'):
                            break
                    else:
                        break
                    moTypes.append(mapNarc['folders']['zob']['files'][zobFile])
                npcTypes = []
                for i in range(10):
                    for zobFile in mapNarc['folders']['zob']['files']:
                        if zobFile.startswith('npctype_') and zobFile.endswith(f'_{i}.zob'):
                            break
                    else:
                        break
                    npcTypes.append(mapNarc['folders']['zob']['files'][zobFile])
                assert len(moTypes) in (2, 10)
                assert len(npcTypes) in (2, 10)

                parseZmb(zmbFile)


if __name__ == '__main__':
    main()