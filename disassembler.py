import os, os.path

import ndspy.bmg
import zeldaScripts


def disassembleInstructionType1(inst, bmg, allBmgs):
    """
    Disassemble an instruction of type 1.
    """
    assert inst & 0xFF == 1

    bmgID = (inst >> 8) & 0xFF
    messageID = (inst >> 16) & 0xFFFF
    gotoIndex = (inst >> 32) & 0xFFFF
    gotoBmg = (inst >> 48) & 0xFF

    if gotoIndex == 0xFFFF: gotoIndex = -1
    if gotoBmg == 0xFF: gotoBmg = -1

    messageBmg = allBmgs[bmgID][1]
    comment = str(messageBmg.messages[messageID]).replace('\n', ' ')
    if len(comment) > 70:
        comment = comment[:70] + '[...]'
    comment = f'"{comment}"'

    if -1 in [gotoBmg, gotoIndex]:
        gotoName = 'END'
    else:
        gotoName = f'B{gotoBmg}_L{gotoIndex}'

    return ('SAY', comment,
        f'msg={bmgID}/{messageID}',
        f'goto={gotoName}')


def disassembleInstructionType2(inst, bmg, allBmgs):
    """
    Disassemble an instruction of type 2.
    """
    assert inst & 0xFF == 2

    labelCount = (inst >> 8) & 0xFF
    whatToCheckFor = (inst >> 16) & 0xFFFF
    parameter = (inst >> 32) & 0xFFFF
    baseLabelNumber = (inst >> 48) & 0xFFFF

    def defaultParser(bmg, allBmgs, param):
        return (f'SWITCH{whatToCheckFor}', None, f'param={param}')

    parserFuncs = {
        1: disassembleInstructionType2_1,
        4: disassembleInstructionType2_4,
        }

    parserFunc = parserFuncs.get(whatToCheckFor, defaultParser)

    formattedCmd = parserFunc(bmg, allBmgs, parameter)

    gotoLabels = []
    for i in range(baseLabelNumber, baseLabelNumber + labelCount):
        gotoBmg, gotoIndex = bmg.labels[i]
        gotoLabels.append(f'B{gotoBmg}_L{gotoIndex}')

    return (*formattedCmd,
            f'goto=[{", ".join(gotoLabels)}]',)


def disassembleInstructionType2_1(bmg, allBmgs, param):
    assert param == 0
    return ('SW_RESP', None)


def disassembleInstructionType2_4(bmg, allBmgs, param):
    index = param >> 5
    bit = param & 0x1F
    return ('SW_FLAG', None, f'index={index}', f'bit={bit}')


things = set()

def disassembleInstructionType3(inst, bmg, allBmgs):
    """
    Disassemble an instruction of type 3.
    """
    assert inst & 0xFF == 3

    unk01 = (inst >> 8) & 0xFF
    labelNumber = (inst >> 16) & 0xFFFF
    unk04 = inst >> 32

    things.add(unk01)

    gotoBmg, gotoIndex = bmg.labels[labelNumber]
    gotoName = f'B{gotoBmg}_L{gotoIndex}'

    return ('DO', None,
        unk01, unk04, f'goto={gotoName}')


def disassembleInstruction(inst, bmg, allBmgs):
    """
    Disassemble a single instruction.
    """

    instID = inst & 0xFF

    parserFunc = {
        1: disassembleInstructionType1,
        2: disassembleInstructionType2,
        3: disassembleInstructionType3,
        }.get(instID)
    if parserFunc is None:
        raise ValueError(f'Unknown command type: {instID}')

    name, comment, *args = parserFunc(inst, bmg, allBmgs)

    line = name + ' '
    while len(line) < 8: line += ' '
    line += ', '.join(str(a) for a in args) + ' '
    if comment:
        while len(line) < 36: line += ' '
        line += '# ' + comment
    return line


def disassembleInstructionRaw(inst, *args):
    # Fake "disassemble instruction"
    temp = []
    for i in range(8):
        temp.append('%02X' % ((inst >> (i * 8)) & 0xFF))
    return ' '.join(temp) 


def analyze(filename, rawData, bmg, allBmgs):
    if b'FLW1' not in rawData:
        print(f'{filename} does not have scripts.')
        return
    bmgID = [a for (a,(b,c)) in allBmgs.items() if c is bmg][0]
    FLW1Offset = rawData.index(b'FLW1')

    # Print the scripts
    idx2ScriptId = {b: a for (a, b) in bmg.scripts.items()}
    lines = []

    # for scriptID, instIdx in bmg.scripts.items():
    #     scriptName = f'SCRIPT_{scriptID >> 16}_{scriptID & 0xFFFF}'
    #     lines.append(f'{scriptName} = {bmgID}_{instIdx}')
    # lines.append('')

    zeldaScripts.disassembleInstructions(bmg.instructions)
    return

    for i, inst in enumerate(bmg.instructions):
        for scriptID, instIdx in bmg.scripts.items():
            if i != instIdx: continue
            lines.append(f'S{scriptID >> 16}_{scriptID & 0xFFFF}:')

        line = f'B{bmgID}_L{i}: '

        # for scriptID, instIdx in bmg.scripts.items():
        #     if i != instIdx: continue
        #     line += f'B{bmgID}_S{scriptID >> 16}_{scriptID & 0xFFFF}: '

        while len(line) < 12:
            line += ' '

        line += disassembleInstruction(inst, bmg, allBmgs)
        #line += '  # ' + filename + ' ' + hex(FLW1Offset + 16 + 8 * i)
        lines.append(line)

    if lines:
        with open('/home/user/zed/Testing/stExportedScripts/' + filename + '.txt', 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))

    # Print the messages
    lines = []
    for i, msg in enumerate(bmg.messages):
        lines.append(f'{i}:')
        lines.append(str(msg))
        lines.append('--------' * 4)
    del lines[-1]
    with open('/home/user/zed/Testing/stExportedMessages/' + filename + '.txt', 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))


def main():
    dir = '/home/user/zed/Testing/st/root/English/Message/'
    dir2 = '/home/user/zed/Testing/stResavedBMGs/'

    BMGs = {}

    for fn in os.listdir(dir):
        fullfn = os.path.join(dir, fn)
        with open(fullfn, 'rb') as f:
            d = f.read()

        bmg = ndspy.bmg.BMG(d)
        BMGs[bmg.id] = (fn, bmg)


    for id, (fn, bmg) in BMGs.items():
        analyze(fn, d, bmg, BMGs)


main()