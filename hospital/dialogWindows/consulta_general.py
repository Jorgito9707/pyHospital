from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QTableView, QHeaderView, QMessageBox, QFileDialog
from PyQt6.QtSql import QSqlTableModel, QSqlQuery
from PyQt6.QtCore import Qt
import csv

from hospital.dialogWindows.Pacientes.filtro_pacientes import FiltroPacientes

class ConsultarPacientesHistoria(QDialog):
    """
    Ventana de dialogo que permite consultar la tabla general de pacientes e historias clínicas, con el nombre de doctor asociado.
    Tambien permite el filtrado de pacientes y el guardado de la información en un archivo CSV.
    """

    def __init__(self, doctor_id):
        super().__init__()
        self.doctor_id = doctor_id
        self.setWindowTitle("Consulta General")
        self.model = QSqlTableModel()
        self.setupUi()

    def setupUi(self):
        layout = QVBoxLayout()
        
        # Crear la tabla
        self.tabla_consulta = QTableView()
        self.tabla_consulta.setModel(self.model)
        layout.addWidget(self.tabla_consulta)
        
        # Botones
        button_layout = QHBoxLayout()
        
        self.btn_filtrar = QPushButton("Filtrar")
        self.btn_filtrar.clicked.connect(self.open_filter_dialog)
        button_layout.addWidget(self.btn_filtrar)
        
        self.btn_guardar = QPushButton("Guardar")
        self.btn_guardar.clicked.connect(self.guardar_archivo)
        button_layout.addWidget(self.btn_guardar)
        
        self.btn_cerrar = QPushButton("Cerrar")
        self.btn_cerrar.clicked.connect(self.close)
        button_layout.addWidget(self.btn_cerrar)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
        self.actualizar_tabla()

    def actualizar_tabla(self):
        query = QSqlQuery()
        query.prepare("""
            SELECT p.id_paciente, p.nombre, p.apellido, p.telefono, p.email, p.fecha_nacimiento,
                   h.id_historia_clinica, h.motivo_consulta, h.fecha_consulta, h.historia_familiar,
                   h.alergias, h.diagnostico, h.tratamiento, h.evolucion_clinica,
                   d.nombre AS nombre_doctor, d.apellido AS apellido_doctor
            FROM PACIENTES p
            LEFT JOIN HISTORIAS_CLINICAS h ON p.id_paciente = h.id_paciente
            LEFT JOIN DOCTORES d ON p.id_doctor = d.id_doctor
            WHERE p.id_doctor = :doctor_id
        """)
        query.bindValue(":doctor_id", self.doctor_id)
        query.exec()
        self.model.setQuery(query)

    def guardar_archivo(self):
        file_name = QFileDialog.getSaveFileName(self, "Guardar Archivo", "", "CSV (*.csv)")[0] #la posicion 0 es el archivo seleccionado por el usuario
        if file_name:
            with open(file_name, "w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                headers = [self.model.headerData(i, Qt.Orientation.Horizontal) for i in range(self.model.columnCount())]

                # escribir encabezados -----
                writer.writerow(headers) 

                #almacenar datos de la tabla ---------------------------------
                for row in range(self.model.rowCount()):
                    for column in range(self.model.columnCount()):
                        writer.writerow([self.model.index(row, column).data()])
            
            QMessageBox.information(self, "Información", "Archivo guardado correctamente")

    def open_filter_dialog(self):
        dialog = FiltroPacientes(self.doctor_id)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # Actualizar la tabla con los resultados del filtro
            self.actualizar_tabla()