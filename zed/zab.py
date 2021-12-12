import struct

import common


class ZAB:
    """
    Zelda Area Boundaries. Used for syncing the top-screen map with the
    actual 3D world.
    """
    def __init__(self, game=None, data=None):
        if data is not None:
            self._initFromData(game, data)

    def _initFromData(self, game, data):
        magic, fileLen, sectionCount, unk0C = \
            struct.unpack_from('<4sIIi', data, 0)
        assert magic == b'ZCAB'
        assert sectionCount == 2
        assert unk0C == -1

        offset = 0x10

        # CABM
        cabmMagic, cabmSize, cabmUnk08, cabmUnk0C, cabmUnk0D, cabmCount = struct.unpack_from('<4sIIBBH', data, offset)
        assert cabmMagic[::-1] == b'CABM'
        # cabmUnk08 is maybe four separate values? Since 0x04040404 is used once?
        assert cabmUnk0C in [0, 1, 2]
        assert cabmUnk0D in [0, 1, 2]
        assert cabmCount * 8 == cabmSize - 16

        self.cabmUnk08 = cabmUnk08
        self.cabmUnk0C = cabmUnk0C
        self.cabmUnk0D = cabmUnk0D

        self.CABM = []
        for i in range(cabmCount):
            entryOff = offset + 16 + 8 * i
            self.CABM.append(data[entryOff : entryOff + 8])

        offset += cabmSize

        # CABI
        cabiMagic, cabiSize, cabiCount, cabiUnk0A = struct.unpack_from('<4sIHh', data, offset)
        assert cabiMagic[::-1] == b'CABI'
        assert cabiUnk0A == -1

        self.CABI = []
        for i in range(cabiCount):
            entryOff = offset + 12 + 12 * i
            self.CABI.append(data[entryOff : entryOff + 12])


    def save(self, game):
        """
        Save the ZAB back to a bytes object.
        """

        data = bytearray(0x10)

        # CABM
        data.extend(struct.pack('<4sIIBBH',
            b'CABM'[::-1], 16 + len(self.CABM) * 8, self.cabmUnk08,
            self.cabmUnk0C, self.cabmUnk0D, len(self.CABM)))
        for c in self.CABM:
            data.extend(c)

        # CABI
        data.extend(struct.pack('<4sIHh',
            b'CABI'[::-1], 12 + len(self.CABI) * 12, len(self.CABI), -1))
        for c in self.CABI:
            data.extend(c)

        # ZAB header
        struct.pack_into('<4sIIi', data, 0,
            b'ZCAB', len(data), 2, -1)

        return data