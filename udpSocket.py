#-*- coding:utf-8 -*-
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtNetwork import QUdpSocket, QAbstractSocket, QHostAddress
from binascii import a2b_hex, b2a_hex
import socket
from threading import Thread

class Socket(QObject):
    recvDataReady = pyqtSignal(bytes, str, int)
    def __init__(self):
        super(Socket, self).__init__()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.runFlag = False

    def config(self, addr, port, buf_size):

        # self.socket.bind(('127.0.0.1', 6666))
        self.socket.bind((addr, port))
        self.buf_size = buf_size

    def start(self):
        self.runFlag = True

    def stop(self):
        self.runFlag = False

    def close(self):
        self.socket.close()

    def receive(self):
        while self.runFlag:
            data, address = self.udpServerSocket.recvfrom(self.buf_size)
            self.recvDataReady.emit(data, address[0], address[1])



class UdpCore(QWidget):
    '''
    UDP作为Server，只需要绑定本机IP地址和端口号，Client发送数据时，指定正确的地址和端口号即可
    '''
    recvDataReady = pyqtSignal(bytes, str, int)
    def __init__(self):
        super(UdpCore, self).__init__()
        self.initUI()
        self.udpSocket = Socket()
        self.signalSlot()

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

        # self.targetIP = QLineEdit('192.168.1.102')
        self.targetIP = QLineEdit('127.0.0.1')
        self.targetIP.setInputMask('000.000.000.000')
        self.targetIP.setToolTip('发送数据时，本机需要匹配其他设备IP地址和端口号')
        self.targetPort = QLineEdit('4444')

        self.bindRbtn = QRadioButton()
        self.bindRbtn.setObjectName('singleRadioBtn')

        form = QFormLayout()
        form.addRow('本机IP地址：', self.masterIP)
        form.addRow('本机端口号：', self.masterPort)
        form.addRow('设备IP地址：', self.targetIP)
        form.addRow('UDP端口号：', self.targetPort)

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.bindRbtn)
        hbox.addStretch(1)

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(form)
        mainLayout.addLayout(hbox)

        groupBox.setLayout(mainLayout)
        return groupBox

    def signalSlot(self):
        self.bindRbtn.clicked.connect(self.udpLinkStatus)
        self.udpSocket.recvDataReady[bytes, str, int].connect(self.processUDPDatagrams)

    # def udpConfig(self):
    #     self.udpSocket.config(self.masterIP.text(), int(self.masterPort.text()), 2048)

    @pyqtSlot(str)
    def sendFrame(self, frame, dataMode='hex', boardCast=False):
        if dataMode == 'utf8':
            data = frame.encode(encoding='utf-8')
        elif dataMode == 'hex':
            data = a2b_hex(frame)
        elif dataMode == 'ascii':
            data = a2b_hex(frame)
        else:
            data = a2b_hex(frame)


    @pyqtSlot()
    def processUDPDatagrams(self, data, addr, port):
        print(data)

    @pyqtSlot()
    def udpLinkStatus(self):
        if self.bindRbtn.isChecked():
            try:
                self.udpSocket.config(self.masterIP.text(), int(self.masterPort.text()), 2048)
            except OSError:
                QMessageBox.warning(self, "警告", 'UDP端口被占用')
        else:
            self.udpSocket.close()
        pass

    def currentStatus(self):
        pass

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ui = UdpCore()
    ui.show()
    sys.exit(app.exec_())
