# 9/15/17
# Making a master SBNK for this game.

SDAT_PATH = 'Testing/st/root/SoundData/final_sound_data.sdat'

import ndspy.soundArchive
import ndspy.soundBank


names = {
    0: 'Silence',
    1: 'Phantom Hourglass Titlescreen / Great Sea',
    2: 'Phantom Hourglass Titlescreen / Great Sea (Duplicate)',
    3: 'File Select',
    4: 'Zelda\'s Flute Performance',
    5: 'You got soldier\'s wear!',
    6: 'Sneaking with Zelda',
    7: 'Sword Explanation 1',
    8: 'Sword Explanation 2',
    9: 'Sword Explanation 3',
    10: 'Sword Training 1',
    11: 'Sword Training 2',
    12: 'Sword Training 3',
    13: 'Sword Minigame Quiet',
    14: 'Minigame',
    15: 'Enemy Encounter ',
    16: 'Minigame Alt.',
    17: 'Decide the train path!',
    18: 'Peaceful Realm Train Journey',
    19: 'Train Tutorial',
    20: 'Train Tutorial (Duplicate)',
    21: 'Lost Woods',
    22: 'Blizzard',
    23: 'Dire Weather Train Journey',
    24: 'Underwater Train Journey',
    25: 'Fire Realm Key Enemy Battle',
    26: 'Silence',
    27: 'Dark Realm Train Journey',
    28: 'Enemy Train Encounter',
    29: 'Dark Train Chase',
    30: 'Train Tutorial (Duplicate 2)',
    31: 'Pirates!',
    32: 'Pirates! (no intro)',
    33: 'Overworld',
    34: 'Overworld (Duplicate)',
    35: 'Aboda Village',
    36: 'Aboda Village Indoors',
    37: 'Hyrule Castle Town',
    38: 'Hyrule Castle Town Indoors',
    39: 'Hyrule Castle',
    40: 'Hyrule Castle (Duplicate)',
    41: 'Empty Hyrule Castle',
    42: 'Whittleton',
    43: 'Whittleton Indoors',
    44: 'Anouki Village',
    45: 'Anouki Village Indoors',
    46: 'Anouki Village (Duplicate)',
    47: 'Anouki Village Indoors (Duplicate)',
    48: 'Papuchia Village',
    49: 'Papuchia Village Indoors',
    50: 'Happy Goron Village',
    51: 'Happy Goron Village (Duplicate)',
    52: 'Goron Village',
    53: 'Goron Village (Duplicate)',
    54: 'Phantom Hourglass Titlescreen / Great Sea (Duplicate 2)',
    55: 'Beedle\'s Airshop',
    56: 'Fortune Teller',
    57: 'Linebeck Intro',
    58: 'Linebeck\'s Theme',
    59: 'Lokomo Sanctuary',
    60: 'Silence?',
    61: 'Tower of Spirits Lobby',
    62: 'Cave',
    63: 'Cave (Duplicate)',
    64: 'Tower of Spirits ',
    65: 'Tower of Spirits Staircase',
    66: 'Dungeon',
    67: 'Dungeon (Duplicate)',
    68: 'Dungeon (Duplicate 2)',
    69: 'Dungeon (Duplicate 3)',
    70: 'Fire/Desert Dungeon',
    71: 'Fire/Desert Dungeon (Duplicate)',
    72: 'Cave (Duplicate 2)',
    73: 'Cave (Duplicate 3)',
    74: 'Phantom Hourglass Dungeon',
    75: 'Phantom has spawned!',
    76: 'Phantom chase',
    77: 'Phantom chase (alternate)',
    78: 'Enemy encounter (Duplicate)',
    79: 'Miniboss',
    80: 'Rocktite Chase (Fire)',
    81: 'Stagnox Intro',
    82: 'Stagnox',
    83: 'Fraaz Intro',
    84: 'Fraaz',
    85: 'Phytops Intro',
    86: 'Phytops',
    87: 'Cragma Intro',
    88: 'Cragma',
    89: 'Skeldritch Intro',
    90: 'Skeldritch',
    91: 'Byrne Battle (Not duplicate)',
    92: 'Malladus',
    93: 'Dark Train Battle',
    94: 'Phantom Hourglass Boss Battle',
    95: 'Chancellor Cole Battle',
    96: 'Malladus Battle 2',
    97: 'Malladus Battle 2 (Duplicate)',
    98: 'Rocktite Chase (Snow)',
    99: 'Dark Link',
    100: 'Got an important item!',
    101: 'Got an item!',
    102: 'Learned a song!',
    103: 'Got a heart container!',
    104: 'Got a Realm Railmap!',
    105: 'Got a train car!',
    106: 'Played a Lokomo Duet!',
    107: 'Beat a boss!',
    108: 'Got a Gem! [Unused? Phantom Hourglass]',
    109: 'Failed a minigame',
    110: 'Struck by phantom!',
    111: 'Game Over!',
    112: 'Silence?',
    113: 'Silence?',
    114: 'Silence?',
    115: 'Silence?',
    116: 'Silence?',
    117: 'Silence?',
    118: 'Gage\'s Song Part 1',
    119: 'Steem\'s Song Part 1',
    120: 'Carben\'s Song Part 1',
    121: 'Embrose\'s Song Part 1',
    122: 'Rael\'s Song Part 1',
    123: 'Gage\'s Song Part 1 (Duplicate)',
    124: 'Gage\'s Song Part 2',
    125: 'Steem\'s Song Part 2',
    126: 'Carben\'s Song Part 2',
    127: 'Embrose\'s Song Part 2',
    128: 'Rael\'s Song Part 2',
    129: 'Gage\'s Song Part 2 (Duplicate)',
    130: 'Zelda\'s Song Part 1',
    131: 'Hint',
    132: 'Hint (Duplicate)',
    133: 'Song of Awakening Stone Notes',
    134: 'Song of Healing Stone Notes',
    135: 'Song of Birds Stone Notes',
    136: 'Song of Light Stone Notes',
    137: 'Song of Discovery Stone Notes',
    138: 'Song of Awakening Flute Notes',
    139: 'Song of Healing Flute Notes',
    140: 'Song of Birds Flute Notes',
    141: 'Song of Light Flute Notes',
    142: 'Song of Discovery Flute Notes ',
    143: 'Song of Awakening Played The First Time',
    144: 'Song of Awakening',
    145: 'Song of Healing Played The First Time',
    146: 'Song of Healing',
    147: 'Song of Birds Played The First Time',
    148: 'Song of Birds',
    149: 'Song of Light Played The First Time',
    150: 'Song of Light',
    151: 'Song of Discovery Played The First Time',
    152: 'Song of Discovery',
    153: 'Tag Mode',
    160: 'Title Screen',
    161: 'Silence',
    163: 'Intro Cutscene',
    164: 'Aboda Village (Cutscene?)',
    167: 'Silence',
    167: 'Got an important item!',
    168: 'Engineer Ceremony',
    172: 'Train is derailing!',
    173: 'Tower of Spirits is breaking up!',
    178: 'Malladus is a Train!',
    181: 'Chancellor Cole is evil!',
    182: 'Chancellor Cole is unhinged!',
    183: 'Chancellor Cole is super unhiged!',
    184: 'Chancellor Cole is REALLY unhinged!',
    185: 'Byrne vs Alfonzo',
    186: 'Silence',
    187: 'Zelda is dead!',
    188: 'The evildoers walk away...',
    190: 'Tower of Spirits is Spinning',
    193: 'Anjean, the Tower of Spirits Keeper',
    194: 'Zelda is unhinged!',
    195: 'Silence',
    198: 'Silence',
    203: 'Cleared Forest Temple!',
    206: 'Tracks are being restored!',
    209: 'Tracks from Forest Temple are restored!',
    212: 'Cleared Snow Temple!',
    215: 'Tracks are being restored!',
    218: 'Tracks from Snow Temple are restored!',
    221: 'Cleared Water Temple!',
    224: 'Tracks are being restored!',
    227: 'Tracks from Water Temple are restored!',
    230: 'Talking to Byrne',
    231: 'Anjean will handle this!',
    233: 'Silence',
    236: 'Cleared Fire Temple!',
    239: 'Tracks are being restored!',
    242: 'Tracks from Fire Temple are restored!',
    248: 'Silence',
    235: 'Talking to Byrne',
    251: 'Desert cutscene',
    255: 'Chancellor Cole is Evil!',
    256: 'Entering Dark Realm!',
    258: 'Tower of Spirits Lobby w/Echoes',
    261: 'Silence',
    262: 'Byrne is Defeated',
    263: 'Silence',
    266: 'Silence',
    267: 'Silence',
    270: 'Chancellor Cole Succeeds!',
    271: 'Resurrection, commence!',
    272: 'Malladus is back!',
    275: 'Malladus Cutscene 1',
    276: 'Malladus Cutscene 2',
    277: 'Malladus Cutscene 3',
    278: 'Malladus Cutscene 4',
    279: 'Malladus Cutscene 5',
    280: 'Malladus Cutscene 6',
    281: 'Malladus Cutscene 7',
    282: 'Malladus Cutscene 8',
    284: 'Silence',
    289: 'Ending',
    294: 'Ending 2',
    297: 'Ending 2 (Duplicate)',
    300: 'Endine 2 (Duplicate)',
    303: 'Silence',
    304: 'Got an item!',
    307: 'Bells',
    308: 'File Saved',
    309: 'File Saved (Duplicate)',
    310: 'Failed to save',
    311: 'Failed to save (Duplicate)',
    312: 'Ghost Zelda appears',
    313: 'Ghost Zelda hides',
    314: 'Ghost Zelda freaks out!',
    315: 'Target Hit',
    316: 'Target Hit 2',
    317: 'Target Hit 3',
    318: 'Target Hit 4',
    319: 'Goron Target Hit',
    320: 'Telling Fortune',
    321: '?',
    322: '?',
    323: '?',
    324: 'Silence?',
    351: 'Adventurous Theme',
    352: 'Battle Menu',
    353: 'Phantom Chase Weird',
    354: 'Twilight Princess Boss Combo!',
    355: 'Victory Jingle?',
    356: 'Got a Gem!',
    357: 'Lost',
    358: 'Twilight Princess Boss Combo!',
    359: 'Phantom Appears Weird',
    360: 'Momentous Jingle',
    361: 'Jingly Jingle',
    362: 'Whimsical Jingle',
    }

def main():
    with open(SDAT_PATH, 'rb') as f:
        sdatData = f.read()
    sdat = ndspy.soundArchive.SDAT(sdatData)

    for i, (n, seq) in enumerate(sdat.sequences):
        if seq is None: continue
        s = f'SSEQ_%04d ({names.get(i, "?")}) ' % i
        if len(s) % 2: s += ' '
        while len(s) < 70: s += '. '
        print(s + f'-> bank {seq.bankID}')
    return

    musicSwar = sdat.waveArchives[0][1]

    def notesUsedBy(instrument):
        if isinstance(instrument, ndspy.soundBank.SingleNoteInstrument):
            yield instrument.noteDefinition
        elif isinstance(instrument, ndspy.soundBank.RangeInstrument):
            assert instrument.noteDefinitions
            yield from instrument.noteDefinitions
        elif isinstance(instrument, ndspy.soundBank.RegionalInstrument):
            assert instrument.regions
            for endpoint, note in instrument.regions:
                yield note
    def swavsUsedBy(instrument):
        for note in notesUsedBy(instrument):
            yield note.swavID

    allInstruments = []
    for bID, (bName, b) in enumerate(sdat.banks):
        # Only SWAR 0 is used for music. (1 is SFX and 2 is cutscenes)
        if 0 in b.waveArchives:
            allInstruments.extend(b.instruments)
            for i, inst in enumerate(b.instruments):
                if inst is not None:
                    inst._bankID = bID
                    inst._instID = i

    # [{note, note, note}, ...]: all notes used by each instrument in order
    # [{swav, swav, swav}, ...]: all SWAVs used by each instrument in order
    allInstrumentsByNotesUsed = []
    allInstrumentsBySwavsUsed = []
    for inst in allInstruments:
        thing1 = list(notesUsedBy(inst))
        thing2 = set(swavsUsedBy(inst))
        allInstrumentsByNotesUsed.append(([inst], thing1))
        allInstrumentsBySwavsUsed.append(thing2)


    # temp = []
    # temp.append('[')
    # for swavID in range(9999):
    #     temp.append('[')
    #     for inst, swavsUsed in zip(allInstruments, allInstrumentsBySwavsUsed):
    #         if swavID in swavsUsed:
    #             temp.append(f'({inst._bankID},{inst._instID}),')
    #     temp.append('],')
    # temp.append(']')
    # print(''.join(temp))
    # return


    mergedInstruments = [(q, list(x)) for q, x in allInstrumentsByNotesUsed]

    # Quick first pass: remove blank instruments
    mergedInstruments = [(q, x) for q, x in mergedInstruments if x]

    # Pass 1.1?: look for identical instruments
    i = 0
    while i < len(mergedInstruments):
        j = i + 1
        while j < len(mergedInstruments):
            incrementJ = True

            assert j > i

            # See if we can combine instruments i and j
            instI = mergedInstruments[i][0][0]
            instJ = mergedInstruments[j][0][0]
            instINotes = mergedInstruments[i][1]
            instJNotes = mergedInstruments[j][1]

            combinable = isinstance(instI, type(instJ)) and len(instINotes) == len(instJNotes)
            for note1 in instINotes:
                for note2 in instJNotes:
                    if note1.swavID != note2.swavID:
                        combinable = False

            if combinable == True:
                mergedInstruments[i][0].append(instJ)
                del mergedInstruments[j]
                incrementJ = False

            if incrementJ:
                j += 1

        i += 1

    # print(len(mergedInstruments))
    # print(mergedInstruments)

    instrumentsBySwav = [[(52,0)],[(131,10),(131,11),(131,28),(131,32),(132,10),(132,11),(132,28),(132,32),(133,10),(133,11),(133,28),(133,32),(134,10),(134,11),(134,28),(134,32)],[(131,7),(131,18),(131,26),(131,30),(132,7),(132,18),(132,26),(132,30),(133,7),(133,18),(133,26),(133,30),(134,7),(134,18),(134,26),(134,30)],[(0,0),(20,1)],[(20,1),(29,6),(96,3)],[(20,1),(29,6),(96,3)],[(20,1),(29,6)],[(116,5)],[(70,9)],[(70,9)],[(20,2)],[(20,2)],[(20,2)],[(129,0)],[(131,10),(132,10),(133,10),(134,10)],[(70,6)],[(70,6)],[(56,2),(57,2)],[(29,4),(53,18),(69,7)],[(53,18)],[(53,18)],[(54,0),(56,3),(58,3),(60,3),(62,3),(64,3)],[(51,8)],[(60,5),(61,5)],[(60,5),(61,5)],[(10,1)],[(10,1)],[(10,1)],[(18,0)],[(18,0)],[(18,0)],[(18,0)],[(18,0)],[(11,1)],[(11,1)],[(11,1)],[(11,1)],[(49,2)],[(49,2)],[(49,2)],[(94,4),(104,2)],[(94,4)],[(95,7),(111,4)],[(95,7),(96,7)],[(94,2)],[(29,1),(94,2)],[(94,2)],[(124,2),(125,2)],[(94,0)],[(94,0)],[(43,6),(44,6),(131,12),(132,12),(133,12),(134,12)],[(103,6)],[(24,3)],[(121,1)],[(31,2),(86,5)],[(31,2),(91,3)],[(31,2),(91,3)],[(31,2),(86,5)],[(9,1)],[(31,2),(91,3)],[(24,6),(69,6)],[(8,1),(24,6),(62,1),(63,1),(131,35),(132,35),(133,35),(134,35)],[(2,2),(10,2),(30,3),(121,5),(131,17),(132,17),(133,17),(134,17)],[(2,2),(10,2),(30,3),(121,5)],[(2,2),(10,2),(30,3),(121,5)],[(30,3)],[(30,3)],[(110,0)],[(110,0)],[(110,0)],[(110,0)],[(110,0)],[(19,4),(23,3),(60,2),(61,2),(121,4)],[(19,4),(23,3)],[(19,4),(66,3),(68,3),(69,3),(70,3),(71,3)],[(77,5)],[(84,2),(103,4)],[(16,7),(28,0),(29,0),(53,17),(84,2)],[(16,7),(28,0),(29,0),(32,6),(53,17),(122,0)],[(53,17)],[(41,3)],[(41,3)],[(14,4),(48,1),(50,0),(87,0),(100,0)],[(50,0),(69,8),(87,0),(100,0)],[(50,0),(69,8),(87,0),(100,0)],[(50,0),(69,8),(87,0),(100,0)],[(103,4)],[(51,0)],[(26,3)],[(121,2)],[(12,7),(50,4),(53,14),(69,2),(70,10),(87,4)],[(29,5),(51,3),(51,9),(103,2),(105,6),(131,5),(131,19),(132,5),(132,19),(133,5),(133,19),(134,5),(134,19)],[(123,0),(129,1)],[(8,0),(9,0)],[(8,0),(9,0)],[(8,0)],[(76,2),(94,6),(112,2)],[(60,4),(61,4),(76,2),(112,2),(126,1)],[(76,2),(94,6),(112,2)],[(76,2),(94,6),(112,2)],[(78,5)],[(78,5)],[(115,3)],[(115,3)],[(115,0)],[(115,1),(116,7)],[(1,0),(45,1)],[(1,2),(11,5),(13,2),(40,6),(46,7),(48,4),(53,10),(70,4),(73,10),(128,2)],[(117,4)],[(15,0),(16,0),(17,0),(32,5),(38,5),(78,0)],[(45,4)],[(45,4)],[(45,4)],[(37,3),(40,0),(120,3)],[(117,2)],[(117,2)],[(117,2)],[(117,2)],[(117,2)],[(117,3)],[(78,1)],[(118,7)],[(118,7)],[(117,6)],[(118,5)],[(27,0)],[(117,5)],[(80,0),(131,22),(132,22),(133,22),(134,22)],[(78,3)],[(78,3)],[(80,2)],[(118,0)],[(80,1),(131,23),(132,23),(133,23),(134,23)],[(34,0),(35,3),(45,0)],[(115,2)],[(117,0)],[(1,1),(15,1),(35,2),(45,3),(118,10),(128,1)],[(1,1),(15,1),(45,3),(118,10),(128,1)],[(13,3),(35,4),(37,0),(40,2)],[(37,0)],[(15,3),(27,1),(45,5)],[(15,3),(45,5)],[(15,3),(45,5)],[(78,2),(117,1)],[(34,2),(35,1),(37,5),(104,8),(107,10),(120,5)],[(45,2),(79,2),(80,3),(118,1),(131,21),(131,24),(131,25),(132,21),(132,24),(132,25),(133,21),(133,24),(133,25),(134,21),(134,24),(134,25)],[(2,0),(33,2),(62,4),(63,4),(66,4)],[(2,0),(33,2),(62,4),(63,4),(66,4),(131,4),(131,16),(132,4),(132,16),(133,4),(133,16),(134,4),(134,16)],[(2,0),(66,4)],[(37,1)],[(40,1)],[(37,2),(118,2)],[(16,6),(17,6),(36,2),(38,10),(40,4),(79,3)],[(1,5),(39,0),(40,3),(47,6),(48,6),(78,6),(128,5)],[(1,5),(13,5),(37,6),(39,0),(47,6),(48,6),(78,6),(120,6),(128,5)],[(1,6),(13,6)],[(1,6)],[(1,3)],[(1,3),(118,3)],[(1,3)],[(1,3),(36,1),(38,8)],[(1,3),(118,3)],[(1,4),(13,4),(14,2),(79,0),(128,4),(131,20),(131,29),(132,20),(132,29),(133,20),(133,29),(134,20),(134,29)],[(1,4),(14,2)],[(118,4)],[(15,2),(78,4),(118,4)],[(21,0)],[(26,4)],[(26,4)],[(18,3),(104,3)],[(26,5),(130,0)],[(23,5)],[(23,5)],[(3,6),(19,7),(88,4),(90,4),(102,4)],[(25,5)],[(25,5),(74,0)],[(25,5),(74,0)],[(25,5)],[(41,2),(111,6)],[(41,2)],[(41,2),(82,5)],[(41,2),(52,6),(111,6)],[(76,3),(112,3)],[(21,0)],[(76,3),(112,3)],[(47,7),(97,1)],[(121,6)],[(2,1),(68,7),(83,3)],[(52,6),(86,1),(91,1)],[(3,6)],[(25,5)],[(46,6)],[(103,1),(131,1),(131,34),(132,1),(132,34),(133,1),(133,34),(134,1),(134,34)],[(26,2),(127,0)],[(26,2)],[(127,0)],[(105,4),(107,4)],[(5,8),(6,8),(7,8),(13,0),(14,8),(16,1),(17,1),(32,4),(34,1),(35,0),(37,4),(38,7),(39,2),(40,5),(43,0),(44,0),(50,2),(53,21),(79,1),(87,2),(113,3),(118,11),(122,7),(128,0)],[(3,7),(88,4)],[(46,1),(47,8),(48,8),(83,2),(84,3),(90,4),(93,1),(99,2),(102,4)],[(49,5),(70,7),(109,11)],[(42,0),(58,2),(59,2)],[(42,0),(58,2),(59,2),(82,5)],[(7,8),(28,6),(49,3),(83,3),(99,5),(109,5),(113,0)],[(5,8)],[(5,8),(7,8),(46,0),(109,5),(113,0)],[(5,8),(7,8),(46,0),(113,0)],[(84,3),(91,4),(102,1),(102,3),(108,11)],[(26,6),(83,3)],[(26,6)],[(11,2)],[(89,0),(102,1),(102,3),(126,2)],[(89,0)],[(26,1)],[(31,2),(91,3)],[(76,3),(112,3)],[(56,6),(57,6),(109,0)],[(77,3),(116,1)],[(20,5),(21,5)],[(68,7)],[(106,4)],[(114,5)],[(111,6),(114,5)],[(96,4)],[(76,3),(77,7),(84,3),(112,3)],[(2,1)],[(49,3),(82,5),(109,5)],[(49,3),(109,5)],[(52,6),(104,3)],[(42,1)],[(49,4),(109,5)],[(26,0)],[(26,1)],[(3,5)],[(2,1),(22,1),(30,1),(68,7)],[(121,6)],[(131,34),(132,34),(133,34),(134,34)],[(114,5)],[(17,10),(29,2),(30,2),(53,20),(64,1),(65,1),(109,12),(131,2),(131,31),(132,2),(132,31),(133,2),(133,31),(134,2),(134,31)],[(17,10),(29,2),(30,2),(53,20),(64,1),(65,1),(109,12)],[(20,6),(39,1),(70,1),(76,6),(77,2),(112,6)],[(39,1),(70,1),(76,6),(77,2),(112,6)],[(105,4)],[(38,5),(131,2),(131,31),(131,34),(132,2),(132,31),(132,34),(133,2),(133,31),(133,34),(134,2),(134,31),(134,34)],[(41,2),(98,3)],[(56,1),(57,1)],[(52,6),(103,1)],[(127,3)],[(131,1),(132,1),(133,1),(134,1)],[(131,1),(132,1),(133,1),(134,1)],[(31,7)],[(31,7)],[(31,7)],[(31,7)],[(41,2)],[(31,7)],[(10,4),(98,2)],[(10,4),(98,2),(121,6)],[(121,6)],[(2,1),(10,4),(98,2),(121,6)],[(46,0)],[(99,5)],[(4,1),(5,1),(7,1),(19,0),(48,9),(60,1),(61,1),(82,0)],[(4,1),(5,1),(7,1),(19,0),(60,1),(61,1),(82,0)],[(18,3),(131,1),(132,1),(133,1),(134,1)],[(13,7),(16,2),(28,4),(32,8),(71,4)],[(13,7),(16,2),(28,4),(32,8),(71,4)],[(13,7),(71,4)],[(16,2),(28,4),(32,8)],[(13,7),(71,4)],[(16,2),(28,4),(32,8),(56,1),(57,1)],[(24,5)],[(25,4),(116,8)],[(103,3),(131,3),(132,3),(133,3),(134,3)],[(43,2),(44,2),(77,7),(84,3),(91,4),(102,5)],[(43,2),(44,2)],[(51,1),(103,9)],[(77,7)],[(31,6),(121,6)],[(31,6)],[(116,2),(126,2)],[(11,4)],[(23,5)],[(23,5)],[(68,6),(73,8)],[(68,6)],[(53,8),(68,6),(73,8)],[(3,2),(42,4),(85,5)],[(3,2),(42,4),(85,5)],[(9,4)],[(8,4)],[(28,5),(38,4),(46,2),(53,15),(82,8),(107,12),(108,12),(122,4)],[(28,5),(38,4),(46,2),(53,15),(82,8)],[(3,1),(109,1)],[(3,1),(5,13),(6,13),(52,5),(66,1),(67,1),(73,7),(82,11),(85,2),(109,1),(113,1),(114,4)],[(5,13)],[(3,1),(5,13),(52,5),(53,7),(66,1),(67,1),(73,7),(82,11),(85,2),(109,1),(113,1)],[(3,1),(5,13),(66,1),(67,1),(73,7),(82,11),(85,2),(109,1)],[(52,5)],[(41,0)],[(41,0)],[(8,3),(9,3)],[(8,2),(9,2)],[(17,12),(30,4),(30,5)],[(10,0),(17,12),(30,4),(30,5)],[(10,0),(17,12),(30,4),(30,5)],[(17,12),(30,4),(30,5)],[(10,0),(17,12),(30,4),(30,5)],[(10,0),(17,12),(30,4),(30,5)],[(97,3),(101,3),(104,6)],[(49,0),(82,10),(97,3),(101,3),(106,0)],[(49,0),(97,3),(101,3)],[(49,0),(82,10),(97,3),(101,3),(106,0)],[(49,0),(82,10),(97,3),(101,3),(104,6)],[(49,0),(97,3),(101,3),(106,0)],[(18,2),(21,3)],[(4,12),(5,9),(5,10),(5,12)],[(4,12),(5,9),(5,10),(5,12)],[(33,1),(85,4)],[(33,1),(58,1),(59,1),(85,4)],[(23,1)],[(23,1)],[(23,1)],[(23,1)],[(74,3)],[(74,3)],[(74,3)],[(74,3)],[(74,3)],[(2,0)],[(25,2)],[(25,2)],[(25,2)],[(25,2),(114,2),(120,3)],[(25,2)],[(96,9)],[(96,9)],[(42,3),(71,6),(109,16)],[(42,3),(71,6),(109,16)],[(88,3)],[(52,3)],[(52,3),(104,1)],[(96,6),(105,2),(106,2),(107,2),(108,2),(114,1)],[(104,1),(105,2),(106,2),(107,2),(108,2),(111,8),(114,1)],[(104,1),(105,2),(106,2),(107,2),(108,2)],[(96,8),(104,1)],[(96,8)],[(23,2)],[(23,2)],[(23,2)],[(94,1)],[(11,0),(12,6)],[(12,6),(90,8),(94,1)],[(11,0),(12,6),(90,8),(94,1)],[(11,0)],[(19,6)],[(19,6)],[(30,0)],[(30,0)],[(19,8),(109,8)],[(22,4),(68,8),(76,0),(109,8),(112,0)],[(68,8),(76,0),(109,8),(112,0)],[(22,4)],[(19,8)],[(6,14),(68,8),(109,8)],[(74,1),(75,1),(92,1)],[(74,1),(75,1),(92,1)],[(74,1),(75,1),(92,1)],[(74,1)],[(52,2),(88,0)],[(52,2),(88,0)],[(88,0)],[(90,0)],[(83,0),(90,0),(91,0)],[(83,0),(90,0)],[(83,0),(86,0),(91,0)],[(83,0),(91,0)],[(52,2)],[(52,2),(88,0)],[(2,3),(3,0),(5,11),(131,13),(132,13),(133,13),(134,13)],[(2,3),(3,0),(5,11),(126,3)],[(5,11)],[(47,0),(48,0),(99,0)],[(47,0),(48,0),(99,0)],[(31,8)],[(31,8)],[(31,5)],[(31,5)],[(31,5)],[(76,5),(112,5),(114,1)],[(76,5),(112,5)],[(41,1),(91,2)],[(41,1),(86,2),(91,2)],[(103,8),(131,14),(132,14),(133,14),(134,14)],[(86,8),(104,9),(107,3),(108,3)],[(86,8),(104,9),(107,3),(108,3)],[(88,3)],[(20,3),(22,3),(86,3)],[(22,3),(86,3)],[(20,3)],[(20,3)],[(88,3)],[(88,3)],[(22,3),(86,3)],[(96,0)],[(96,0)],[(110,1)],[(110,1),(120,9)],[(31,3),(51,7),(116,3)],[(116,3)],[(4,3),(5,3),(6,3),(7,3),(16,3),(32,7),(33,0),(43,3),(44,3),(46,5),(47,2),(48,2),(50,1),(53,19),(66,2),(68,2),(70,2),(71,2),(73,4),(82,1),(85,0),(87,1),(100,1),(109,7),(113,6),(128,3),(131,9),(131,15),(131,27),(131,33),(132,9),(132,15),(132,27),(132,33),(133,9),(133,15),(133,27),(133,33),(134,9),(134,15),(134,27),(134,33)],[(5,3),(6,3),(33,0),(39,3),(43,3),(46,5),(47,2),(48,2),(53,19),(66,2),(70,2),(82,1),(109,7),(128,3)],[(109,7),(128,3)],[(16,3),(32,7),(82,1),(109,7),(122,9),(128,3)],[(4,3),(5,3),(6,3),(7,3),(16,3),(32,7),(33,0),(39,3),(43,3),(44,3),(46,5),(47,2),(48,2),(50,1),(53,19),(66,2),(68,2),(70,2),(71,2),(73,4),(82,1),(85,0),(87,1),(100,1),(109,7),(128,3),(131,9),(131,15),(131,27),(131,33),(132,9),(132,15),(132,27),(132,33),(133,9),(133,15),(133,27),(133,33),(134,9),(134,15),(134,27),(134,33)],[(4,7),(5,7),(7,7),(82,3),(109,14)],[(4,7),(5,7),(7,7),(82,3),(109,14)],[(42,2),(46,9),(47,5),(48,5),(56,4),(57,4),(93,0),(98,1)],[(5,9),(6,9),(7,9),(12,1),(16,4),(17,3),(28,1),(39,5),(46,8),(47,3),(53,13),(71,7),(82,12),(98,0),(99,1),(109,3)],[(12,1),(28,1),(32,9),(53,13),(109,3)],[(5,9),(6,9),(39,5),(46,8),(47,3),(71,7),(82,12),(98,0),(99,1),(109,3)],[(5,9),(7,9),(12,1),(28,1),(32,9),(39,5),(46,8),(47,3),(53,13),(71,7),(82,12),(98,0),(99,1),(109,3)],[(3,4)],[(3,4)],[(42,2),(86,2)],[(42,2)],[(23,0)],[(23,0)],[(25,3),(86,10)],[(25,3),(86,10)],[(25,3)],[(25,3)],[(25,3),(86,10)],[(91,2)],[(12,3),(42,2),(46,9),(47,5),(48,5),(93,0),(98,1),(113,4)],[(12,3),(42,2),(46,9),(47,5),(48,5),(56,4),(57,4),(93,0),(98,1),(113,4)],[(42,2),(46,9),(98,1)],[(93,0)],[(12,4)],[(12,4)],[(12,4)],[(25,0)],[(25,0)],[(51,14),(103,10)],[(23,4)],[(23,4)],[(103,5)],[(24,0)],[(24,0)],[(2,4),(24,0)],[(22,0)],[(22,0)],[(22,0),(73,5)],[(22,0)],[(124,3),(125,3)],[(14,0),(28,2),(50,3),(62,2),(63,2),(87,3),(87,7),(122,2)],[(96,5)],[(114,3)],[(114,3)],[(14,6),(50,6),(51,11),(130,1)],[(14,6),(50,6)],[(22,20)],[(75,0),(92,0)],[(51,5)],[(75,2),(92,2)],[(51,4)],[(17,14),(30,6),(30,7)],[(50,5),(100,5)],[(91,1),(111,5)],[(88,1),(89,4),(90,6),(102,6),(104,0)],[(51,12),(52,1)],[(51,12),(51,13),(52,1),(103,5)],[(31,1),(51,6),(103,0)],[(31,1)],[(31,4),(116,9)],[(24,1)],[(24,1)],[(24,1)],[(24,1)],[(25,1),(82,13),(99,3)],[(25,1),(86,6),(99,3)],[(25,1),(69,1),(82,13),(99,3),(103,7)],[(116,8)],[(124,0)],[(125,0)],[(53,1),(73,1)],[(73,1)],[(73,1)],[(73,1)],[(73,1)],[(52,4)],[(88,1),(90,2),(102,2)],[(52,4),(88,2),(89,2),(90,2),(102,2),(107,9)],[(52,4)],[(90,2),(102,2)],[(90,2),(102,2)],[(88,2),(89,2),(107,9),(126,0)],[(11,3),(64,2),(65,2),(126,4)],[(24,2)],[(24,2)],[(24,2)],[(24,2)],[(24,2)],[(22,2)],[(76,1),(112,1)],[(76,1),(112,1)],[(76,1),(112,1)],[(76,1),(112,1)],[(12,5),(19,3),(20,4),(85,1)],[(12,5),(19,3),(20,4),(85,1)],[(12,5),(19,3),(20,4),(85,1),(113,2)],[(21,4),(22,2)],[(21,4),(22,2)],[(21,4)],[(21,4),(22,2)],[(19,2),(23,6),(24,4),(43,7),(44,7),(69,4)],[(19,2),(23,6),(24,4),(43,7),(53,9),(69,4),(73,9)],[(19,2),(24,4),(43,7),(44,7),(69,4),(73,9)],[(19,2),(23,6),(24,4),(43,7),(44,7),(69,4),(73,9)],[(26,7)],[(26,7)],[(26,7)],[(26,7)],[(42,5),(72,1),(77,6),(84,0),(99,4),(131,6),(132,6),(133,6),(134,6)],[(42,5),(64,5),(65,5),(72,1),(84,0),(99,4),(131,6),(132,6),(133,6),(134,6)],[(77,6)],[(53,12),(71,1),(73,12)],[(53,12),(71,1),(73,12)],[(76,4),(112,4)],[(76,4),(112,4)],[(76,4),(112,4)],[(76,4),(112,4)],[(5,4),(12,0),(53,2),(53,6),(55,0),(56,0),(56,15),(57,0),(57,15),(58,0),(58,15),(59,0),(59,15),(60,0),(60,15),(61,0),(61,15),(62,0),(62,15),(63,0),(63,15),(64,0),(64,15),(65,0),(65,15),(66,0),(66,5),(68,0),(68,5),(69,0),(69,5),(70,0),(70,5),(71,0),(71,5),(73,2),(73,6),(114,0),(119,0),(163,0)],[(5,4),(53,2),(53,6),(73,2),(73,6),(131,0),(132,0),(133,0),(134,0)],[(114,0),(131,0),(132,0),(133,0),(134,0)],[(83,1),(96,2)],[(33,3),(82,7),(83,1),(96,2),(109,15)],[(83,1)],[(33,3),(82,7),(83,1),(109,15)],[(33,3),(82,7),(83,1),(109,15)],[(97,0),(104,4)],[(97,0),(104,4)],[(51,10),(105,8),(106,8),(110,2)],[(18,1),(36,0),(104,11),(105,8),(106,8)],[(18,1),(36,0),(110,2)],[(110,2)],[(36,0),(110,2)],[(77,4)],[(77,4)],[(77,4)],[(46,4)],[(46,4)],[(77,1)],[(77,1)],[(21,1),(96,1)],[(21,1)],[(21,1),(96,1),(111,1)],[(21,1)],[(3,3),(10,3),(49,1),(85,3),(131,8),(132,8),(133,8),(134,8)],[(3,3),(10,3),(49,1),(51,13),(85,3)],[(109,2)],[(109,2)],[(109,2)],[(109,2)],[(109,2)],[(77,0)],[(121,0)],[(81,11),(130,2)]]

    # Use instrumentsBySwav to make instrument "groups" (lists of
    # instruments with any swavs in common with each other)
    instrumentGroups = []
    for groupedInsts in instrumentsBySwav:
        newGroup = list(groupedInsts)
        _instrumentGroups = [newGroup]
        for g in instrumentGroups:
            if any(x in g for x in groupedInsts):
                newGroup.extend(g)
            else:
                _instrumentGroups.append(g)
        instrumentGroups = _instrumentGroups

        # deduplicate
        instrumentGroups[0] = sorted(set(instrumentGroups[0]))

    for g in instrumentGroups:
        x = []
        for y in g:
            x.append(f'{"%03d" % y[0]}.{"%02d" % y[1]}')
        print(', '.join(x))

    return

    print(instrumentGroups)
    print(len(instrumentGroups))
    print(len(instrumentsBySwav))

    return

    with open('/usr/share/dict/words', 'r', encoding='utf-8') as f:
        w = f.read()
    w = w.split('\n')
    import random
    for insts, _ in mergedInstruments:
        print('__' + random.choice(w).replace("'", '') + ':')
        for inst in insts:
            print(f'    {"%03d" % inst._bankID}.{"%02d" % inst._instID},')
    return

    # Second pass: intelligent merging of instruments
    i = 0
    while i < len(mergedInstruments):
        j = i + 1
        while j < len(mergedInstruments):
            incrementJ = True

            assert j > i

            # See if we can combine instruments i and j
            instI = mergedInstruments[i][1]
            instJ = mergedInstruments[j][1]

            combinable = any(note.swavID == note2.swavID for note in instI for note2 in instJ)

            if combinable:
                # Now try to disprove that the instruments are truly combinable.
                breakout = False
                for note in instI:
                    for note2 in instJ:
                        if note.swavID == note2.swavID:
                            for prop in ['note', 'attack', 'decay', 'sustain', 'release', 'pan']:
                                if getattr(note, prop) != getattr(note2, prop):
                                    combinable = False
                                    breakout = True
                                    break
                        if breakout: break
                    if breakout: break

            if combinable:
                mergedInstruments[i][0].extend(mergedInstruments[j][0])
                mergedInstruments[i][1].extend(mergedInstruments[j][1])
                del mergedInstruments[j]
                incrementJ = False

            if incrementJ:
                j += 1

        i += 1

    squishedInstruments = []
    for squishInstruments, squishNotes in mergedInstruments:
        noteRegions = [] # (low, high, note)
        for inst in squishInstruments:
            if isinstance(inst, ndspy.soundBank.SingleNoteInstrument):
                noteRegions.append((0, 127, inst.noteDefinition))
            elif isinstance(inst, ndspy.soundBank.RegionalInstrument):
                lo = 0
                for hi, note in inst.regions:
                    noteRegions.append((lo, hi, note))
                    lo = hi + 1

        # Iterate over every note value and pick the representative note
        # for each one.
        # We go from 127 to 0, and every time we hit a "high" value for
        # some note, we switch to it. If we hit "high"s for multiple
        # notes simultaneously, we pick the one with the tightest
        # bounding range.
        newInstrumentNotes = []
        for i in range(127, -1, -1):
            bestRepl = None
            bestRange = 129
            for lo, hi, note in noteRegions:
                if hi == i:
                    if hi - lo + 1 < bestRange:
                        bestRepl = note
                        bestRange = hi - lo + 1
            if bestRepl is not None:
                newInstrumentNotes.append(bestRepl)
            else:
                newInstrumentNotes.append(newInstrumentNotes[-1])

        # Reverse, because we went in backwards order.
        newInstrumentNotes.reverse()

        # And now collapse them...
        newRegions = []
        currentStart = 0
        currentNote = newInstrumentNotes[0]
        for i in range(128):
            thisNote = newInstrumentNotes[i]
            if thisNote is not currentNote:
                newRegions.append((currentStart, i - 1, currentNote))
                currentStart = i
                currentNote = thisNote
        newRegions.append((currentStart, 127, currentNote))

        # We're only allowed 8 regions.
        while len(newRegions) > 8:
            # This is so dumb
            smallestPotentialRegion = 9999999
            for i in range(len(newRegions) - 1):
                lo = newRegions[i][0]
                hi = newRegions[i+1][1]
                potentialRegion = hi - lo + 1
                if potentialRegion < smallestPotentialRegion:
                    smallestPotentialRegion = potentialRegion
            for i in range(len(newRegions) - 1):
                lo = newRegions[i][0]
                hi = newRegions[i+1][1]
                potentialRegion = hi - lo + 1
                if potentialRegion == smallestPotentialRegion:
                    # Perform the merge.
                    # Use the note from whichever region is larger.
                    region1 = newRegions[i]
                    region2 = newRegions[i + 1]
                    range1 = region1[1] - region1[0] + 1
                    range2 = region2[1] - region2[0] + 1
                    if range1 > range2:
                        note = region1[2]
                    else:
                        note = region2[2]
                    newRegion = (region1[0], region2[1], note)
                    newRegions[i] = newRegion
                    del newRegions[i + 1]
                    break

        # Finally, set up the appropriate instrument type.
        if len(newRegions) == 1:
            # Use a single-note instrument.
            # Grab the type from the first SingleNoteInstrument we've got,
            # because IDK what it means exactly.
            for inst in squishInstruments:
                if isinstance(inst, ndspy.soundBank.SingleNoteInstrument):
                    type_ = inst.type
            inst = ndspy.soundBank.SingleNoteInstrument(type_, newRegions[0][2])
        else:
            # Make a real regional instrument.
            regions2 = [(end, note) for (start, end, note) in newRegions]
            inst = ndspy.soundBank.RegionalInstrument(regions2)

        squishedInstruments.append(inst)

    # DEBUGGING
    for inst in squishedInstruments:
        print('---')
        if isinstance(inst, ndspy.soundBank.SingleNoteInstrument):
            print(inst.noteDefinition.swavID)
        else:
            ...

    # Finally, put that all into a big SBNK and save it.
    sbnk = ndspy.soundBank.SBNK()
    sbnk.waveArchives = [0]
    sbnk.instruments = squishedInstruments
    d = sbnk.save()[0]
    with open('MasterSBNK.sbnk', 'wb') as f:
        f.write(d)

    return


    notesUsedBySwav = {i: set() for i in range(568)}
    for inst in allInstruments:
        for note in notesUsedBy(inst):
            notesUsedBySwav[note.swavID].add(note.note)
    for i in range(568):
        print(notesUsedBySwav[i])
    print(len(set(allInstruments)))
    return


    mergedInstruments = [] # [{swav, swav, swav}, ...]: the same as above, but overlapping instruments are combined
    for i in range(568):
        theseInstruments = [x for x in allInstrumentsBySwavsUsed if i in x]
        print(i, theseInstruments)

        for inst in mergedInstruments:
            if i in inst:
                for t in theseInstruments:
                    inst |= t
                break
        else:
            newEntry = set()
            for t in theseInstruments:
                newEntry |= t
            mergedInstruments.append(newEntry)


    for swavsUsed in mergedInstruments:
        print('---------- Possible types for this instrument:')
        for swav in swavsUsed:
            for inst, wavsUsed in zip(allInstruments, allInstrumentsBySwavsUsed):
                if swav in wavsUsed:
                    print(inst.__class__.__name__)

    print(mergedInstruments)
    print(len(mergedInstruments))

        #print(b.instruments)

main()