
import struct


import common


class LDLB:
    """
    Spirit Tracks-only: trigger zone
    """
    def __init__(self, game=None, data=None):
        self.data = data

        # First byte or two: zone ID
        # In Aboda Village:
        #     0 = Alfonso's train station trigger
        #     1 = ?
        #     2 = Zelda commenting on the town when at the station
        #     3 = ?
        #     4 = the girl that yells at you
        #     5 = Zelda coming out of your pocket when at the station

    def save(self, game):
        """
        Save the LDLB back to a bytes object.
        """
        return self.data

TEMP = set()


class Location:
    """
    A location.
    """
    def __init__(self, game=None, data=None):

        self.data = data

        if data is None:
            self.id = 0
            ...

        else:
            # TEMP.add(data[0x0F])
            # print(sorted(TEMP), str([hex(x) for x in sorted(TEMP)]).replace("'", ''))
            (self.id, unk01, unk02, self.y1, self.x1, self.y2, self.x2) = \
                struct.unpack_from('<BB5h', data)

    def save(self, game):
        """
        Save the location back to a bytes object.
        """
        return self.data


class Path:
    """
    A path.
    """
    def __init__(self, game=None, header=None):
        self.header = header
        self.nodes = []

    def save(self, game):
        """
        Save the path's header (only!) back to a bytes object.
        """
        return self.header


class PathNode:
    """
    A path node.
    """
    def __init__(self, game=None, data=None):
        self.data = data

    def save(self, game):
        """
        Save the node back to a bytes object.
        """
        return self.data


class Exit:
    """
    Defines an exit in a map.
    """
    def __init__(self, game=None, data=None):

        if data is None:
            self.id = 1
            self.destinationMap = 0
            self.destinationEntrance = 0
            self.destinationCourse = ''
            self.rotation = 0
            self.unk16 = 0
            self.unk17 = 1

        else:
            (self.id, self.destinationMap, self.destinationEntrance, destCourse,
                self.rotation, self.unk16, self.unk17) = \
                struct.unpack_from('<HBB16sHbb', data)
            self.destinationCourse = destCourse.rstrip(b'\0').decode('ascii')


    def save(self, game):
        """
        Save the exit back to a bytes object.
        """
        return struct.pack('<HBB16sHbb',
            self.id, self.destinationMap, self.destinationEntrance,
            self.destinationCourse.encode('ascii').ljust(16, b'\0'),
            self.rotation, self.unk16, self.unk17)


class CAME:
    """
    ?
    """
    def __init__(self, game=None, data=None):
        self.data = data

    def save(self, game):
        """
        Save the CAME back to a bytes object.
        """
        return self.data


class CMPT:
    """
    ?
    """
    def __init__(self, game=None, data=None):
        self.data = data

    def save(self, game):
        """
        Save the CMPT back to a bytes object.
        """
        return self.data


class Entrance:
    """
    Defines an entrance in a map.
    """
    def __init__(self, game=None, data=None):

        if data is None:
            self.x = self.y = self.z = 0
            self.rotation = 0
            self.id = 1
            self.unk0F = 0
            self.isZelda = False
            self.unk11 = 0
            self.useZPosition = False

        else:
            (self.x, self.z, self.y, self.rotation, self.id,
                self.unk0F, self.isZelda, self.unk11, self.useZPosition) = \
                struct.unpack_from('<IIIhbb?b?x', data)


    def save(self, game):
        """
        Save the exit back to a bytes object.
        """
        return struct.pack('<IIIhbb?b?x',
            self.x, self.z, self.y, self.rotation, self.id,
            self.unk0F, self.isZelda, self.unk11, self.useZPosition)


class MapObject:
    """
    A generally static object on a map, constrained to points on the
    tile grid.
    """
    def __init__(self, game=None, data=None):

        if data is None:
            # TODO: get better defaults here and in Actor
            self.type = 0 if game == common.Game.PhantomHourglass else '____'
            self.x = self.y = 0
            self.rotation = 0
            self.unk08 = 0
            self.unk0A = 0
            self.unk0C = 0
            self.unk0E = 0
            self.unk10 = 1 if game == common.Game.PhantomHourglass else 0
            self.unk11 = 1 if game == common.Game.PhantomHourglass else 0
            self.unk12 = 0
            self.unk13 = 0
            self.scriptID = 0
            self.unk1A = -1
            self.unk1B = 1

        else:
            (type, self.x, self.y, self.rotation, self.unk08, self.unk0A,
                    self.unk0C, self.unk0E, self.unk10, self.unk11, self.unk12,
                    self.unk13, self.scriptID, self.unk1A, self.unk1B) = \
                struct.unpack_from('<4sBB5H4BIbB2x', data)

            if game == common.Game.PhantomHourglass:
                self.type, = struct.unpack_from('<I', type)
            else:
                self.type = type[::-1].decode('ascii')


        # allScripts = {(200, 302), (100, 106), (300, 15), (102, 903), (101, 901), (200, 471), (200, 876), (200, 2), (161, 206), (600, 101), (130, 1), (100, 112), (106, 111), (121, 70), (121, 812), (200, 550), (131, 602), (141, 107), (100, 307), (131, 608), (101, 306), (142, 109), (104, 500), (111, 10), (122, 137), (130, 502), (200, 93), (132, 502), (120, 2), (101, 405), (200, 530), (151, 21), (122, 30), (150, 10), (121, 3), (100, 11), (161, 2), (101, 932), (200, 504), (132, 105), (101, 10), (200, 909), (323, 0), (102, 1), (100, 17), (300, 6), (142, 6), (101, 910), (101, 601), (103, 4), (1, 40), (100, 502), (141, 19), (101, 700), (200, 752), (131, 5), (200, 557), (132, 6), (101, 101), (201, 110), (141, 100), (104, 0), (110, 600), (310, 110), (100, 314), (101, 315), (600, 1), (200, 700), (107, 152), (200, 400), (132, 509), (200, 537), (200, 205), (121, 4), (131, 215), (122, 3), (322, 20), (101, 941), (200, 511), (161, 402), (310, 51), (200, 211), (323, 9), (102, 503), (110, 102), (141, 50), (111, 110), (322, 14), (131, 100), (140, 508), (1, 33), (200, 590), (121, 830), (100, 102), (101, 913), (131, 10), (151, 803), (121, 800), (104, 7), (122, 70), (200, 101), (200, 570), (105, 6), (122, 155), (105, 500), (601, 5), (200, 512), (141, 81), (111, 6), (122, 133), (1, 137), (141, 200), (151, 1), (200, 81), (101, 609), (122, 10), (310, 10), (200, 218), (210, 1), (323, 14), (321, 2), (100, 7), (322, 9), (140, 507), (132, 101), (101, 6), (200, 55), (200, 460), (104, 203), (112, 2), (161, 209), (323, 20), (100, 109), (141, 5), (161, 104), (101, 922), (100, 150), (200, 871), (200, 603), (161, 203), (101, 202), (100, 81), (101, 301), (107, 150), (101, 212), (200, 851), (100, 310), (101, 311), (122, 140), (142, 104), (310, 13), (100, 14), (322, 0), (200, 904), (103, 901), (101, 800), (141, 62), (100, 20), (200, 741), (300, 9), (102, 901), (104, 111), (101, 606), (105, 103), (200, 4), (122, 110), (141, 300), (161, 204), (600, 103), (100, 114), (151, 200), (200, 552), (131, 604), (310, 200), (200, 721), (141, 105), (122, 50), (100, 317), (131, 610), (101, 304), (202, 202), (122, 151), (131, 202), (200, 800), (130, 500), (200, 95), (120, 4), (200, 532), (601, 57), (200, 200), (131, 208), (101, 930), (200, 506), (101, 8), (100, 19), (300, 0), (142, 4), (105, 104), (103, 6), (1, 46), (100, 121), (131, 7), (132, 0), (151, 804), (112, 101), (104, 2), (200, 96), (105, 3), (101, 313), (200, 702), (107, 154), (200, 402), (601, 2), (200, 70), (110, 2), (121, 10), (321, 21), (122, 1), (322, 18), (101, 939), (110, 100), (1, 13), (200, 213), (210, 4), (102, 501), (161, 303), (321, 15), (111, 104), (322, 12), (131, 102), (200, 50), (101, 503), (323, 17), (141, 10), (102, 905), (101, 927), (101, 108), (104, 9), (105, 4), (200, 572), (100, 84), (122, 153), (142, 202), (110, 5), (310, 22), (150, 26), (122, 131), (142, 103), (200, 83), (1, 6), (100, 1), (322, 7), (140, 2), (132, 103), (140, 501), (101, 4), (101, 805), (112, 4), (141, 3), (100, 111), (300, 12), (101, 920), (200, 605), (161, 201), (130, 2), (100, 117), (101, 321), (200, 710), (101, 200), (200, 547), (131, 601), (100, 83), (106, 10), (121, 50), (141, 110), (101, 210), (200, 853), (310, 400), (100, 304), (200, 521), (1, 101), (101, 309), (141, 72), (142, 110), (121, 20), (601, 54), (200, 90), (1, 31), (130, 201), (100, 8), (101, 935), (200, 501), (101, 13), (200, 906), (105, 202), (101, 505), (141, 60), (102, 2), (300, 11), (161, 103), (142, 3), (105, 101), (101, 604), (200, 6), (1, 43), (200, 580), (121, 74), (200, 717), (131, 0), (131, 606), (200, 860), (200, 560), (101, 318), (150, 20), (131, 204), (101, 401), (200, 202), (131, 210), (101, 928), (1, 10), (130, 101), (121, 840), (323, 4), (102, 5), (200, 750), (300, 2), (200, 450), (1, 44), (200, 587), (112, 8), (100, 123), (101, 916), (131, 9), (132, 2), (151, 806), (200, 730), (201, 153), (104, 4), (121, 60), (105, 1), (200, 567), (105, 503), (132, 505), (200, 541), (110, 0), (150, 1), (111, 5), (122, 134), (141, 203), (322, 16), (101, 612), (101, 937), (1, 3), (200, 215), (323, 13), (107, 200), (161, 301), (151, 700), (100, 4), (200, 52), (322, 10), (131, 104), (140, 5), (140, 504), (104, 200), (101, 501), (323, 19), (141, 8), (161, 107), (101, 925), (200, 600), (132, 9), (101, 106), (201, 130), (100, 901), (104, 11), (101, 205), (105, 10), (100, 301), (103, 100), (100, 86), (106, 1), (101, 215), (142, 200), (323, 101), (310, 20), (111, 2), (142, 101), (601, 51), (131, 500), (200, 85), (1, 4), (2, 3), (100, 3), (100, 600), (322, 5), (140, 503), (101, 2), (200, 901), (122, 121), (101, 803), (112, 6), (141, 1), (200, 301), (100, 105), (161, 108), (102, 902), (101, 902), (200, 470), (200, 875), (200, 1), (300, 14), (161, 207), (600, 100), (121, 71), (100, 119), (200, 712), (106, 110), (131, 603), (141, 108), (101, 208), (100, 306), (131, 609), (101, 307), (141, 70), (122, 136), (142, 108), (131, 201), (130, 505), (601, 52), (132, 501), (101, 406), (100, 10), (161, 3), (101, 933), (200, 503), (132, 104), (101, 11), (200, 908), (105, 200), (323, 1), (100, 16), (300, 5), (161, 101), (111, 102), (101, 911), (101, 602), (103, 5), (1, 41), (142, 1), (100, 501), (200, 582), (141, 20), (121, 72), (201, 140), (101, 102), (201, 150), (141, 101), (110, 603), (100, 313), (200, 562), (310, 230), (101, 316), (600, 0), (107, 153), (131, 206), (132, 508), (200, 204), (310, 300), (161, 304), (131, 212), (161, 4), (101, 942), (200, 510), (1, 8), (310, 50), (200, 210), (323, 6), (102, 502), (321, 10), (111, 111), (101, 904), (131, 101), (300, 8), (103, 2), (1, 34), (112, 10), (100, 101), (101, 914), (131, 11), (151, 800), (121, 801), (200, 732), (104, 6), (200, 100), (105, 7), (122, 154), (105, 501), (601, 6), (132, 507), (101, 408), (300, 100), (111, 7), (122, 132), (1, 138), (141, 201), (151, 6), (200, 80), (101, 610), (1, 1), (200, 217), (210, 0), (321, 3), (100, 6), (322, 8), (140, 506), (132, 100), (101, 7), (200, 54), (104, 202), (120, 100), (112, 1), (100, 108), (300, 17), (161, 105), (101, 923), (200, 870), (200, 602), (101, 104), (104, 900), (121, 810), (200, 707), (104, 13), (101, 203), (105, 8), (100, 303), (310, 240), (100, 80), (101, 302), (107, 151), (101, 213), (200, 850), (100, 309), (142, 107), (151, 31), (131, 502), (200, 87), (122, 20), (2, 1), (130, 202), (100, 13), (100, 602), (322, 3), (200, 61), (200, 903), (101, 801), (141, 63), (200, 303), (200, 740), (100, 107), (102, 900), (101, 900), (101, 607), (200, 472), (200, 877), (104, 110), (200, 3), (200, 577), (161, 205), (600, 102), (141, 301), (100, 113), (200, 551), (131, 605), (201, 100), (110, 501), (200, 720), (141, 106), (100, 316), (131, 611), (101, 305), (122, 150), (104, 501), (131, 203), (130, 503), (200, 94), (132, 503), (120, 3), (101, 404), (200, 531), (121, 2), (131, 209), (161, 1), (101, 931), (200, 505), (101, 9), (100, 18), (200, 747), (300, 7), (105, 105), (103, 7), (1, 47), (100, 503), (141, 18), (121, 820), (100, 120), (132, 7), (151, 805), (200, 727), (112, 100), (104, 1), (110, 601), (122, 60), (100, 315), (200, 701), (600, 2), (101, 314), (200, 401), (601, 3), (310, 30), (200, 206), (131, 214), (151, 11), (101, 940), (110, 103), (161, 401), (1, 14), (200, 212), (102, 500), (111, 105), (322, 15), (131, 103), (1, 32), (200, 591), (141, 11), (100, 103), (102, 904), (200, 597), (101, 109), (151, 802), (106, 120), (104, 8), (200, 102), (200, 571), (105, 5), (201, 120), (122, 152), (601, 4), (110, 4), (150, 5), (141, 80), (122, 130), (142, 102), (1, 136), (200, 82), (101, 608), (1, 7), (310, 11), (2, 4), (100, 0), (322, 6), (140, 1), (132, 102), (140, 500), (101, 5), (200, 56), (112, 3), (161, 208), (100, 110), (101, 921), (100, 151), (122, 100), (200, 604), (161, 202), (310, 220), (141, 30), (100, 116), (101, 201), (100, 82), (101, 300), (121, 51), (141, 111), (101, 211), (200, 852), (122, 40), (100, 311), (200, 520), (142, 204), (101, 310), (142, 105), (130, 506), (601, 55), (310, 2), (151, 400), (100, 15), (322, 1), (200, 500), (200, 905), (105, 203), (102, 504), (141, 61), (200, 742), (300, 10), (111, 101), (105, 102), (101, 605), (200, 5), (103, 8), (142, 2), (100, 115), (131, 1), (131, 607), (200, 722), (141, 104), (200, 527), (101, 319), (121, 30), (131, 205), (200, 801), (130, 501), (601, 56), (120, 5), (101, 402), (200, 201), (131, 211), (200, 507), (130, 100), (323, 5), (102, 4), (300, 1), (142, 5), (103, 1), (1, 45), (151, 500), (100, 122), (131, 6), (200, 592), (132, 1), (151, 807), (201, 154), (104, 3), (105, 2), (101, 312), (601, 1), (200, 71), (132, 504), (200, 540), (110, 3), (321, 20), (141, 204), (322, 19), (101, 613), (101, 938), (121, 850), (200, 214), (323, 10), (161, 302), (111, 107), (322, 13), (131, 105), (140, 4), (200, 51), (101, 502), (323, 16), (141, 9), (104, 100), (101, 926), (132, 8), (101, 107), (100, 900), (104, 10), (101, 206), (310, 100), (105, 11), (100, 300), (100, 85), (121, 40), (200, 902), (142, 203), (310, 23), (111, 3), (142, 100), (131, 501), (200, 84), (1, 5), (141, 40), (2, 2), (151, 300), (100, 2), (322, 4), (140, 3), (140, 502), (101, 3), (200, 900), (101, 804), (122, 120), (112, 5), (141, 2), (200, 300), (200, 737), (161, 109), (300, 13), (101, 903), (100, 104), (310, 210), (130, 3), (100, 118), (101, 320), (200, 711), (300, 200), (131, 600), (106, 11), (141, 109), (101, 209), (100, 305), (200, 522), (210, 100), (1, 100), (101, 308), (141, 71), (130, 504), (200, 91), (132, 500), (101, 407), (601, 53), (1, 30), (100, 9), (101, 934), (200, 502), (200, 907), (105, 201), (101, 504), (102, 3), (300, 4), (161, 102), (111, 103), (105, 100), (101, 603), (200, 7), (1, 42), (100, 500), (200, 581), (121, 73), (131, 3), (132, 4), (101, 103), (201, 151), (141, 102), (110, 602), (100, 312), (200, 561), (101, 317), (202, 201), (131, 207), (101, 400), (200, 203), (150, 15), (121, 6), (131, 213), (161, 5), (322, 2), (1, 9), (323, 7), (200, 751), (300, 3), (101, 905), (103, 3), (1, 35), (112, 9), (100, 100), (200, 757), (101, 915), (131, 8), (132, 3), (151, 801), (121, 802), (200, 731), (201, 152), (104, 5), (151, 900), (105, 502), (151, 41), (132, 506), (101, 409), (200, 542), (110, 1), (122, 135), (1, 139), (151, 600), (141, 202), (322, 17), (101, 611), (101, 936), (1, 2), (200, 216), (210, 3), (323, 12), (100, 5), (322, 11), (140, 505), (200, 53), (104, 201), (101, 500), (323, 18), (300, 16), (161, 106), (101, 924), (200, 601), (132, 10), (101, 105), (121, 811), (106, 100), (100, 902), (104, 12), (101, 204), (105, 9), (100, 302), (100, 87), (101, 303), (101, 214), (142, 201), (100, 308), (200, 517), (323, 100), (310, 21), (150, 25), (142, 106), (1, 140), (601, 50), (131, 503), (200, 86), (321, 5), (100, 12), (100, 601), (200, 60), (101, 1), (101, 802), (112, 7)}
        # thisScript = (self.scriptID >> 16, self.scriptID & 0xFFFF)
        # if thisScript not in [(0, 0)] and thisScript not in allScripts:
        #     print('                                ', self.type)
        #     print('                                ', thisScript)
            #if self.type != 'PASS': raise


    def save(self, game):
        """
        Save the map object back to a bytes object.
        """
        if game == common.Game.PhantomHourglass:
            type = struct.pack('<I', self.type)
        else:
            type = self.type.encode('ascii')[::-1]

        return struct.pack('<4sBB5H4BIbB2x',
            type, self.x, self.y, self.rotation, self.unk08, self.unk0A,
            self.unk0C, self.unk0E, self.unk10, self.unk11, self.unk12,
            self.unk13, self.scriptID, self.unk1A, self.unk1B)



class Actor:
    """
    An object that can move and/or be interacted with more than map
    objects can.
    """
    def __init__(self, game=None, data=None):

        # unk1C can make actors disappear

        if data is None:
            self.type = '____'
            self.x = self.y = self.z = 0
            self.rotation = 0
            self.unk0C = 0
            self.unk10 = 0
            self.unk14 = 0
            self.scriptID = 0
            self.unk1C = 0

        else:
            (type, self.x, self.y, self.z, self.rotation, self.unk0C,
                    self.unk10, self.unk14, self.scriptID, self.unk1C) = \
                struct.unpack_from('<4s4h5I', data)
            self.type = type[::-1].decode('ascii')


    def save(self, game):
        """
        Save the actor back to a bytes object.
        """
        return struct.pack('<4s4h5I',
            self.type.encode('ascii')[::-1],
            self.x, self.y, self.z, self.rotation, self.unk0C, self.unk10,
            self.unk14, self.scriptID, self.unk1C)


class ZMB:
    """
    "Zelda Map Binary": a file defining most of the interesting things
    about a map.
    """
    def __init__(self, game=None, data=None):
        if data is not None:
            self._initFromData(game, data)


    def _initFromData(self, game, data):
        """
        Load a ZMB from data.
        """

        magic1, magic2, fileLen, sectionCount, unk10, unk14, unk18, unk1C = \
            struct.unpack_from('<4s4s6I', data)
        assert magic1 == b'MAPB'[::-1]
        assert magic2 == b'ZMB1'[::-1]
        assert fileLen == len(data)
        assert unk10 == unk14 == unk18 == unk1C == 0x01020304

        if game == common.Game.PhantomHourglass:
            assert sectionCount == 9
        else:
            assert sectionCount == 11

        offset = 0x20

        def sectionHeader(expectedMagic):
            """
            Helper function to read a standard section header and verify
            that the magic is as expected.
            """
            magic, len, count, unk0A = struct.unpack_from('<4sIHh', data, offset)
            assert magic == expectedMagic[::-1] # (reverse it because little-endian)
            return offset, len, count, unk0A


        # LDLB section (Spirit Tracks-only): Something to do with script triggers
        self.LDLB = []
        if game == common.Game.SpiritTracks:
            ldlbOffset, ldlbLen, ldlbCount, ldlbUnk0A = sectionHeader(b'LDLB')
            assert ldlbUnk0A == -1
            assert ldlbLen == 12 + 8 * ldlbCount

            for i in range(ldlbCount):
                baseOff = ldlbOffset + 12 + 8 * i
                self.LDLB.append(LDLB(game, data[baseOff : baseOff+8]))

            offset += ldlbLen


        # ROMB section
        rombOffset, rombLen, rombCount, rombUnk0A = sectionHeader(b'ROMB')
        assert rombUnk0A in (0x00, 0x30)
        assert rombLen == 12 + rombCount * 0xC0 # But it's more complicated than a simple table.

        self.rombCount = rombCount
        self.rombUnk0A = rombUnk0A
        self.rombData = data[rombOffset + 12 : rombOffset + rombLen]

        offset += rombLen


        # ROOM section: Room settings
        roomOffset, roomLen, roomCount, roomUnk0A = sectionHeader(b'ROOM')
        assert roomLen == 0x20
        assert roomCount == 1
        assert roomUnk0A == 0x0304

        (self.roomUnk0C, self.skyboxType, self.drawDistance, self.roomUnk10,
            self.musicID, self.lightingType, self.roomUnk14, self.roomUnk15,
            self.roomUnk16, self.roomUnk18, self.roomUnk19, self.roomUnk1A,
            self.roomUnk1B, self.roomUnk1C, self.roomUnk1D, self.roomUnk1E) = \
            struct.unpack_from('<bbhh4bHB5bH', data, roomOffset + 12)
        # interested = unk1D
        # if interested not in TEMP:
        #     TEMP[interested] = []
        # TEMP[interested].append(f'{courseNames[courseName]}/{mapNumber}')
        #print(hex(unk1D) + ',')
        # unk0C values: [0, 1, 2, 3, 4, 5, 12, 14, 18, 23, 24, 25, 26, 27, 28, 29, 30, 31, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65]
        # Skybox types: [-1, 0, 1, 2, 3, 4, 5, 7, 8, 9, 11, 12, 13, 14, 15, 16]
        # drawDistance: [1, 4, 5, 10, 15, 20, 30, 50]
        #     Setting it to 0 causes the pan-out in Aboda Village to show things spawning
        # unk10: [0, 1, 2]
        # unk14: [0, 1, 3, 4, 5, 6, 7, 8, 16, 17, 19, 21, 23, 24, 32, 33, 34, 35, 36, 39, 48, 49, 50, 51, 52, 56, 64, 65, 67, 68, 71, 80, 83, 88, 96, 115]
        # unk15: [0, 1, 2, 3, 4, 5, 6, 16, 17, 18, 20, 32, 35, 48, 50, 51, 52, 54, 64, 67, 80, 82, 83, 84, 86]
        # unk16: [0]
        # unk18: {0, 1, 2}
        # unk19: {-1, 0}
        # unk1A: {0, 1}
        # unk1B: {0, 1}
        # unk1C: [3, 11, 19, 35, 43, 131, 139, 147, 163, 171, 195, 267]
        # unk1E: [0]

        offset += roomLen


        # ARAB section: Locations
        arabEntryLen = 0x0C if game == common.Game.PhantomHourglass else 0x10
        arabOffset, arabLen, arabCount, arabUnk0A = sectionHeader(b'ARAB')
        assert arabUnk0A == -1
        assert arabLen == 12 + arabCount * arabEntryLen

        self.locations = []
        for i in range(arabCount):
            baseOff = arabOffset + 12 + arabEntryLen * i
            self.locations.append(Location(game, data[baseOff : baseOff+arabEntryLen]))

        offset += arabLen


        # RALB section: Paths
        ralbOffset, ralbLen, ralbCount, ralbUnk0A = sectionHeader(b'RALB')
        assert ralbUnk0A == -1

        self.paths = []
        off = ralbOffset + 12
        for i in range(ralbCount):
            headerLen = 8 if game == common.Game.SpiritTracks else 12
            header = data[off : off+headerLen]
            off += headerLen

            path = Path(game, header)
            self.paths.append(path)

            nodeCount = header[1]
            assert header[2] in [0, 1, 2]

            for j in range(nodeCount):
                if game == common.Game.SpiritTracks:
                    nodeLen = data[off + 0x12]
                else:
                    nodeLen = 12

                node = PathNode(game, data[off : off+nodeLen])
                path.nodes.append(node)
                off += nodeLen

        offset += ralbLen


        # WARP section: Exits
        warpOffset, warpLen, warpCount, warpUnk0A = sectionHeader(b'WARP')
        assert warpUnk0A == -1
        assert warpLen == 12 + 0x18 * warpCount

        self.exits = []
        for i in range(warpCount):
            baseOff = warpOffset + 12 + 0x18 * i
            self.exits.append(Exit(game, data[baseOff : baseOff + 0x18]))

        offset += warpLen


        # CAME section
        cameOffset, cameLen, cameCount, cameUnk0A = sectionHeader(b'CAME')
        assert cameUnk0A == -1
        assert cameLen == 12 + 0x1C * cameCount

        self.CAME = []
        for i in range(cameCount):
            baseOff = cameOffset + 12 + 0x1C * i
            self.CAME.append(CAME(game, data[baseOff : baseOff + 0x1C]))

        offset += cameLen


        # CMPT section (Spirit Tracks-only)
        self.CMPT = []
        if game == common.Game.SpiritTracks:
            cmptOffset, cmptLen, cmptCount, cmptUnk0A = sectionHeader(b'CMPT')
            assert cmptUnk0A == -1
            assert cmptLen == 12 + 0x10 * cmptCount

            for i in range(cmptCount):
                baseOff = cmptOffset + 12 + 0x10 * i
                self.CMPT.append(CMPT(game, data[baseOff : baseOff + 0x10]))

            offset += cmptLen


        # PLYR section: Entrances
        plyrEntryLen = 0x10 if game == common.Game.PhantomHourglass else 0x14
        plyrOffset, plyrLen, plyrCount, plyrUnk0A = sectionHeader(b'PLYR')
        assert plyrUnk0A == 0x0304
        assert plyrLen == 12 + plyrCount * plyrEntryLen

        self.entrances = []
        for i in range(plyrCount):
            baseOff = plyrOffset + 12 + plyrEntryLen * i
            self.entrances.append(Entrance(game, data[baseOff : baseOff + plyrEntryLen]))

        offset += plyrLen


        # MPOB section: Map Objects
        mpobOffset, mpobLen, mpobCount, mpobUnk0A = sectionHeader(b'MPOB')
        assert mpobUnk0A == -1
        assert mpobLen == 12 + 0x1C * mpobCount

        self.mapObjects = []
        for i in range(mpobCount):
            baseOff = mpobOffset + 12 + 0x1C * i
            self.mapObjects.append(MapObject(game, data[baseOff : baseOff + 0x1C]))

        offset += mpobLen


        # NPCA section: Actors
        npcaOffset, npcaLen, npcaCount, npcaUnk0A = sectionHeader(b'NPCA')
        assert npcaUnk0A == -1
        assert npcaLen == 12 + 0x20 * npcaCount

        self.actors = []
        for i in range(npcaCount):
            baseOff = npcaOffset + 12 + 0x20 * i
            self.actors.append(Actor(game, data[baseOff : baseOff + 0x20]))


    def save(self, game):
        """
        Save the map back to a bytes object.
        """

        data = bytearray(0x20)

        sections = []


        # LDLB
        if game == common.Game.SpiritTracks:
            ldlbData = bytearray()
            for ldlb in self.LDLB:
                ldlbData.extend(ldlb.save(game))
            sections.append((b'LDLB', len(self.LDLB), -1, ldlbData))

        elif self.LDLB:
            print('WARNING: Ignoring nonempty LDLB section!!')


        # ROMB
        sections.append((b'ROMB', self.rombCount, self.rombUnk0A, self.rombData))


        # ROOM
        roomData = struct.pack('<bbhh4bHB5bH',
            self.roomUnk0C, self.skyboxType, self.drawDistance, self.roomUnk10,
            self.musicID, self.lightingType, self.roomUnk14, self.roomUnk15,
            self.roomUnk16, self.roomUnk18, self.roomUnk19, self.roomUnk1A,
            self.roomUnk1B, self.roomUnk1C, self.roomUnk1D, self.roomUnk1E)
        sections.append((b'ROOM', 1, 0x0304, roomData))


        # ARAB
        arabData = bytearray()
        for loc in self.locations:
            arabData.extend(loc.save(game))
        sections.append((b'ARAB', len(self.locations), -1, arabData))


        # RALB
        ralbData = bytearray()
        for path in self.paths:
            ralbData.extend(path.save(game))
            for node in path.nodes:
                ralbData.extend(node.save(game))
        sections.append((b'RALB', len(self.paths), -1, ralbData))


        # WARP
        warpData = bytearray()
        for warp in self.exits:
            warpData.extend(warp.save(game))
        sections.append((b'WARP', len(self.exits), -1, warpData))


        # CAME
        cameData = bytearray()
        for came in self.CAME:
            cameData.extend(came.save(game))
        sections.append((b'CAME', len(self.CAME), -1, cameData))


        # CMPT
        if game == common.Game.SpiritTracks:
            cmptData = bytearray()
            for cmpt in self.CMPT:
                cmptData.extend(cmpt.save(game))
            sections.append((b'CMPT', len(self.CMPT), -1, cmptData))

        elif self.CMPT:
            print('WARNING: Ignoring nonempty CMPT section!!')


        # PLYR
        plyrData = bytearray()
        for plyr in self.entrances:
            plyrData.extend(plyr.save(game))
        sections.append((b'PLYR', len(self.entrances), 0x0304, plyrData))


        # MPOB
        mpobData = bytearray()
        for mpob in self.mapObjects:
            mpobData.extend(mpob.save(game))
        sections.append((b'MPOB', len(self.mapObjects), -1, mpobData))


        # NPCA
        npcaData = bytearray()
        for npca in self.actors:
            npcaData.extend(npca.save(game))
        sections.append((b'NPCA', len(self.actors), -1, npcaData))


        # Put the sections together
        for magic, count, unk0A, sectionData in sections:
            data.extend(struct.pack('<4sIHh', magic[::-1], 12 + len(sectionData), count, unk0A))
            data.extend(sectionData)

        # Add the ZMB header
        struct.pack_into('<4s4s6I', data, 0,
            b'MAPB'[::-1], b'ZMB1'[::-1], len(data), len(sections),
            0x01020304, 0x01020304, 0x01020304, 0x01020304)

        return data


    def renderPNG(self):
        """
        TESTING ONLY: Render a PNG map of the stage.
        """
        import PIL.Image, PIL.ImageDraw, PIL.ImageFont

        IMGW, IMGH = 1024, 1024
        IMGW += 80; IMGH += 80
        
        image = PIL.Image.new('RGBA', (IMGW, IMGH), (0, 0, 0, 0))
        draw = PIL.ImageDraw.Draw(image)
        font = PIL.ImageFont.truetype('/usr/share/fonts/truetype/noto/NotoMono-Regular.ttf', 10)

        stuff = []
        lines = []
        rects = []
        for obj in self.mapObjects:
            t = obj.type
            if isinstance(t, int): t = f'({t})'
            stuff.append(((255,0,0,255), t, obj.x << 4, obj.y << 4))
        for i, path in enumerate(self.paths):
            lastXY = None
            for j, node in enumerate(path.nodes):
                if len(node.data) == 12: continue # skip PH
                x, = struct.unpack_from('<i', node.data, 4)
                z, = struct.unpack_from('<i', node.data, 8)
                y, = struct.unpack_from('<i', node.data, 12)
                x >>= 8; y >>= 8
                x += 0x200; y += 0x180
                stuff.append(((255,0,255,255), f'{i}/{j}', x, y))
                if lastXY is not None:
                    lines.append(((255,0,255,255), lastXY, (x, y)))
                lastXY = x, y
        for act in self.actors:
            stuff.append(((0,0,0,255), act.type, act.x, act.y))
        for ent in self.entrances:
            stuff.append(((0,0,255,255), "Ent.", ent.x >> 12, ent.y >> 12))
        for loc in self.locations:
            x1, y1, x2, y2 = loc.x1, loc.y1, loc.x2, loc.y2
            x1 += 0x200; x2 += 0x200
            y1 += 0x180; y2 += 0x180
            rects.append(((255,127,0,255), (255,127,0,63), (x1, y1), (x2, y2)))
            stuff.append(((255,127,0,255), str(loc.id), x1 + 1, y1 + 1))

        if stuff:
            minX = minY = 0xFFFF
            maxX = maxY = 0
            for _, name, xPos, yPos in stuff:
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

            for outline, fill, (x1, y1), (x2, y2) in rects:
                x1a, y1a = canvasPos(x1, y1)
                x2a, y2a = canvasPos(x2, y2)
                drawRect(image, [(x1a, y1a), (x2a, y2a)], fill, outline)

            for color, name, xPos, yPos in stuff:
                assert (xPos >> 4) <= 256
                assert (yPos >> 4) <= 256

                x, y = canvasPos(xPos, yPos)

                draw.text((x, y), name, color, font=font)

            for color, (x1, y1), (x2, y2) in lines:
                x1a, y1a = canvasPos(x1, y1)
                x2a, y2a = canvasPos(x2, y2)
                draw.line([(x1a, y1a), (x2a, y2a)], color, 2)

        return image




# TEMP
def drawRect(img, xy, fill=None, outline=None):
    """
    https://stackoverflow.com/a/3120700
    """
    import PIL.Image, PIL.ImageDraw
    import math

    (x1, y1), (x2, y2) = xy
    x1 = max(x1, 0); y1 = max(y1, 0)
    w, h = x2 - x1, y2 - y1
    rect = PIL.Image.new('RGBA', (math.ceil(w), math.ceil(h)))
    rdraw = PIL.ImageDraw.Draw(rect)
    rdraw.rectangle([(0, 0), (w, h)],
                  fill=fill, outline=outline)
    img.alpha_composite(rect, dest=(int(x1), int(y1)))