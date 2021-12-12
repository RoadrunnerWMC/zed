import os, os.path
import sys

import ndspy.bmg, ndspy.rom


class ScriptRunner:
    def __init__(self, bmgs):
        self.bmgs = bmgs


    def runScript(self, scriptID):
        """
        Run the specified script.
        """

        for bId, b in self.bmgs.items():
            if scriptID in b.scripts:
                self.nextBmgID = bId
                self.nextInstructionIdx = b.scripts[scriptID]
                break
        else:
            print("Sorry, but there's no script with that ID. :/")
            return

        while (self.nextBmgID not in (0xFF, -1)
                and self.nextInstructionIdx not in (0xFFFF, -1)):
            self.runInstruction()
        print('(End of script.)\n')


    def runInstruction(self):
        """
        Interpret the next instruction.
        """
        bmg = self.bmgs[self.nextBmgID]
        instruction = bmg.instructions[self.nextInstructionIdx]

        instructionType = instruction & 0xFF
        if instructionType == 1:
            self.runInstructionType1(instruction)
        elif instructionType == 2:
            self.runInstructionType2(instruction)
        elif instructionType == 3:
            self.runInstructionType3(instruction)
        else:
            raise RuntimeError(f'Found an instruction with type {instructionType}...?')


    def runInstructionType1(self, instruction):
        """
        Interpret an instruction of type 1.
        """
        bmgID = (instruction >> 8) & 0xFF
        messageID = (instruction >> 16) & 0xFFFF
        nextInstIdx = (instruction >> 32) & 0xFFFF
        nextBmgID = (instruction >> 48) & 0xFF

        message = self.bmgs[bmgID].messages[messageID]
        partsToPrint = []
        response1 = []
        response2 = []
        response3 = []
        response4 = []
        currentlyPrintingTo = partsToPrint
        for i, part in enumerate(message.stringParts):
            if isinstance(part, str):
                currentlyPrintingTo.append(part)
            elif part.type == 0:
                if part.data == b'\0\0':
                    currentlyPrintingTo = response1
                elif part.data == b'\1\0':
                    currentlyPrintingTo = response2
                elif part.data == b'\2\0':
                    currentlyPrintingTo = response3
                elif part.data == b'\3\0':
                    currentlyPrintingTo = response4
            else:
                currentlyPrintingTo.append(str(part))

        stringMessage = "".join(partsToPrint).rstrip()
        print(f'\033[3m"{stringMessage}"\033[0m')
        self.response1 = ''.join(response1)
        self.response2 = ''.join(response2)
        self.response3 = ''.join(response3)
        self.response4 = ''.join(response4)

        self.nextBmgID = nextBmgID
        self.nextInstructionIdx = nextInstIdx


    def runInstructionType2(self, instruction):
        """
        Interpret an instruction of type 2.
        """
        labelsCount = (instruction >> 8) & 0xFF
        whatToCheckFor = (instruction >> 16) & 0xFFFF
        parameter = (instruction >> 32) & 0xFFFF
        baseLabelNumber = (instruction >> 48) & 0xFFFF

        n = self.checkCondition(whatToCheckFor, parameter)
        while n >= labelsCount:
            print(f"Can't branch to label +{n} -- only +0 through +{labelsCount-1} are allowed...")
            n = self.checkCondition(whatToCheckFor, parameter)

        self.nextBmgID, self.nextInstructionIdx = self.bmgs[self.nextBmgID].labels[baseLabelNumber + n]


    def runInstructionType3(self, instruction):
        """
        Interpret an instruction of type 3.
        """

        labelNumber = (instruction >> 16) & 0xFFFF

        print('ANIMATION')

        self.nextBmgID, self.nextInstructionIdx = self.bmgs[self.nextBmgID].labels[labelNumber]


    def checkCondition(self, type, parameter):
        """
        Check a condition.
        """

        def process(x): return int(x)

        if type in [1, 2, 3]: # Response to a question
            responses = [self.response1,
                         self.response2,
                         self.response3,
                         self.response4][:type + 1]
            shortcuts = [''] * len(responses)
            chars = 0
            while len(set(shortcuts)) < len(shortcuts):
                chars += 1
                shortcuts = [r[:chars].lower() for r in responses]
            prompt = ' '.join(f'[{s}: {r}]' for s, r in zip(shortcuts, responses))

            def process(x):
                if x.lower() in shortcuts:
                    return shortcuts.index(x)
                else:
                    raise ValueError

        elif type == 4: # Checking a flag?
            index = parameter >> 5
            bit = parameter & 0x1F
            prompt = f'Is bit {bit} of global value {index} set? (Y/N): '
            def process(x):
                if x.lower() == 'y':
                    return 0
                elif x.lower() == 'n':
                    return 1
                else:
                    raise ValueError

        else: # Undocumented
            prompt = f'Enter the result of check_{type}({parameter}): '

        while True:
            try:
                return process(input(prompt))
            except ValueError:
                prompt = 'wat '



def getScriptID():
    """
    Get a script ID as input from the user. Return None if the input is
    blank or otherwise invalid.
    """
    raw = input('Enter a script category and ID (like "104, 9"): ')
    if ',' not in raw:
        return None
    rawspl = raw.split(',')
    a, b = int(rawspl[0]), int(rawspl[1])
    return a << 16 | b


def main():
    if len(sys.argv) > 1:
        inpath = sys.argv[1]
    else:
        inpath = 'Testing/Zelda - Spirit Tracks.nds'

    BMGs = {}

    if os.path.isfile(inpath):
        with open(inpath, 'rb') as f:
            romData = f.read()
        rom = ndspy.rom.NintendoDSRom(romData)

        datasList = []
        for filename in rom.filenames['English/Message'].files:
            datasList.append(rom.files[rom.filenames['English/Message/' + filename]])

        for d in datasList:
            bmg = ndspy.bmg.BMG(d)
            BMGs[bmg.id] = bmg

    else:
        for fn in os.listdir(inpath):
            fullfn = os.path.join(inpath, fn)
            with open(fullfn, 'rb') as f:
                d = f.read()
            bmg = ndspy.bmg.BMG(d)
            BMGs[bmg.id] = bmg

    assert len(BMGs) == 30

    runner = ScriptRunner(BMGs)

    scriptID = getScriptID()
    while scriptID is not None:
        runner.runScript(scriptID)
        scriptID = getScriptID()

    print('Closing.')


if __name__ == '__main__': main()