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
    assert courseInit.startswith(b'ZCIB')
    assert courseList.startswith(b'ZCLB')

    finalList = []

    zcibMagic, initUnk04, entriesCount1, entriesCount2 = struct.unpack_from('<4s3I', courseInit)
    zclbMagic, listUnk04, entriesCount3, entriesCount4 = struct.unpack_from('<4s3I', courseList)

    # Why are there four entries counts?
    assert entriesCount1 == entriesCount2 == entriesCount3 == entriesCount4

    initOffset = listOffset = 0x10
    for i in range(entriesCount1):
        initEntryLength = struct.unpack_from('<I', courseInit, initOffset)[0]
        listEntryLength = struct.unpack_from('<I', courseList, listOffset)[0]
        entryName = courseInit[initOffset + 4 : initOffset + 0x14].rstrip(b'\0').decode('shift-jis')
        entryFile = courseList[listOffset + 4 : listOffset + 0x14].rstrip(b'\0').decode('shift-jis')

        finalList.append((entryName, entryFile))

        initOffset += initEntryLength
        listOffset += listEntryLength

    return finalList

def main():
    with open(os.path.join(ROOT_ST, 'Course/courseinit.cib'), 'rb') as f:
        courseinit = f.read()
    with open(os.path.join(ROOT_ST, 'Course/courselist.clb'), 'rb') as f:
        courselist = f.read()

    courses = parseCourselist(courseinit, courselist)

    print(courses)

    # for dir, folders, files in os.walk(ROOT_ST):
    #     for file in files:
    #         full = os.path.join(dir, file)
    #         with open(full, 'rb') as f:
    #             fd = f.read()
    #         if fd.startswith(b'\x10') and not file.endswith('ntfp'):
    #             print(full + 'as LZ10')
    #             fd = decompress_LZ10(fd)
    #             print(fd.startswith(b'NARC'))
    #         if fd.startswith(b'NARC'):
    #             print(full + ' as narc')
    #             narc = loadNarc(fd)
    #             #print(narc)

if __name__ == '__main__':
    main()