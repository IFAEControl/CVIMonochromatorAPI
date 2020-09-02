import platform
import sys
from PyQt5 import QtWidgets as QtW
from PyQt5 import QtCore as QtC
from PyQt5 import QtGui as QtG
from cvi_gui import Ui_Form
from CVIMonochromator import CVIMonochromator
from serial_ports_list import get_available_ports as get_ports
from time import sleep


if platform.system() == 'Darwin':
    print("I'm on macOS!")
elif platform.system() == 'Windows':
    print("I'm on Windows!")
elif platform.system() == 'Linux':
    print("I'm on Linux!")
else:
    print("Fuck, don't know the platform I'm running...")


class MainWindow(QtW.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.cvi_monochromator = CVIMonochromator()

        self.ui.unitsLabel.setText("nm")
        self.ui.availableSerialsList.addItems(get_ports())
        self.ui.refreshPortsListButton.clicked.connect(self.refresh_ports_list)
        self.ui.connectSerialButton.clicked.connect(self.connect_serial_port)
        self.ui.disconnectSerialButton.clicked.connect(self.disconnect_serial_port)
        self.ui.gotoButton.clicked.connect(self.goto_function)
        self.ui.forwardButton.clicked.connect(self.forward)
        self.ui.backwardButton.clicked.connect(self.backward)

        self.ui.queryPosButton.clicked.connect(self.query_position)

        # Your code ends here
        self.show()

    def goto_function(self):
        if self.cvi_monochromator.isConnected():
            self.cvi_monochromator.goto(int(self.ui.spinBox.text()))

    def refresh_ports_list(self):
        self.ui.availableSerialsList.clear()
        self.ui.availableSerialsList.addItems(get_ports())

    def connect_serial_port(self):
        if not self.cvi_monochromator.isConnected():
            print("Connecting!")
            self.cvi_monochromator.openCommunication(self.ui.availableSerialsList.currentText())
        else:
            print("Already connected, don't try to reconnect!")

    def disconnect_serial_port(self):
        if self.cvi_monochromator.isConnected():
            self.cvi_monochromator.closeCommunication()

    def query_position(self):
        if self.cvi_monochromator.isConnected():
            self.ui.wavelenghtDisplay.setText(str(self.cvi_monochromator.query(0)))

    def forward(self):
        if self.cvi_monochromator.isConnected():
            if self.cvi_monochromator.query(0) < 1032:
                self.cvi_monochromator.goto(self.cvi_monochromator.query(0) + 1)
                sleep(0.2)
                self.ui.wavelenghtDisplay.setText(str(self.cvi_monochromator.query(0)))

    def backward(self):
        if self.cvi_monochromator.isConnected():
            if self.cvi_monochromator.query(0) > 1:
                self.cvi_monochromator.goto(self.cvi_monochromator.query(0) - 1)
                sleep(0.2)
                self.ui.wavelenghtDisplay.setText(str(self.cvi_monochromator.query(0)))


if __name__ == '__main__':
    app = QtW.QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())
