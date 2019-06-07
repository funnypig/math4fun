
"""
    ASSUMING START STATE IS 1 AND FINISH STATE IS 0

------------------------------------------------------------------------------------------
    stateCount: number of states
    digitCount: power of set we are working on/ number of digits

------------------------------------------------------------------------------------------
    lineLength: number of cells in a row
    line: initial line

------------------------------------------------------------------------------------------
    instruction: dict of dict
        - key1: state
        - key2: digit

        value: tuple (setNumber, moveTo, newState)

        f.e. 00(q2)100 => State: q2; Digit: 1.
            take instruction: self.instruction[2][1]
------------------------------------------------------------------------------------------
"""

class TuringMachine:
    def __init__(self, stateCount = 1, digitCount = 2, lineLength = 100, line = []):

        self.stateCount = stateCount
        self.digitCount = digitCount

        self.digits = [str(i) for i in range(digitCount)]
        self.instruction = {1:{}}

        self.lineLength = lineLength
        self.line = line

        while len(self.line) < self.lineLength:
            self.line.append('0')

        self.curState = 1
        self.curPosition = 0

    def addDigit(self, digit):
        self.digitCount+=1
        self.digits.append(digit)

    def addState(self):
        self.stateCount+=1

    def setInstruction(self, stateNumber, digit, instruction):
        if not stateNumber in self.instruction:
            self.instruction[stateNumber] = {}

        self.instruction[stateNumber][digit] = instruction
        self.curState = 1

    def setStartPosition(self, pos):
        self.curPosition = pos % self.lineLength
        self.curState = 1

    def setLine(self, line):
        while len(self.line)<len(line):
            self.line.append('0')
            self.lineLength+=1

        for i in range(len(line)):
            self.line[i] = line[i]

    def play(self):

        while self.curState != 0:

            newNumber, moveTo, newState = self.instruction[self.curState][self.line[self.curPosition]]

            self.line[self.curPosition] = newNumber

            if moveTo == 'R':
                if self.curPosition >= self.lineLength-3:
                    self.line.append('0')
                    self.lineLength+=1

                self.curPosition += 1

            elif moveTo == 'L':
                if self.curPosition <= 2:
                    self.line.insert(0, '0')
                    self.lineLength+=1

                self.curPosition -= 1
            else:
                pass

            self.curState = newState

            yield newNumber, moveTo, newState

        self.curState = 1