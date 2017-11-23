#-*- coding:utf-8 -*-
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtNetwork import QUdpSocket, QHostAddress
from binascii import a2b_hex, b2a_hex

from tcpClient import *

from udpWidget import *

class NetTools(QMainWindow):
    def __init__(self):
        super(NetTools, self).__init__()
        self.initUI()

    def initUI(self):

        self.udpModule = UdpWidget()
        self.tcpClientModule =TcpClient()

        test = self.testUI()

        toolbox = QToolBox()
        toolbox.addItem(self.udpModule, "UDP")
        toolbox.addItem(QLabel('123'), "TCP Server")
        toolbox.addItem(self.tcpClientModule, "TCP Client")


        vbox = QVBoxLayout()
        vbox.addWidget(toolbox)
        vbox.addWidget(test)

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(vbox)

        mainWidget = QWidget()
        mainWidget.setLayout(mainLayout)
        self.setCentralWidget(mainWidget)
        pass

    def testUI(self):

        self.btn = QPushButton('send')
        self.btn.clicked.connect(self.sendData)
        vbox = QVBoxLayout()
        vbox.addWidget(self.btn)

        frame = QFrame()
        frame.setLayout(vbox)

        return frame

    def sendData(self):
        # self.udpModule.sendUdpFrame('1234', 'utf8')
        self.tcpClientModule.sendTcpFrame('12345678123456781234567812345678')

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ui = NetTools()
    ui.show()
    sys.exit(app.exec_())