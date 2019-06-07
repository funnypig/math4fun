"""

    In this module you will find modeling of Turing Machine.
    You can write your own 'algorithms' and initilize values on the line.


    Created by: Illya Antipiev

"""

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QFont, QColor
from PyQt5.QtCore import pyqtSlot, QEvent, pyqtSignal, QBasicTimer
import PyQt5.QtWidgets

import time

import TuringMachine
import sys


DIGITS = [chr(i) for i in range(ord('0'), ord('9')+1)]
DIGITS.extend([chr(i) for i in range(ord('a'), ord('z')+1)])


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
        self.grid.addWidget(self.Line, 0, 0, 1, 10)
        self.drawLine()

        #---------------------------------------------------------------------------------
        # Second line
        label = QLabel('Instructions:')
        label.setFont(self.font)
        self.grid.addWidget(label, 1, 0)

        #---------------------------------------------------------------------------------
        # Third line
        self.instructionTable = QTableWidget()
        self.instructionTable.setRowCount(self.machine.digitCount)
        self.instructionTable.setColumnCount(self.machine.stateCount)

        self.instructionTable.setVerticalHeaderLabels(self.machine.digits)
        self.instructionTable.setHorizontalHeaderLabels(['q1'])

        self.grid.addWidget(self.instructionTable, 2, 0, 3, 9)

        #---------------------------------------------------------------------------------
        # Fourth line
        self.addStateButton = QPushButton("Add state", self)
        self.addStateButton.setFont(self.font)
        self.addStateButton.clicked.connect(self.addState)

        self.addDigitButton = QPushButton("Add digit", self)
        self.addDigitButton.setFont(self.font)
        self.addDigitButton.clicked.connect(self.addDigit)

        self.grid.addWidget(self.addStateButton, 2, 10)
        self.grid.addWidget(self.addDigitButton, 3, 10)


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

        self.grid.addWidget(self.applyInstructionButton, 6, 0)
        self.grid.addWidget(self.applyCurPosButton, 6, 1)
        self.grid.addWidget(self.applyLineButton, 6, 2)


        #---------------------------------------------------------------------------------
        # Sixth line
        playfont = QFont()
        playfont.setBold(True)
        playfont.setPixelSize(30)

        self.PlayButton = QPushButton("PLAY", self)
        self.PlayButton.setFont(playfont)
        self.PlayButton.clicked.connect(self.play)

        self.grid.addWidget(self.PlayButton, 5, 10, 2, 1)

        #---------------------------------------------------------------------------------
        self.grid.setRowStretch(0,5)
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
        self.grid.addWidget(self.Line, 0, 0, 1, 10)

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

        if self.step > 50:

            try:
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
                self.timer.start(0, self)

            except StopIteration:
                self.timer.stop()

                msg = QMessageBox.about(self, "Message", "Machine has finished its work!")
                return
        else:
            time.sleep(0.01)
            self.step += 1


    @pyqtSlot()
    def play(self):

        self.timer = QBasicTimer()

        self.playMachine = self.machine.play()
        self.step = 0
        self.timer.start(0, self)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.instance().processEvents()

    ex = MachineGUI()
    sys.exit(app.exec_())