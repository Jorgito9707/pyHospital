from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QDialogButtonBox, QMessageBox
from PyQt6.QtSql import QSqlQuery
class FiltroPacientes(QDialog):
    """
    Ventana de diálogo que permite al usuario ingresar filtros para buscar pacientes.
    """

    def __init__(self, doctor_id):
        super().__init__()
        self.doctor_id = doctor_id
        self.setWindowTitle("Filtrar Pacientes")
        self.setupUi()

    def setupUi(self):
        layout = QVBoxLayout()

        # Campo para ID
        id_layout = QHBoxLayout()
        id_layout.addWidget(QLabel("ID:"))
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
            "id": self.IdField.text(),
            "nombre": self.nombre_searchField.text(),
            "apellido": self.apellido_searchField.text()
        }
    
    def accept(self):
        filters = self.get_filters()
        query = self.build_query(filters)
        
        if query.exec() and query.next():
            super().accept()
        else:
            QMessageBox.information(self, "Sin resultados", "No se encontraron pacientes que coincidan con los criterios de búsqueda.")

    def build_query(self, filters):
        query = QSqlQuery()
        query_str = """
            SELECT PACIENTES.id_paciente, PACIENTES.nombre, PACIENTES.apellido, PACIENTES.telefono, PACIENTES.email, PACIENTES.fecha_nacimiento,
                   HISTORIAS_CLINICAS.id_historia_clinica, HISTORIAS_CLINICAS.motivo_consulta, HISTORIAS_CLINICAS.fecha_consulta, HISTORIAS_CLINICAS.historia_familiar,
                   HISTORIAS_CLINICAS.alergias, HISTORIAS_CLINICAS.diagnostico, HISTORIAS_CLINICAS.tratamiento, HISTORIAS_CLINICAS.evolucion_clinica,
                   DOCTORES.nombre AS nombre_doctor, DOCTORES.apellido AS apellido_doctor

            FROM PACIENTES 
            LEFT JOIN HISTORIAS_CLINICAS ON PACIENTES.id_paciente = HISTORIAS_CLINICAS.id_paciente
            LEFT JOIN DOCTORES ON PACIENTES.id_doctor = DOCTORES.id_doctor

            WHERE PACIENTES.id_doctor = :doctor_id
        """

        conditions = []
        if filters['id']:
            conditions.append("PACIENTES.id_paciente = :id")
        if filters['nombre']:
            conditions.append("PACIENTES.nombre LIKE :nombre")
        if filters['apellido']:
            conditions.append("PACIENTES.apellido LIKE :apellido")

        if conditions:
            query_str += " AND " + " AND ".join(conditions)

        query.prepare(query_str)
        query.bindValue(":doctor_id", self.doctor_id)
        if filters['id']:
            query.bindValue(":id", filters['id'])
        if filters['nombre']:
            query.bindValue(":nombre", f"%{filters['nombre']}%")
        if filters['apellido']:
            query.bindValue(":apellido", f"%{filters['apellido']}%")

        return query
