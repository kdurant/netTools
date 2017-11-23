#-*- coding:utf-8 -*-
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtNetwork import QTcpSocket, QHostAddress
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
        self.tcpClient.connected.connect(self.sendRequest)
        self.tcpClient.disconnected.connect(self.serverHasStopped)
        self.tcpClient.readyRead.connect(self.processTcpClientDatagrams)

    @pyqtSlot()
    def ctrlTcpStatus(self):
        if self.linkRbtn.isChecked():
            self.tcpClient.connectToHost(self.serverIP.text(), int(self.serverPort.text()))
        else:
            self.tcpClient.disconnectFromHost()

    @pyqtSlot()
    def processTcpClientDatagrams(self):
        data = self.tcpClient.readLine()
        print(data)
        self.tcpClientRecvDataReady.emit(data)

    @pyqtSlot()
    def sendTcpClientFrame(self, frame):
        self.tcpClient.write(QByteArray(a2b_hex(frame)))

    @pyqtSlot()
    def sendRequest(self):
        # QMessageBox.information(self, '信息', '已连接到TCP Server')
        print('connect')
        pass

    @pyqtSlot()
    def serverHasStopped(self):
        print('disconnect')
        self.tcpClient.close()

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ui = TcpClient()
    ui.show()
    sys.exit(app.exec_())