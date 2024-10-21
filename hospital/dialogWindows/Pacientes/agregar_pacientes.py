from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QDateEdit, QFormLayout, QDialogButtonBox, QMessageBox, QSpacerItem, QSizePolicy
from PyQt6.QtSql import QSqlQuery

class AgregarPacientes(QDialog):
    """
    Ventana de dialogo para agregar un nuevo paciente al sistema.
    Contiene los campos necesarios para ello.
    """
        
    def __init__(self, doctor_id):
        super().__init__()
        self.doctor_id = doctor_id
        self.setWindowTitle("Agregar Nuevo Paciente")
        self.setupUi()

    def setupUi(self):
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        self.nameField = QLineEdit()
        form_layout.addRow("Nombre:", self.nameField)

        self.lastNameField = QLineEdit()
        form_layout.addRow("Apellido:", self.lastNameField)

        self.telephoneField = QLineEdit()
        form_layout.addRow("Teléfono:", self.telephoneField)

        self.emailField = QLineEdit()
        form_layout.addRow("Email:", self.emailField)

        self.dateField = QDateEdit()
        self.dateField.setCalendarPopup(True)
        form_layout.addRow("Fecha de Nacimiento:", self.dateField)

        layout.addLayout(form_layout)

        #agregar un spacer para separar los botones del resto de formulario
        spacer = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        layout.addItem(spacer)

        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

        self.setLayout(layout)

    #metodos de botones --------------------------------------------
    def accept(self):
        nombre = self.nameField.text()
        apellido = self.lastNameField.text()
        telefono = self.telephoneField.text()
        email = self.emailField.text()
        date = self.dateField.date().toString('dd-MM-yyyy')
        
        if nombre and apellido and date:
            query = QSqlQuery()
            query.prepare("INSERT INTO PACIENTES (nombre, apellido, telefono, email, fecha_nacimiento, id_doctor) VALUES (?, ?, ?, ?, ?, ?)")
            query.addBindValue(nombre)
            query.addBindValue(apellido)
            query.addBindValue(telefono)
            query.addBindValue(email)
            query.addBindValue(date)
            query.addBindValue(self.doctor_id) #id del doctor que ya tiene sesion iniciada

            if query.exec():
                QMessageBox.information(self, "Éxito", "Paciente agregado exitosamente.")
                super().accept()  # Cierra el diálogo
            else:
                QMessageBox.warning(self, "Error", "No se pudo agregar el paciente.")
        else:
            QMessageBox.warning(self, "Error", "Por favor, rellene los campos necesarios.")
    
    def reject(self):
        super().reject()