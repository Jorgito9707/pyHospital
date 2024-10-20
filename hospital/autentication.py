from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QMessageBox, QDialog
from PyQt6.QtSql import QSqlQuery
from hospital.view import MainWindow

class AutenticationWindow(QWidget):
    """
    Clase que representa la ventana de autenticación. Contiene dos campos de entrada (nombre de usuario y contraseña),
    un botón para iniciar sesión y un layout vertical para acomodar los elementos.
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Autenticación")
        self.resize(300, 200)

        self.setupUi()
    
    def setupUi(self):
        layout = QVBoxLayout()

        self.name_field = QLineEdit()
        self.name_field.setPlaceholderText("Nombre de usuario")
        layout.addWidget(self.name_field)

        self.password_field = QLineEdit()
        self.password_field.setPlaceholderText("Contraseña")
        self.password_field.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_field)

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

    def toggle_password_visibility(self):
        if self.password_field.echoMode() == QLineEdit.EchoMode.Password:
            self.password_field.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.password_field.setEchoMode(QLineEdit.EchoMode.Password)
    
    def apply_styles(self):
        self.setStyleSheet("""
            QWidget {
                font-size: 14px;
            }
            QLineEdit {
                padding: 5px;
                margin-bottom: 10px;
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
        """)