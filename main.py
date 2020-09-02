import platform
import sys
from PyQt5 import QtWidgets as QtW
from PyQt5 import QtCore as QtC
from PyQt5 import QtGui as QtG
from cvi_gui import Ui_Form
from CVIMonochromator import CVIMonochromator
from serial_ports_list import get_available_ports as get_ports


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
        self.ui.connectSerialButton.clicked.connect(self.connect_serial_port)
        self.ui.gotoButton.clicked.connect(self.goto_function)

        # Your code ends here
        self.show()

    def goto_function(self):
        print(self.ui.spinBox.text())
        self.cvi_monochromator.goto(int(self.ui.spinBox.text()))
        self.ui.wavelenghtDisplay.setText(self.ui.spinBox.text())

    def connect_serial_port(self):
        self.cvi_monochromator.openCommunication(self.ui.availableSerialsList.currentText())


if __name__ == '__main__':
    app = QtW.QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())
