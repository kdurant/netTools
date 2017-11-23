#-*- coding:utf-8 -*-
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtNetwork import QUdpSocket, QHostAddress
from binascii import a2b_hex, b2a_hex

from tcpClient import *
from tcpServer import *
from udpWidget import *

class NetTools(QMainWindow):
    def __init__(self):
        super(NetTools, self).__init__()
        self.initUI()
        self.timer = QTimer()
        self.timer.start(1000)
        self.timer.timeout.connect(self.queryStatus)

    def initUI(self):

        self.udpModule = UdpWidget()
        self.tcpClientModule =TcpClient()
        self.tcpServerModule = TcpServer()

        test = self.testUI()

        toolbox = QToolBox()
        toolbox.addItem(self.udpModule, "UDP")
        toolbox.addItem(self.tcpServerModule, "TCP Server")
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
        self.tcpClientModule.sendTcpClientFrame('12345678123456781234567812345678')

    def queryStatus(self):
        print(self.tcpClientModule.currentStatus())

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ui = NetTools()
    ui.show()
    sys.exit(app.exec_())
