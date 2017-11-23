#-*- coding:utf-8 -*-
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtNetwork import QTcpSocket, QAbstractSocket, QHostAddress
from binascii import a2b_hex, b2a_hex

class TcpClient(QWidget):
    tcpClientRecvDataReady = pyqtSignal(bytes)
    def __init__(self):
        super(TcpClient, self).__init__()
        self.tcpClient = QTcpSocket()
        self.initUI()
        self.signalSlot()

    def initUI(self):
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.paraUI())
        self.setLayout(mainLayout)

    def paraUI(self):
        groupBox = QGroupBox('参数设置')
        # self.masterIP = QLineEdit('192.168.1.166')
        self.serverIP = QLineEdit('127.0.0.1')
        self.serverIP.setInputMask('000.000.000.000')
        self.serverIP.setToolTip('需要连接到Server的IP地址')
        self.serverPort = QLineEdit('1060')
        self.serverPort.setToolTip('需要连接到Server的端口')

        form = QFormLayout()
        form.addRow('Server IP地址：', self.serverIP)
        form.addRow('Server 端口号：', self.serverPort)

        self.linkRbtn = QRadioButton()

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(form)
        mainLayout.addWidget(self.linkRbtn)

        groupBox.setLayout(mainLayout)
        return groupBox

    def signalSlot(self):
        self.linkRbtn.clicked.connect(self.ctrlTcpStatus)
        self.linkRbtn.clicked.connect(self.currentTcpStatus)
        self.tcpClient.connected.connect(self.hasConnected)
        self.tcpClient.disconnected.connect(self.hasClosed)
        self.tcpClient.readyRead.connect(self.processTcpClientDatagrams)

    @pyqtSlot()
    def ctrlTcpStatus(self):
        if self.linkRbtn.isChecked():
            self.tcpClient.connectToHost(self.serverIP.text(), int(self.serverPort.text()))
        else:
            self.tcpClient.disconnectFromHost()

    def currentTcpStatus(self):
        if self.tcpClient.state() == QAbstractSocket.UnconnectedState:
            QMessageBox.information(self, '信息', 'socket没有连接')
        elif self.tcpClient.state() == QAbstractSocket.HostLookupState:
            QMessageBox.information(self, '信息', 'socket正在查找主机名称')
        elif self.tcpClient.state() == QAbstractSocket.ConnectingState:
            QMessageBox.information(self, '信息', 'socket正在查找主机名称')
        elif self.tcpClient.state() == QAbstractSocket.ConnectedState:
            QMessageBox.information(self, '信息', '连接已建立')
        elif self.tcpClient.state() == QAbstractSocket.BoundState:
            QMessageBox.information(self, '信息', 'socket绑定到一个地址和端口')
        elif self.tcpClient.state() == QAbstractSocket.ClosingState:
            QMessageBox.information(self, '信息', 'socket即将关闭')
        elif self.tcpClient.state() == QAbstractSocket.ConnectedState:
            QMessageBox.information(self, '信息', '仅限内部使用')

    @pyqtSlot()
    def processTcpClientDatagrams(self):
        data = self.tcpClient.readLine()
        data = data.data()
        print(data)
        self.tcpClientRecvDataReady.emit(data)

    @pyqtSlot()
    def sendTcpClientFrame(self, frame):
        self.tcpClient.write(QByteArray(a2b_hex(frame)))

    @pyqtSlot()
    def hasConnected(self):
        QMessageBox.information(self, '信息', '已连接到TCP Server')
        pass

    @pyqtSlot()
    def hasClosed(self):
        QMessageBox.information(self, '信息', '已关闭到TCP Server的连接')
        self.tcpClient.close()

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ui = TcpClient()
    ui.show()
    sys.exit(app.exec_())