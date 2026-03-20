import sys
from PyQt6.QtWidgets import QApplication

from database.create_tables import create_tables
from services.usuario_service import criar_usuario_padrao
from ui.login_window import LoginWindow

def main():
    print("Iniciando sistema...")

    # Prepara o banco de dados
    create_tables()
    criar_usuario_padrao()

    app = QApplication(sys.argv)

    # Inicia pela janela de LOGIN
    window = LoginWindow()
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()