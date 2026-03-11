import sys

from PyQt6.QtWidgets import QApplication

from database.create_tables import create_tables
from ui.main_window import MainWindow

from ui.add_item_window import AddItemWindow

def main():

    print("Iniciando sistema...")

    create_tables()

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()