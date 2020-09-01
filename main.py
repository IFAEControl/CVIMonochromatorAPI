import platform
import sys
from PyQt5 import QtWidgets as QtW
from PyQt5 import QtCore as QtC
from PyQt5 import QtGui as QtG
from cvi_gui import Ui_Form
from CVIMonochromator import CVIMonochromator

serial_device = ''

if platform.system() == 'Darwin':
    print("I'm on macOS!")
    serial_device = '/dev/tty.usbserial'
elif platform.system() == 'Windows':
    print("I'm on Windows!")
    serial_device = 'COM3'
elif platform.system() == 'Linux':
    print("I'm on Linux!")
    serial_device = '/dev/ttyUSB0'
else:
    print("Fuck, don't know the platform I'm running...")


class MainWindow(QtW.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.cvi_monochromator = CVIMonochromator(serial_device)

        self.ui.unitsLabel.setText("nm")
        self.ui.gotoButton.clicked.connect(self.goto_function)

        # Your code ends here
        self.show()

    def goto_function(self):
        print(self.ui.spinBox.text())
        self.cvi_monochromator.goto(int(self.ui.spinBox.text()))
        self.ui.wavelenghtDisplay.setText(self.ui.spinBox.text())


if __name__ == '__main__':
    app = QtW.QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())
