""" LCD character generator
    Graphical generator for LCD special characters for Arduino-like boards.
    Data can be used by copy/paste to an editor.
    You can also save data to an .h file that can be included in a project or loaded
    later for reworking.

    This code is open source, published under GNU GPL3.
"""

# importing the required libraries
from PyQt5.QtCore import QFileInfo, pyqtSlot
from PyQt5.QtWidgets import (QMainWindow, QApplication, QPushButton, QWidget, QGridLayout, QHBoxLayout,
                             QPlainTextEdit, QFileDialog)
import sys


class Window(QMainWindow):
    """ Main window class """
    # this list contains the 'printing' buttons
    vlist = list()
    # this list contains the text to display
    bt_to_text = [
        "byte customChar[] = {",
        "    B00000,",
        "    B00000,",
        "    B00000,",
        "    B00000,",
        "    B00000,",
        "    B00000,",
        "    B00000,",
        "    B00000",
        "};"
    ]

    def __init__(self):
        super(Window, self).__init__()

        # set the title
        self.setWindowTitle("Lcd character generator")
        self.widget = QWidget()
        self.wlayout = QGridLayout()
        self.btlayout = QGridLayout()
        self.btlayout.setHorizontalSpacing(0)
        self.btlayout.setVerticalSpacing(0)
        self.widget.setLayout(self.wlayout)
        self.setCentralWidget(self.widget)
        # create widgets
        self.setupUI()

    def setupUI(self):
        # populate buttons and add them to a grid
        hlist = []
        for i in range(8):
            for j in range(5):
                hlist.append(QPushButton("", self))
                hlist[j].setCheckable(True)
                hlist[j].resize(50, 50)
                hlist[j].setStyleSheet("background-color : lightgrey")
                hlist[j].clicked.connect(self.set_buttons)
                self.btlayout.addWidget(hlist[j], i, j)
            self.vlist = self.vlist + hlist
            hlist.clear()
        # add buttons layout to window layout
        self.wlayout.addLayout(self.btlayout, 0, 0)
        # create 'system' buttons
        self.clearBtn = QPushButton("Clear", self)
        self.clearBtn.clicked.connect(self.clear_data)
        self.saveBtn = QPushButton("Save", self)
        self.saveBtn.clicked.connect(self.save_file)
        self.loadBtn = QPushButton("Load", self)
        self.loadBtn.clicked.connect(self.load_file)
        self.exitBtn = QPushButton("Exit", self)
        self.exitBtn.clicked.connect(self.exitapp)
        # create a text box and add text
        self.textedit = QPlainTextEdit()
        self.textedit.setReadOnly(True)
        for x in self.bt_to_text:
            self.textedit.appendPlainText(x)
        self.wlayout.addWidget(self.textedit, 0, 1)
        # create an horizontal layout for the 'system' buttons
        horlay = QHBoxLayout()
        horlay.addWidget(self.clearBtn)
        horlay.addWidget(self.loadBtn)
        horlay.addWidget(self.saveBtn)
        horlay.addWidget(self.exitBtn)
        self.wlayout.addLayout(horlay, 1, 1)

        # show all the widgets
        self.update()
        self.show()

    @pyqtSlot()
    def set_buttons(self):
        """ callback used by 'printing' buttons """
        for i in range(len(self.vlist)):
            if self.vlist[i].isChecked():
                # setting background color to light-blue
                self.vlist[i].setStyleSheet("background-color : lightblue")
            else:
                # set background color back to light-grey
                self.vlist[i].setStyleSheet("background-color : lightgrey")
        # clear text
        self.textedit.clear()
        # create the text according to buttons state
        tmp_str = "    B"
        for i in range(8):
            for j in range(5):
                tmp_str = tmp_str + str(int(self.vlist[5*i + j].isChecked()))
            if i < 7:
                self.bt_to_text[i+1] = tmp_str + ","
            else:
                self.bt_to_text[i+1] = tmp_str
            tmp_str = "    B"
        # display text
        for x in self.bt_to_text:
            self.textedit.appendPlainText(x)

    @pyqtSlot()
    def exitapp(self):
        """ Exit button callback - exits to system """
        QApplication.instance().quit()

    @pyqtSlot()
    def clear_data(self):
        """ Clear button callback. Clear text and buttons """
        self.textedit.clear()
        for i in range(40):
            self.vlist[i].setChecked(False)
            self.vlist[i].setStyleSheet("background-color : lightgrey")
        for i in range(7):
            self.bt_to_text[i+1] = "    B00000,"
        self.bt_to_text[8] = "    B00000"
        for x in self.bt_to_text:
            self.textedit.appendPlainText(x)

    @pyqtSlot()
    def load_file(self):
        """ Load button callback. Load data from disk """
        # erase previous data
        self.clear_data()
        # open file selection dialog
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "Load file",
                                                  "", """Lcd files
                                                   (*.h);;All Files (*)""",
                                                  options=options)
        # file can be opened
        if fileName:
            # read data from file
            with open(fileName, 'r')as file:
                for x in range(len(self.bt_to_text)):
                    self.bt_to_text[x] = file.readline().strip('\n')
            # set buttons state
            for i in range(8):
                tmp_str = self.bt_to_text[i+1]
                tmp_str = tmp_str[5:]
                for j in range(5):
                    x = tmp_str[j]
                    self.vlist[5*i+j].setChecked(int(x))
            self.set_buttons()

    @pyqtSlot()
    def save_file(self):
        """ Save button callback. Save data to disk """
        # open file selection dialog
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "Save file", "",
                                                  """Lcd files
                                                   (*.h);;All Files (*)""",
                                                  options=options)
        # file can be written
        if fileName:
            # add .h suffix if not in filename
            if not QFileInfo(fileName).suffix():
                fileName += '.h'
            # write data to file
            with open(fileName, 'w')as file:
                for x in self.bt_to_text:
                    file.write(x+"\n")


# create pyqt5 app
App = QApplication(sys.argv)

# create the instance of our Window
window = Window()

# start the app
sys.exit(App.exec())
