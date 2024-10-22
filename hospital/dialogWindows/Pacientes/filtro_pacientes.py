from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QDialogButtonBox, QMessageBox
from PyQt6.QtSql import QSqlQuery
from PyQt6.QtCore import pyqtSignal

class FiltroPacientes(QDialog):
    """
    Ventana de diálogo que permite al usuario ingresar filtros para buscar pacientes.
    """
    filterApplied = pyqtSignal(dict) #señal que va a indicar cuando se aplica el filtro 

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Filtrar Pacientes")
        self.setupUi()

    def setupUi(self):
        layout = QVBoxLayout()

        # Campo para ID
        id_layout = QHBoxLayout()
        id_layout.addWidget(QLabel("Id Paciente:"))
        self.IdField = QLineEdit()
        id_layout.addWidget(self.IdField)
        layout.addLayout(id_layout)

        # Campo para Nombre
        nombre_layout = QHBoxLayout()
        nombre_layout.addWidget(QLabel("Nombre:"))
        self.nombre_searchField = QLineEdit()
        nombre_layout.addWidget(self.nombre_searchField)
        layout.addLayout(nombre_layout)

        # Campo para Apellido
        apellido_layout = QHBoxLayout()
        apellido_layout.addWidget(QLabel("Apellido:"))
        self.apellido_searchField = QLineEdit()
        apellido_layout.addWidget(self.apellido_searchField)
        layout.addLayout(apellido_layout)

        # Botones de aceptar y cancelar
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self.setLayout(layout)

    def get_filters(self):
        return {
            "id_paciente": self.IdField.text(),
            "nombre": self.nombre_searchField.text(),
            "apellido": self.apellido_searchField.text()
        }
    
    def accept(self):
        filters = self.get_filters()
        self.filterApplied.emit(filters) #emitir los filtros aplicados, valores de campos
        super().accept()