from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtSql import QSqlQuery
from PyQt6.QtCore import Qt

class AgregarDoctores(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Agregar Doctor")
        self.setupUi()

    def setupUi(self):
        layout = QVBoxLayout()

        # Campos de entrada
        self.nombre_input = QLineEdit()
        self.apellido_input = QLineEdit()
        self.password_input = QLineEdit()
        self.telefono_input = QLineEdit()
        self.email_input = QLineEdit()

        # Diseño de la interfaz
        form_layout = QVBoxLayout()
        form_layout.addWidget(QLabel("Nombre:"))
        form_layout.addWidget(self.nombre_input)
        form_layout.addWidget(QLabel("Apellido:"))
        form_layout.addWidget(self.apellido_input)
        form_layout.addWidget(QLabel("Contraseña:"))
        form_layout.addWidget(self.password_input)
        form_layout.addWidget(QLabel("Teléfono:"))
        form_layout.addWidget(self.telefono_input)
        form_layout.addWidget(QLabel("Email:"))
        form_layout.addWidget(self.email_input)

        layout.addLayout(form_layout)

        # Botones
        button_layout = QHBoxLayout()
        agregar_button = QPushButton("Agregar")
        agregar_button.clicked.connect(self.agregar_doctor)
        cancelar_button = QPushButton("Cancelar")
        cancelar_button.clicked.connect(self.reject)

        button_layout.addWidget(agregar_button)
        button_layout.addWidget(cancelar_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)

    def agregar_doctor(self):
        nombre = self.nombre_input.text()
        apellido = self.apellido_input.text()
        password = self.password_input.text()
        telefono = self.telefono_input.text()
        email = self.email_input.text()

        if not all([nombre, apellido, password, telefono, email]):
            QMessageBox.warning(self, "Error", "Todos los campos son obligatorios")
            return

        query = QSqlQuery()
        query.prepare("""
            INSERT INTO DOCTORES (nombre, apellido, password, telefono, email, administrador)
            VALUES (:nombre, :apellido, :password, :telefono, :email, 0)
        """)
        query.bindValue(":nombre", nombre)
        query.bindValue(":apellido", apellido)
        query.bindValue(":password", password)
        query.bindValue(":telefono", telefono)
        query.bindValue(":email", email)

        if query.exec():
            QMessageBox.information(self, "Éxito", "Doctor agregado correctamente")
            self.accept()
        else:
            QMessageBox.critical(self, "Error", f"No se pudo agregar el doctor: {query.lastError().text()}")