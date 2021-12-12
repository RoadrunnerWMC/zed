# Quick script to hackily patch a given Get Item ID into a BMG script.


import struct

import ndspy.lz10
import ndspy.narc
import ndspy.rom


GET_ITEM = 101

ROM_IN = 'Testing/Zelda - Spirit Tracks.nds'
ROM_OUT = 'Testing/Zelda - Spirit Tracks - Testing.nds'



def main():

    with open(ROM_IN, 'rb') as f:
        romData = f.read()
    rom = ndspy.rom.NintendoDSRom(romData)

    villageBmgId = rom.filenames['English/Message/village.bmg']
    villageBmg = rom.files[villageBmgId]

    villageBmg = bytearray(villageBmg)

    # Dumb thing for fun
    commandsStart = 0x15E50
    labelsStart = 0x17BB0
    labelBmgsStart = 0x181E0

    cmdIdx = 0x9F

    numCmds = 2#117
    for i in range(numCmds):
        # GET_ITEM = i
        # if GET_ITEM in [21, 22, 23, 24]: GET_ITEM = 17
        GET_ITEM = 62
        cmd = struct.pack('<BBHI', 3, 9, i, GET_ITEM)
        if i == 1:
            cmd = struct.pack('<BBHI', 3, 0, i, 0x2BE)
        villageBmg[commandsStart + cmdIdx * 8:commandsStart + cmdIdx * 8 + 8] = cmd
        nextCmd = cmdIdx + 1 if i != (numCmds - 1) else 0xFFFF
        villageBmg[labelsStart + i * 2 : labelsStart + i * 2 + 2] = struct.pack('<H', nextCmd)
        villageBmg[labelBmgsStart + i] = 0x14
        cmdIdx += 1
    
    # for i in range(117):
    #     thisCmdIdx = lastCmdIdx + 1
    #     labelValue = struct.unpack_from('<H', villageBmg, labelsStart + 2 * lastCmdIdx)
    #     while labelValue == 0xFFFF:
    #         thisCmdIdx += 1
    #         labelValue = struct.unpack_from('<H', villageBmg, labelsStart + 2 * lastCmdIdx)


    # "2" is the first label that's FF/FFFF
    # cmd = struct.pack('<BBHI', 3, 9, 2, GET_ITEM)
    # cmd = struct.pack('<BBHI', 3, 0, 2, 0x2BE)
    # villageBmg[0x16348:0x16350] = cmd

    rom.files[villageBmgId] = villageBmg

    romDataOut = rom.save()
    with open(ROM_OUT, 'wb') as f:
        f.write(romDataOut)


if __name__ == '__main__':
    main()
