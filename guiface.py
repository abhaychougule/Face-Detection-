import sys
from PyQt5 import QtGui

app = QtGui.QApplication(sys.argv)

window = QtGui.QWidget()
window.setGeometry(0, 0, 500, 300)
window.setWindowTitle("PyQT Tuts!")

window.show()
