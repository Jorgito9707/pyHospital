from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLineEdit, QPushButton, QMessageBox, QDialog
from PyQt6.QtGui import QIcon
from PyQt6.QtSql import QSqlQuery
from hospital.view import MainWindow

import os

class AutenticationWindow(QWidget):
    """
    Clase que representa la ventana de autenticación. Contiene dos campos de entrada (nombre de usuario y contraseña),
    un botón para iniciar sesión y un layout vertical para acomodar los elementos.
    """

    def __init__(self):
        super().__init__()
        self.file_path = os.path.dirname(os.path.abspath(__file__)) #fichero padre

        self.setWindowTitle("Autenticación")
        self.resize(300, 200)

        self.setupUi()
    
    def setupUi(self):
        layout = QVBoxLayout()

        self.name_field = QLineEdit()
        self.name_field.setPlaceholderText("Nombre de usuario")
        layout.addWidget(self.name_field)

        #contraseña y boton ocultar/mostrar ---
        password_layout = QHBoxLayout()

        self.password_field = QLineEdit()
        self.password_field.setPlaceholderText("Contraseña")
        self.password_field.setEchoMode(QLineEdit.EchoMode.Password)
        password_layout.addWidget(self.password_field)

        #boton mostrar ocultar contraseña -----
        self.toggle_password_button = QPushButton()
        #self.toggle_password_button.setFixedSize(30, 30)
        self.toggle_password_button.clicked.connect(self.toggle_password_visibility)
        icon_path = os.path.join(self.file_path, '.', 'images', 'ojo_abierto.png')
        self.toggle_password_button.setIcon(QIcon(icon_path))

        password_layout.addWidget(self.toggle_password_button)

        layout.addLayout(password_layout)

        #boton para iniciar sesión ---
        login_button = QPushButton("Iniciar sesión")
        login_button.clicked.connect(self.autenticar)
        layout.addWidget(login_button)

        self.setLayout(layout)
        self.apply_styles()

    def autenticar(self):
        nombre = self.name_field.text()
        clave = self.password_field.text()
        
        query = QSqlQuery()

        # Consulta a la base de datos para comprobar existencia del doctor específico
        query.prepare("SELECT * FROM DOCTORES WHERE nombre=? AND password=?")
        query.addBindValue(nombre)
        query.addBindValue(clave)
        
        if query.exec() and query.next():
            doctor_id = query.value(0)  # el id es la primera columna
            doctor_lastName = query.value(2) # apellido
            doctor_admin = query.value(6) # permiso de administrador
            
            # Le paso el id y el nombre del doctor que inició la sesión
            self.ventana_principal = MainWindow(doctor_id, nombre, doctor_lastName, doctor_admin)
            self.ventana_principal.show()
            
            self.close()
        else:
            QMessageBox.warning(self, "Error", "Credenciales incorrectas")

    #meotodo para mostrar/ocultar la contraseña al presionar el botón
    def toggle_password_visibility(self):
        if self.password_field.echoMode() == QLineEdit.EchoMode.Password:
            icon_path = os.path.join(self.file_path, '.', 'images', 'ojo_cerrado.png')
            self.toggle_password_button.setIcon(QIcon(icon_path))

            self.password_field.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            icon_path = os.path.join(self.file_path, '.', 'images', 'ojo_abierto.png')
            self.toggle_password_button.setIcon(QIcon(icon_path))
            self.password_field.setEchoMode(QLineEdit.EchoMode.Password)
    
    def apply_styles(self):
        self.setStyleSheet("""
            QWidget {
                font-size: 14px;
            }
                           
            QLineEdit {
                padding: 5px;
                margin-bottom: 10px;
                border: 1px solid #ccc;
                border-radius: 4px;
            }
                           
            QPushButton {
                padding: 8px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 4px;
            }
                           
            QPushButton:hover {
                background-color: #45a049;
            }
                           
            #toggle_password_button {
                background-color: #4CAF50;
                border: 1px solid #000;
                border-radius: 4px;
                margin-left: 5px;
            }
                           
            #toggle_password_button:hover {
            b   ackground-color: #e0e0e0;
            }
        """)
        self.toggle_password_button.setObjectName("toggle_password_button")