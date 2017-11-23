#-*- coding:utf-8 -*-
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtNetwork import QTcpServer, QAbstractSocket, QHostAddress
from binascii import a2b_hex, b2a_hex

class TcpServer(QWidget):
    recvDataReady = pyqtSignal(bytes)
    def __init__(self):
        super(TcpServer, self).__init__()
        self.tcpServer = QTcpServer()
        self.initUI()
        self.signalSlot()

    def initUI(self):
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.paraUI())
        self.setLayout(mainLayout)

    def paraUI(self):
        groupBox = QGroupBox('参数设置')
        # self.masterIP = QLineEdit('192.168.1.166')
        self.clientIP = QLineEdit('127.0.0.1')
        self.clientIP.setInputMask('000.000.000.000')
        self.clientIP.setToolTip('需要连接到Client的IP地址')
        self.clientPort = QLineEdit('1060')
        self.clientPort.setToolTip('需要连接到Client的端口')

        form = QFormLayout()
        form.addRow('Client IP地址：', self.clientIP)
        form.addRow('Client 端口号：', self.clientPort)

        self.linkRbtn = QRadioButton()

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(form)
        mainLayout.addWidget(self.linkRbtn)
        mainLayout.addStretch(1)
        mainLayout.setAlignment(self.linkRbtn, Qt.AlignHCenter)

        groupBox.setLayout(mainLayout)
        return groupBox

    def signalSlot(self):
        self.linkRbtn.clicked.connect(self.ctrlTcpStatus)
        self.tcpServer.newConnection.connect(self.addConnection)
        pass

    @pyqtSlot()
    def ctrlTcpStatus(self):
        if self.linkRbtn.isChecked():
            self.tcpServer.listen(QHostAddress.Any, 1060)
        else:
            self.tcpServer.disconnectFromHost()

    def currentStatus(self):
        if self.tcpServer.state() == QAbstractSocket.UnconnectedState:
            return 'socket没有连接'
        elif self.tcpServer.state() == QAbstractSocket.HostLookupState:
            return 'socket正在查找主机名称'
        elif self.tcpServer.state() == QAbstractSocket.ConnectingState:
            return 'socket正在查找主机名称'
        elif self.tcpServer.state() == QAbstractSocket.ConnectedState:
            return '连接已建立'
        elif self.tcpServer.state() == QAbstractSocket.BoundState:
            return 'socket绑定到一个地址和端口'
        elif self.tcpServer.state() == QAbstractSocket.ClosingState:
            return 'socket即将关闭'
        elif self.tcpServer.state() == QAbstractSocket.ConnectedState:
            return '仅限内部使用'

    def addConnection(self):
        try:
            self.clientConnection = self.tcpServer.nextPendingConnection()
            self.clientConnection.nextBlockSize = 0

            self.clientConnection.readyRead.connect(self.processTcpClientDatagrams)
            self.clientConnection.disconnected.connect(self.removeConnection)
            self.clientConnection.error.connect(self.socketError)

        except Exception as ex:
            QMessageBox.information(None, "Network Error", ex.message)

    @pyqtSlot()
    def sendTcpServerFrame(self, frame):
        self.clientConnection.write(QByteArray(a2b_hex(frame)))

    @pyqtSlot()
    def processTcpClientDatagrams(self):
        socket = self.sender()
        data = socket.readAll()
        # data = socket.readLine()
        print(data)
        data = data.data()
        print(data)
        self.recvDataReady.emit(data)

    def newConnect(self):
        print('new connect')

    def removeConnection(self):
        pass

    def socketError(self):
        pass


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ui = TcpServer()
    ui.show()
    sys.exit(app.exec_())
