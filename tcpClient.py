#-*- coding:utf-8 -*-
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtNetwork import QTcpSocket, QHostAddress
from binascii import a2b_hex, b2a_hex

class TcpClient(QWidget):
    def __init__(self):
        super(TcpClient, self).__init__()
        self.tcpClient = QTcpSocket()
        self.initUI()
        # self.tcpClient.connectToHost('127.0.0.1', 1060)
        self.tcpClient.connected.connect(self.sendRequest)
        self.tcpClient.disconnected.connect(self.serverHasStopped)
        # self.signalSlot()


    def initUI(self):
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.paraUI())
        self.setLayout(mainLayout)

    def paraUI(self):
        groupBox = QGroupBox('参数设置')
        # self.masterIP = QLineEdit('192.168.1.166')
        self.masterIP = QLineEdit('127.0.0.1')
        self.masterIP.setInputMask('000.000.000.000')
        self.masterIP.setToolTip('接收数据时，其他设备需要匹配本机IP地址和端口号')
        self.masterPort = QLineEdit('6666')

        form = QFormLayout()
        form.addRow('本机IP地址：', self.masterIP)
        form.addRow('本机端口号：', self.masterPort)

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(form)
        mainLayout.addLayout(form)

        groupBox.setLayout(mainLayout)
        return groupBox

    def sendTcpFrame(self, frame):

        self.tcpClient.connectToHost(self.masterIP.text(), 1060)
        self.tcpClient.write(QByteArray(a2b_hex(frame)))

    def sendRequest(self):
        # QMessageBox.information(self, '信息', '已连接到TCP Server')
        pass

    def serverHasStopped(self):
        self.tcpClient.close()

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ui = TcpClient()
    ui.show()
    sys.exit(app.exec_())