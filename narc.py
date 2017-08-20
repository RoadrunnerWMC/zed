
import collections
import struct

import fnttool

# Nintendo DS standard file header:
NDS_STD_FILE_HEADER = struct.Struct('<4sIIHH')
# - Magic
# - Unk (0x0100FEFF or 0x0100FFFE; maybe a BOM or something?)
# - File size (including this header)
# - Size of this header (16)
# - Number of blocks


def load(data):
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


def save(narc):
    """
    Save a NARC back to data
    """

    fileDatas = []
    nextId = 0

    def parseFolder(folder):
        nonlocal nextId

        output = collections.OrderedDict()
        output['first_id'] = nextId

        output['folders'] = collections.OrderedDict()
        for fname, fdict in folder.get('folders', {}).items():
            temp = parseFolder(fdict)
            if temp: output['folders'][fname] = temp
        if not output['folders']:
            del output['folders']

        output['files'] = list(folder.get('files', {}).keys())
        if not output['files']:
            del output['files']
        for fname, fdata in folder.get('files', {}).items():
            fileDatas.append(fdata)
            nextId += 1

        return output

    fntDict = parseFolder(narc)
    nameTable = bytearray(fnttool.dict2Fnt(fntDict, isNarc=True))
    while len(nameTable) % 4:
        nameTable.append(0xFF)

    numFiles = len(fileDatas)

    fimgData = bytearray(8)

    fatbData = bytearray()
    fatbData.extend(struct.pack('<4sII', b'FATB'[::-1], 0x0C + 8 * numFiles, numFiles))

    for i, fd in enumerate(fileDatas):
        startOff = len(fimgData) - 8
        fimgData.extend(fd)
        endOff = startOff + len(fd)
        fatbData.extend(struct.pack('<II', startOff, endOff))
        while len(fimgData) % 4:
            fimgData.append(0)

    struct.pack_into('<4sI', fimgData, 0, b'FIMG'[::-1], len(fimgData))

    fntbData = struct.pack('<4sI', b'FNTB'[::-1], len(nameTable) + 8) + nameTable

    data = bytearray(0x10)
    data.extend(fatbData)
    data.extend(fntbData)
    data.extend(fimgData)
    NDS_STD_FILE_HEADER.pack_into(data, 0, b'NARC', 0x0100FFFE, len(data), 0x10, 3)

    return bytes(data)