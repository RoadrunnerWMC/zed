
import enum
import struct

import common


class TopScreenMode(enum.IntEnum):
    map = 0
    camera = 1


def neg1AsNone(value):
    return None if value == -1 else value

def noneAsNeg1(value):
    return -1 if value is None else value


class CourseListInitMapEntry:
    """
    A single map entry within a courselist/courseinit course entry.
    """
    def __init__(self, game=None, data=None):
        self.mapID = 0
        self.unk01 = None
        self.unk02 = None
        if data is not None:
            self._initFromData(game, data)


    def _initFromData(self, game, data):
        # Note: it's definitely possible that these aren't the same two
        # unks. But it's a reasonable guess, I think?
        if game == common.Game.PhantomHourglass:
            self.mapID, unk01, unk02 = struct.unpack_from('<Bxxxhh', data)
        else:
            self.mapID, unk01, unk02 = struct.unpack_from('<Bbh', data)

        self.unk01 = neg1AsNone(unk01)
        self.unk02 = neg1AsNone(unk02)


    def save(self, game):
        unk01 = noneAsNeg1(self.unk01)
        unk02 = noneAsNeg1(self.unk02)

        if game == common.Game.PhantomHourglass:
            return struct.pack('<4Bhh',
                self.mapID, 0xFF, 0xFF, 0xFF,
                unk01, unk02)
        else:
            return struct.pack('<Bbh', self.mapID, unk01, unk02)



class CourseListInitCourseEntry:
    """
    A single courselist/courseinit entry.
    """
    def __init__(self, game=None, listData=None, initData=None):
        self.name = ''
        self.title = ''
        self.maps = []
        self.dungeonID = None

        if listData is not None:
            self._initFromData(game, listData, initData)


    def _initFromData(self, game, listData, initData):
        if game == common.Game.PhantomHourglass:
            initData = None
        else:
            if initData is None:
                raise ValueError("Can't parse Spirit Tracks courselist data without courseinit")

        # Parse list data
        dataLen, = struct.unpack_from('<I', listData)

        off = 4

        self.name = listData[off : off+0x10].rstrip(b'\0').decode('shift-jis')
        off += 0x10

        if game == common.Game.PhantomHourglass:
            self.title = listData[off : off+0x10].rstrip(b'\0').decode('shift-jis')
            off += 0x10

        self.unk14, = struct.unpack_from('<I', listData, off)
        off += 4

        if game == common.Game.PhantomHourglass:
            (vehicleCourse, self.initUnk16,
                self.phUnk2C,
                self.phUnk30, self.phUnk32,
                self.phUnk34, self.phUnk35, self.phUnk36, mapCount,
                self.phUnk38) = struct.unpack_from('<HHihh4Bi', listData, off)
            off += 0x14

            self.vehicleCourse = bool(vehicleCourse)

        else:
            (mapCount, self.unk19, self.nameID, self.unk1B,
                topScreenMode, self.unk1E, self.unk1F,
                self.sdatGroupID, self.unk22, self.unk23,
                self.mapDrawID, self.unk25, self.unk26, self.unk27) = struct.unpack_from('<BbbbHbbH6b', listData, off)
            off += 0x10

            self.nameID = neg1AsNone(self.nameID) # maingame.bmg, message (152 + value)
            self.unk1B = neg1AsNone(self.unk1B)
            self.topScreenMode = TopScreenMode(topScreenMode)
            self.unk22 = neg1AsNone(self.unk22)
            self.mapDrawID = neg1AsNone(self.mapDrawID)
            self.unk25 = neg1AsNone(self.unk25)
            self.unk27 = neg1AsNone(self.unk27)

        self.maps = []
        mapEntryLen = 8 if game == common.Game.PhantomHourglass else 4
        for i in range(mapCount):
            self.maps.append(CourseListInitMapEntry(game, listData[off : off+mapEntryLen]))
            off += mapEntryLen

        if off < dataLen:
            self.dungeonID, = struct.unpack_from('<I', listData, off)
        else:
            self.dungeonID = None

        if game == common.Game.SpiritTracks:
            # Parse init data
            self.title = initData[0x04:0x14].rstrip(b'\0').decode('shift-jis')
            (vehicleCourse, self.initUnk16,
                self.bmgID,
                self.initUnk1C, self.initUnk1E,
                self.initUnk20, self.initUnk22,
                self.initUnk24, self.initUnk26) = struct.unpack_from('<HHI6H', initData, 0x14)
            self.vehicleCourse = bool(vehicleCourse)


    def save(self, game):

        listData = bytearray(4)
        initData = bytearray(4)

        listData.extend(self.name.encode('shift-jis').ljust(16, b'\0'))

        if game == common.Game.PhantomHourglass:
            listData.extend(self.title.encode('shift-jis').ljust(16, b'\0'))
        else:
            initData.extend(self.title.encode('shift-jis').ljust(16, b'\0'))

        listData.extend(struct.pack('<I', self.unk14))

        if game == common.Game.PhantomHourglass:
            listData.extend(struct.pack('<HHihh4Bi',
                self.vehicleCourse, self.initUnk16,
                self.phUnk2C,
                self.phUnk30, self.phUnk32,
                self.phUnk34, self.phUnk35, self.phUnk36, len(self.maps),
                self.phUnk38))
        else:
            nameID = noneAsNeg1(self.nameID)
            unk1B = noneAsNeg1(self.unk1B)
            unk22 = noneAsNeg1(self.unk22)
            mapDrawID = noneAsNeg1(self.mapDrawID)
            unk25 = noneAsNeg1(self.unk25)
            unk27 = noneAsNeg1(self.unk27)
            listData.extend(struct.pack('<BbbbHbbH6b',
                len(self.maps), self.unk19, nameID, unk1B,
                self.topScreenMode, self.unk1E, self.unk1F,
                self.sdatGroupID, unk22, self.unk23,
                mapDrawID, unk25, self.unk26, unk27))
            initData.extend(struct.pack('<HHI6H',
                self.vehicleCourse, self.initUnk16,
                self.bmgID,
                self.initUnk1C, self.initUnk1E,
                self.initUnk20, self.initUnk22,
                self.initUnk24, self.initUnk26))

        for m in self.maps:
            listData.extend(m.save(game))

        if self.dungeonID is not None:
            listData.extend(struct.pack('<I', self.dungeonID))

        struct.pack_into('<I', listData, 0, len(listData))
        struct.pack_into('<I', initData, 0, len(initData))

        if game == common.Game.PhantomHourglass:
            return bytes(listData), None
        else:
            return bytes(listData), bytes(initData)



def loadCourseListAndInit(game, listData, initData=None):
    """
    Load courselist.clb and courseinit.cib (if it exists) together, and
    return a list of CourseListInitCourseEntrys.
    """

    if game == common.Game.PhantomHourglass:
        if initData is not None:
            print('WARNING: Ignoring courseinit data because Phantom Hourglass')
            initData = None
    else:
        if initData is None:
            raise ValueError("Can't parse Spirit Tracks courselist data without courseinit")


    listMagic, listWrongFileLen, entriesCount1, entriesCount2 = \
        struct.unpack_from('<4s3I', listData, 0)
    if listMagic != b'ZCLB':
        raise ValueError(f'Not a valid course list file')

    if initData is not None:
        initMagic, initFileLen, entriesCount3, entriesCount4 = \
            struct.unpack_from('<4s3I', initData, 0)
        if initMagic != b'ZCIB':
            raise ValueError(f'Not a valid course initialization file')


    entries = []
    listOffset = initOffset = 0x10
    for i in range(entriesCount1):
        listEntryLength, = struct.unpack_from('<I', listData, listOffset)
        listEntryData = listData[listOffset : listOffset+listEntryLength]

        if initData is not None:
            initEntryLength, = struct.unpack_from('<I', initData, initOffset)
            initEntryData = initData[initOffset : initOffset+initEntryLength]
        else:
            initEntryLength = 0
            initEntryData = None

        entries.append(
            CourseListInitCourseEntry(game, listEntryData, initEntryData))

        listOffset += listEntryLength
        initOffset += initEntryLength

    return entries


def saveCourseListAndInit(game, entries):
    """
    Save a list of CourseListInitCourseEntrys back to bytes objects
    representing courselist.clb and courseinit.cib.
    """
    listData = bytearray()
    initData = bytearray()

    # The value right after the file magic is supposed to be the file's
    # total length. However, Nintendo calculated it incorrectly. Here's
    # the formula they used:
    supposedEntrySize = 0x3C if game == common.Game.PhantomHourglass else 0x28
    wrongFileLen = 0x10 + supposedEntrySize * len(entries)
    # The mistake is that they forgot to take into account the lists of
    # maps in each course entry. Because of these lists, entries have
    # variable length, so a simple multiplication like this is
    # incorrect.
    # At any rate, we do things the same way as Nintendo when possible,
    # so we'll be using that value for file length instead of the true
    # value.
    # Also note that because courseinit has no map lists, wrongFileLen
    # actually happens to be correct for that particular file.

    listData.extend(struct.pack('<4s3I', b'ZCLB', wrongFileLen, len(entries), len(entries)))
    initData.extend(struct.pack('<4s3I', b'ZCIB', wrongFileLen, len(entries), len(entries)))

    for e in entries:
        listEntry, initEntry = e.save(game)
        listData.extend(listEntry)
        if initEntry is not None:
            initData.extend(initEntry)

    if game == common.Game.PhantomHourglass:
        return bytes(listData), None
    else:
        return bytes(listData), bytes(initData)