"""

    In this module you will find modeling of Turing Machine.
    You can write your own 'algorithms' and initilize values on the line.


    Created by: Illya Antipiev

"""

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QFont, QColor
from PyQt5.QtCore import pyqtSlot, QEvent, pyqtSignal, QBasicTimer
import PyQt5.QtWidgets

import clipboard
import time
import pickle

import TuringMachine
import sys


DIGITS = [chr(i) for i in range(ord('0'), ord('9')+1)]
DIGITS.extend([chr(i) for i in range(ord('a'), ord('z')+1)])

SPEED = 50

class MachineGUI(QWidget):

    def __init__(self):
        super().__init__()

        self.machine = TuringMachine.TuringMachine()

        self.font = QFont()
        self.font.setBold(True)
        self.font.setPixelSize(16)


        self.initUI()


    @pyqtSlot()
    def MultiEnter(self, *args):
        print(args)

    def initUI(self):
        self.setGeometry(300, 300, 1000, 300)
        self.setWindowTitle('Turing machine')
        self.setWindowIcon(QIcon('ico.png'))

        self.grid = QGridLayout()
        self.setLayout(self.grid)

        #---------------------------------------------------------------------------------
        # First line
        self.Line = QTableWidget()
        self.grid.addWidget(self.Line, 0, 0, 2, 9)
        self.drawLine()

        self.SaveLineButton = QPushButton("Copy")
        self.PasteLineButton = QPushButton("Paste")

        self.SaveLineButton.clicked.connect(self.SaveLine)
        self.PasteLineButton.clicked.connect(self.PasteLine)
        self.SaveLineButton.setFont(self.font)
        self.PasteLineButton.setFont(self.font)

        self.grid.addWidget(self.PasteLineButton, 0, 10)
        self.grid.addWidget(self.SaveLineButton, 1, 10)

        #---------------------------------------------------------------------------------
        # Second line
        label = QLabel('Instructions:')
        label.setFont(self.font)
        self.grid.addWidget(label, 2, 0)

        #---------------------------------------------------------------------------------
        # Third line
        self.instructionTable = QTableWidget()
        self.instructionTable.setRowCount(self.machine.digitCount)
        self.instructionTable.setColumnCount(self.machine.stateCount)

        self.instructionTable.setVerticalHeaderLabels(self.machine.digits)
        self.instructionTable.setHorizontalHeaderLabels(['q1'])

        self.grid.addWidget(self.instructionTable, 3, 0, 4, 9)

        #---------------------------------------------------------------------------------
        # Fourth line
        self.addStateButton = QPushButton("Add state", self)
        self.addStateButton.setFont(self.font)
        self.addStateButton.clicked.connect(self.addState)

        self.addDigitButton = QPushButton("Add digit", self)
        self.addDigitButton.setFont(self.font)
        self.addDigitButton.clicked.connect(self.addDigit)

        self.grid.addWidget(self.addStateButton, 3, 10)
        self.grid.addWidget(self.addDigitButton, 4, 10)


        self.importMachineButton = QPushButton("Import")
        self.importMachineButton.setFont(self.font)
        self.importMachineButton.clicked.connect(self.importMachine)

        self.saveMachineButton = QPushButton("Save")
        self.saveMachineButton.setFont(self.font)
        self.saveMachineButton.clicked.connect(self.saveMachine)

        self.grid.addWidget(self.saveMachineButton, 5, 10)
        self.grid.addWidget(self.importMachineButton, 6, 10)


        #
        self.grid.addWidget(QLabel(""), 8, 0)

        #---------------------------------------------------------------------------------
        # Fifth line
        self.applyInstructionButton = QPushButton("Apply instructions", self)
        self.applyCurPosButton = QPushButton("Apply current position", self)
        self.applyLineButton = QPushButton("Apply line", self)

        self.applyInstructionButton.setFont(self.font)
        self.applyCurPosButton.setFont(self.font)
        self.applyLineButton.setFont(self.font)

        self.applyInstructionButton.clicked.connect(self.applyInstruction)
        self.applyCurPosButton.clicked.connect(self.applyCurPos)
        self.applyLineButton.clicked.connect(self.applyLine)

        self.grid.addWidget(self.applyInstructionButton, 9, 0)
        self.grid.addWidget(self.applyCurPosButton, 9, 1)
        self.grid.addWidget(self.applyLineButton, 9, 2)


        #---------------------------------------------------------------------------------
        # Sixth line
        playfont = QFont()
        playfont.setBold(True)
        playfont.setPixelSize(22)

        self.PlayButton = QPushButton("PLAY", self)
        self.PlayButton.setFont(playfont)
        self.PlayButton.clicked.connect(self.play)

        self.grid.addWidget(self.PlayButton, 9, 10)

        self.Stop = True
        self.StopButton = QPushButton("STOP", self)
        self.StopButton.setFont(playfont)
        self.StopButton.clicked.connect(self.setStop)

        self.grid.addWidget(self.StopButton, 10, 10)

        # Speed box
        sp = QLabel("Speed (1-100):")
        sp.setFont(self.font)
        self.grid.addWidget(sp, 10, 0)
        self.speedBox = QLineEdit("50")
        self.grid.addWidget(self.speedBox,10, 1)
        self.speedBox.textChanged.connect(lambda s: self.setSpeed(s))

        #---------------------------------------------------------------------------------
        #self.grid.setRowStretch(0,6)
        self.grid.activate()
        self.show()

    def eventFilter(self, QObject, QEvent):
        print(QObject)
        return False

    def drawLine(self):

        self.Line = QTableWidget()
        self.Line.setColumnCount(self.machine.lineLength)
        self.Line.setRowCount(1)

        headers = []
        for pos in range(self.machine.lineLength):
            self.Line.setItem(0, pos, QTableWidgetItem(str(self.machine.line[pos])))

            if self.machine.curPosition == pos:
                headers.append('q'+str(self.machine.curState))
            else:
                headers.append(' ')

        self.Line.setCurrentCell(0, self.machine.curPosition)

        self.Line.setHorizontalHeaderLabels(headers)
        self.Line.resizeRowsToContents()
        self.Line.resizeColumnsToContents()
        self.grid.addWidget(self.Line, 0, 0, 2, 9)

    @pyqtSlot()
    def PasteLine(self):
        s = clipboard.paste()
        line = []
        for si in s:
            if si in self.machine.digits:
                line.append(si)
        self.machine.setLine(line)
        self.drawLine()

    @pyqtSlot()
    def SaveLine(self):
        clipboard.copy(''.join(self.machine.line))

    @pyqtSlot()
    def setSpeed(self, s):
        global SPEED

        try:
            sp = int(s)
            if sp>=100: sp = 100
            if sp<1: sp = 1

            SPEED = 1050-sp*10

            self.speedBox.setStyleSheet("background-color: rgb(255,255,255);")
        except:
            self.speedBox.setStyleSheet("background-color: rgb(244, 66, 146);")

    @pyqtSlot()
    def importMachine(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fname, _ = QFileDialog.getOpenFileName(self, "Save Turing Machine", "", "Machine (*.pickle)", options=options)

        file = open(fname, 'rb')
        TM = pickle.loads(file.read())
        file.close()

        copyline = self.machine.line.copy()
        self.machine = TM
        self.machine.setLine(copyline)

        self.instructionTable.clear()

    def saveMachine(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fname, _ = QFileDialog.getSaveFileName(self, "Save Turing Machine", "", "Machine (*.pickle)", options=options)

        with open(fname, 'wb') as file:
            file.write(pickle.dumps(self.machine))

    @pyqtSlot()
    def setStop(self):
        self.Stop = True

    @pyqtSlot()
    def addState(self):
        self.machine.addState()
        self.instructionTable.setColumnCount(self.machine.stateCount)

        headers = ['q{}'.format(i) for i in range(1, self.machine.stateCount+1)]
        self.instructionTable.setHorizontalHeaderLabels(headers)

    @pyqtSlot()
    def addDigit(self):

        self.machine.addDigit(DIGITS[self.machine.digitCount])

        self.instructionTable.setRowCount(self.machine.digitCount)
        self.instructionTable.setVerticalHeaderLabels(self.machine.digits)

    @pyqtSlot()
    def applyInstruction(self):
        rows = self.instructionTable.rowCount()
        cols = self.instructionTable.columnCount()

        for i in range(rows):
            for j in range(cols):

                item = self.instructionTable.item(i, j)

                if item is None:
                    continue

                txt = item.text().strip()

                try:

                    vals = txt.split()
                    newDigit, moveTo, newState = vals[0], vals[1], int(vals[2])

                    assert moveTo == 'S' or moveTo == 'R' or moveTo == 'L', ''
                    assert newDigit in self.machine.digits, ''
                    assert newState<=self.machine.stateCount, ''

                    self.machine.setInstruction(j+1, DIGITS[i], (newDigit, moveTo, newState))

                    item.setBackground(QColor(255, 255, 255))
                except:
                    item.setBackground(QColor(244, 66, 146))

        self.instructionTable.clearSelection()


    @pyqtSlot()
    def applyCurPos(self):
        self.machine.curPosition = self.Line.selectedIndexes()[0].column()

        self.drawLine()

    @pyqtSlot()
    def applyLine(self):

        line = []
        for i in range(self.Line.columnCount()):
            try:
                dig = self.Line.item(0, i).text().strip()

                assert dig in self.machine.digits

                line.append(dig)

                self.Line.item(0, i).setBackground(QColor(255, 255, 255))
            except:
                self.Line.item(0, i).setBackground(QColor(244, 66, 146))

        self.machine.setLine(line)

        self.Line.clearSelection()


    def timerEvent(self, QTimerEvent):

        try:
            if self.Stop:
                raise StopIteration

            try:
                playState = next(self.playMachine)
                newDigit, moveTo, newState = playState
            except KeyError:
                msg = QMessageBox.about(self, "Message", "Machine failed!")
                self.timer.stop()
                return
            if newState!=0:
                for i in range(self.instructionTable.rowCount()):
                    for j in range(self.instructionTable.columnCount()):
                        try:
                            self.instructionTable.item(i, j).setBackground(QColor(255, 255, 255))
                        except: pass
                #print(DIGITS.index(newDigit), newState-1)
                try:
                    self.instructionTable.item(DIGITS.index(newDigit), newState-1).setBackground(QColor(171, 255, 130))
                except: pass

            self.drawLine()
            self.step = 0
            self.timer.start(SPEED, self)

        except StopIteration:
            self.timer.stop()

            # clean colors
            for i in range(self.instructionTable.rowCount()):
                for j in range(self.instructionTable.columnCount()):
                    try:
                        self.instructionTable.item(i, j).setBackground(QColor(255, 255, 255))
                    except:
                        pass


            msg = QMessageBox.about(self, "Message", "Machine has finished its work!")
            return



    @pyqtSlot()
    def play(self):

        self.Stop = False
        self.timer = QBasicTimer()

        self.playMachine = self.machine.play()
        self.step = 0
        self.timer.start(0, self)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.instance().processEvents()

    ex = MachineGUI()
    sys.exit(app.exec_())