from PyQt6.QtWidgets import QApplication, QLabel
import sys

app = QApplication(sys.argv)

label = QLabel("Sistema de Estoque TI")
label.show()

app.exec()