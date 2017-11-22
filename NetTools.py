#-*- coding:utf-8 -*-
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtNetwork import QUdpSocket, QHostAddress
from binascii import a2b_hex, b2a_hex

from udpWidget import *

class NetTools(QMainWindow):
    def __init__(self):
        super(NetTools, self).__init__()
        self.initUI()

    def initUI(self):
        self.udpModule = UdpWidget()

        vbox = QVBoxLayout()
        vbox.addWidget(self.udpModule)

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(vbox)

        mainWidget = QWidget()
        mainWidget.setLayout(mainLayout)
        self.setCentralWidget(mainWidget)
        pass

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ui = NetTools()
    ui.show()
    sys.exit(app.exec_())