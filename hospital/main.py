from PyQt6.QtWidgets import QApplication, QMessageBox

from hospital.autentication import AutenticationWindow
from hospital.database.database import crear_conexion
import sys

def main():
    app = QApplication(sys.argv)
    
    # Establecer conexión a la base de datos
    if not crear_conexion("salud.sqlite"):
        QMessageBox.critical(None, "Error", "No se pudo conectar a la base de datos.")
        sys.exit(1)
    
    # Mostrar la ventana de autenticación al inicio del programa
    auth_window = AutenticationWindow()
    auth_window.show()
    
    sys.exit(app.exec())