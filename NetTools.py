#-*- coding:utf-8 -*-
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtNetwork import QUdpSocket, QHostAddress
from binascii import a2b_hex, b2a_hex

from tcpClient import *
from tcpServer import *
from udpCore import *

class NetTools(QMainWindow):
    def __init__(self):
        super(NetTools, self).__init__()
        self.initUI()
        self.timer = QTimer()
        self.timer.start(1000)
        self.timer.timeout.connect(self.queryStatus)


    def initUI(self):

        self.udpModule = UdpCore()
        self.tcpClientModule = TcpClient()
        self.tcpServerModule = TcpServer()

        self.udpModule.recvDataReady[bytes, str, int].connect(self.showUdpData)
        self.tcpClientModule.recvDataReady[bytes].connect(self.showData)
        self.tcpServerModule.recvDataReady[bytes].connect(self.showData)
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

        self.sendText = QTextEdit()
        self.recvText = QTextEdit()
        self.btn = QPushButton('send')
        self.btn.clicked.connect(self.sendData)
        vbox = QVBoxLayout()
        vbox.addWidget(self.recvText)
        vbox.addWidget(self.btn)
        vbox.addWidget(self.sendText)

        frame = QFrame()
        frame.setLayout(vbox)

        return frame

    def sendData(self):
        data = self.recvText.toPlainText()
        self.udpModule.sendUdpFrame(data, 'utf8')
        # self.tcpClientModule.sendTcpClientFrame(self.recvText.toPlainText())

    def showData(self, frame):
        data = frame.decode(encoding='utf-8')
        self.sendText.append(data)
        pass

    def showUdpData(self, frame, host, port):
        data = frame.decode(encoding='utf-8')
        self.sendText.append(data)
        pass

    def queryStatus(self):
        print(self.udpModule.currentStatus())
        pass

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ui = NetTools()
    ui.show()
    sys.exit(app.exec_())
