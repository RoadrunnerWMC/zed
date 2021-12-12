import struct

import common


class ZOB:
    def __init__(self, game=None, data=None):
        if data is not None:
            self._initFromData(game, data)
        else:
            self.unk08 = 0
            self.unk0A = 0
            self.unk0E = 0
            self.entries = []

    def _initFromData(self, game, data):
        magic, fileLen, self.unk08, self.unk0A, entriesCount, self.unk0E = \
            struct.unpack_from('<4sI4h', data, 0)
        assert magic == b'ZOLB'

        textBlob = data[0x10 : 0x10 + 4 * entriesCount].decode('latin-1')

        if game == common.Game.PhantomHourglass:
            # Heuristics~
            isStrings = textBlob.isprintable()
        else:
            isStrings = True

        self.entries = []
        for i in range(entriesCount):
            if isStrings:
                self.entries.append(textBlob[4 * i : 4 * i + 4][::-1])
            else:
                self.entries.append(struct.unpack_from('<I', data, 0x10 + 4 * i)[0])


    def save(self, game):
        """
        Save the ZOB back to a bytes object.
        """

        data = bytearray(0x10)

        for e in self.entries:
            if isinstance(e, int):
                data.extend(struct.pack('<I', e))
            else:
                data.extend(e.encode('ascii')[::-1])

        struct.pack_into('<4sI4h', data, 0,
            b'ZOLB', len(data), self.unk08, self.unk0A, len(self.entries),
            self.unk0E)

        return data


    def __eq__(self, other):
        if self.unk08 != other.unk08: return False
        if self.unk0A != other.unk0A: return False
        if self.unk0E != other.unk0E: return False
        return self.entries == other.entries
