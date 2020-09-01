import sys
from PyQt5 import QtWidgets as QtW
from PyQt5 import QtCore as QtC
from PyQt5 import QtGui as QtG
from cvi_gui import Ui_Form
from CVIMonochromator import CVIMonochromator


class MainWindow(QtW.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.cvi_monochromator = CVIMonochromator("COM5")

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
