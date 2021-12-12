# Library for Zelda scripts



def _makeSigned(value, bitCount):
    """
    Take an unsigned variable value and make it signed.
    """
    if value < 0: return value
    if value & (1 << (bitCount - 1)):
        value -= 1 << bitCount
    return value


class Label:
    """
    Convenience class to represent a label.
    """
    bmg = 0
    index = 0
    def __init__(self, bmg, index):
        self.bmg, self.index = bmg, index

    def isNull(self):
        return self.index == -1 and self.bmg == -1


class Instruction:
    """
    Abstract base class for Zelda PH/ST script instructions.
    """
    type = None
    typeID = 0

    @classmethod
    def disassemble(cls, value):
        raise NotImplementedError


class SayInstruction(Instruction):
    """
    Instruction type 1: "SAY". Causes a message to appear.
    """
    type = 'SAY'
    typeID = 1

    @classmethod
    def disassemble(cls, value):

        assert value & 0xFF == 1

        bmgID = (value >> 8) & 0xFF
        messageID = (value >> 16) & 0xFFFF
        gotoIndex = (value >> 32) & 0xFFFF
        gotoBmg = (value >> 48) & 0xFF

        gotoIndex = _makeSigned(gotoIndex, 16)
        gotoBmg = _makeSigned(gotoBmg, 8)

        obj = cls()
        obj.messageBMG = bmgID
        obj.messageID = messageID
        obj.nextLabel = Label(gotoBmg, gotoIndex)
        return obj


class SwitchInstruction(Instruction):
    """
    Instruction type 2: "SW" ("switch"). Causes execution to branch to
    one of any number of labels, depending on some condition.
    """
    type = 'SW'
    typeID = 2

    @classmethod
    def disassemble(cls, value):

        assert value & 0xFF == 2

        numLabels = (value >> 8) & 0xFF
        condition = (value >> 16) & 0xFFFF
        parameter = (value >> 32) & 0xFFFF
        firstLabel = (value >> 48) & 0xFFFF

        subclass = {
            1: SwitchResponse2Instruction,
            2: SwitchResponse3Instruction,
            3: SwitchResponse4Instruction,
            4: SwitchProgressFlagInstruction,
            6: SwitchTempFlagInstruction,
            8: SwitchTemp2FlagInstruction,
            27: SwitchShopInstruction,
            }.get(condition, cls)

        obj = subclass()
        obj.condition = condition
        obj.firstLabel = firstLabel
        obj.numLabels = numLabels
        obj.parameter = parameter
        return obj

    def nameForBranch(self, i):
        return str(i)


class _SwitchInstruction_NoParameter(SwitchInstruction):
    """
    Convenience class that implements a SW instruction with no
    parameter.
    """
    @property
    def parameter(self):
        return 0
    @parameter.setter
    def parameter(self, value):
        pass


class SwitchResponse2Instruction(_SwitchInstruction_NoParameter):
    """
    A "SW" instruction that checks the player's response to a question
    message with 2 possible responses.
    """
    type = 'SW_RESP_2'

    def nameForBranch(self, i):
        return ['(first response)', '(second response)'][i]


class SwitchResponse3Instruction(_SwitchInstruction_NoParameter):
    """
    A "SW" instruction that checks the player's response to a question
    message with 3 possible responses.
    """
    type = 'SW_RESP_3'

    def nameForBranch(self, i):
        return ['(first response)', '(second response)', '(third response)'][i]


class SwitchResponse4Instruction(_SwitchInstruction_NoParameter):
    """
    A "SW" instruction that checks the player's response to a question
    message with 4 possible responses.
    """
    type = 'SW_RESP_4'

    def nameForBranch(self, i):
        return ['(first response)', '(second response)', '(third response)', '(fourth response)'][i]


class SwitchProgressFlagInstruction(SwitchInstruction):
    """
    A "SW" instruction that checks a progress flag.
    """
    type = 'SW_P_FLAG'

    # .flag is an alias for .parameter
    @property
    def flag(self):
        return self.parameter
    @flag.setter
    def flag(self, value):
        self.parameter = value

    def nameForBranch(self, i):
        return ['true', 'false'][i]


class SwitchTempFlagInstruction(SwitchInstruction):
    """
    A "SW" instruction that checks a temporary flag.
    """
    type = 'SW_T_FLAG'

    # .flag is an alias for .parameter
    @property
    def flag(self):
        return self.parameter
    @flag.setter
    def flag(self, value):
        self.parameter = value

    def nameForBranch(self, i):
        return ['true', 'false'][i]


class SwitchTemp2FlagInstruction(SwitchInstruction):
    """
    A "SW" instruction that checks a temporary 2 flag.
    """
    type = 'SW_T2_FLAG'

    # .flag is an alias for .parameter
    @property
    def flag(self):
        return self.parameter
    @flag.setter
    def flag(self, value):
        self.parameter = value

    def nameForBranch(self, i):
        return ['true', 'false'][i]


class SwitchShopInstruction(SwitchInstruction):
    """
    A "SW" instruction that switches based on the shop you're currently
    in (when parameter == 0).
    Parameter = 3 is used once, and... no clue what it's for.
    """
    type = 'SW_SHOP'

    def nameForBranch(self, i):
        return [
            'Castle Town Shop',
            "Forest's General Store",
            'Anouki General Store',
            'Papuchia Shop',
            'Goron Country Store',
            ][i]


class DoInstruction(Instruction):
    """
    Instruction type 3: "DO". Causes something to actually happen.
    """
    type = 'DO'
    typeID = 3

    @classmethod
    def disassemble(cls, value):
        assert value & 0xFF == 3

        action = (value >> 8) & 0xFF
        labelNumber = (value >> 16) & 0xFFFF
        parameter = value >> 32

        subclass = {
            0: DoSetProgressFlagInstruction,
            1: DoClearProgressFlagInstruction,
            2: DoSetTemp2FlagInstruction,
            3: DoClearTemp2FlagInstruction,
            4: DoSetTempFlagInstruction,
            5: DoClearTempFlagInstruction,
            7: DoLaunchScriptInstruction,
            }.get(action, cls)

        if action == 9:
            print(parameter)

        obj = subclass()
        obj.action = action
        obj.labelNumber = _makeSigned(labelNumber, 16)
        obj.parameter = parameter
        return obj


class DoSetProgressFlagInstruction(DoInstruction):
    """
    A "DO" instruction that sets a progress flag.
    """
    type = 'DO_SET_P_FLAG'

    # .flag is an alias for .parameter
    @property
    def flag(self):
        return self.parameter
    @flag.setter
    def flag(self, value):
        self.parameter = value


class DoClearProgressFlagInstruction(DoInstruction):
    """
    A "DO" instruction that clears a progress flag.
    """
    type = 'DO_CLR_P_FLAG'

    # .flag is an alias for .parameter
    @property
    def flag(self):
        return self.parameter
    @flag.setter
    def flag(self, value):
        self.parameter = value


class DoSetTemp2FlagInstruction(DoInstruction):
    """
    A "DO" instruction that sets a temp 2 flag.
    """
    type = 'DO_SET_T2_FLAG'

    # .flag is an alias for .parameter
    @property
    def flag(self):
        return self.parameter
    @flag.setter
    def flag(self, value):
        self.parameter = value


class DoClearTemp2FlagInstruction(DoInstruction):
    """
    A "DO" instruction that clears a temp 2 flag.
    """
    type = 'DO_CLR_T2_FLAG'

    # .flag is an alias for .parameter
    @property
    def flag(self):
        return self.parameter
    @flag.setter
    def flag(self, value):
        self.parameter = value


class DoSetTempFlagInstruction(DoInstruction):
    """
    A "DO" instruction that sets a temp flag.
    """
    type = 'DO_SET_T_FLAG'

    # .flag is an alias for .parameter
    @property
    def flag(self):
        return self.parameter
    @flag.setter
    def flag(self, value):
        self.parameter = value


class DoClearTempFlagInstruction(DoInstruction):
    """
    A "DO" instruction that clears a temp flag.
    """
    type = 'DO_CLR_T_FLAG'

    # .flag is an alias for .parameter
    @property
    def flag(self):
        return self.parameter
    @flag.setter
    def flag(self, value):
        self.parameter = value


class DoLaunchScriptInstruction(DoInstruction):
    """
    A "DO" instruction that immediately launches a different script.
    """
    type = 'DO_SCRPT'

    @property
    def parameter(self):
        return ((self.scriptID & 0xFFFF) << 16) | (self.scriptID >> 16)
    @parameter.setter
    def parameter(self, value):
        self.scriptID = ((value & 0xFFFF) << 16) | (value >> 16)


def disassembleInstruction(instruction):
    """
    Disassemble a single instruction value into an Instruction.
    """
    instID = instruction & 0xFF

    if instID not in (1, 2, 3):
        raise ValueError(f'Unknown instruction type: {instID}')

    return {
        1: SayInstruction,
        2: SwitchInstruction,
        3: DoInstruction,
        }[instID].disassemble(instruction)


def disassembleInstructions(instructions):
    """
    Given a list of instruction values, return a list of Instructions.
    """
    return [disassembleInstruction(inst) for inst in instructions]


def disassembleLabels(labels):
    """
    Given a list of label tuples, return a list of Labels.
    """
    return [Label(*L) for L in labels]