from PyQt6.QtWidgets import (
    QDialog, 
    QVBoxLayout, 
    QHBoxLayout, 
    QPushButton, 
    QTableView, 
    QHeaderView, 
    QMessageBox, 
    QFileDialog, 
    QAbstractItemView
)

from PyQt6.QtSql import QSqlQuery
from PyQt6.QtCore import Qt
import csv

from hospital.dialogWindows.Pacientes.filtro_pacientes import FiltroPacientes
from hospital.model.model import MyModel

class ConsultarPacientesHistoria(QDialog):
    """
    Ventana de dialogo que permite consultar la tabla general de pacientes e historias clínicas, con el nombre de doctor asociado.
    Tambien permite el filtrado de pacientes y el guardado de la información en un archivo CSV.
    """

    def __init__(self, doctor_id):
        super().__init__()
        self.doctor_id = doctor_id
        self.setWindowTitle("Consulta General")
        self.resize(1280, 800)

        self.model = MyModel()
        self.setupUi()

    def setupUi(self):
        layout = QVBoxLayout()
        
        # Crear la tabla
        self.tabla_consulta = QTableView()
        self.tabla_consulta.setModel(self.model)
        layout.addWidget(self.tabla_consulta)

        self.tabla_consulta.setWordWrap(True)  # Permite que el texto se ajuste en varias líneas
        self.tabla_consulta.setTextElideMode(Qt.TextElideMode.ElideNone)  # Evita que el texto se corte con "..."
        self.tabla_consulta.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel) 

        #expandir columnas para llenar espacio disponible de la tabla -------------------------
        horizontal_header = self.tabla_consulta.horizontalHeader()
        horizontal_header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        horizontal_header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive) #modificar manualmente el ancho
        horizontal_header.setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)

        # Ajustar automáticamente la altura de las filas
        self.tabla_consulta.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.tabla_consulta.verticalHeader().setVisible(False)
        
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
            SELECT PACIENTES.id_paciente, PACIENTES.nombre, PACIENTES.apellido, PACIENTES.telefono, PACIENTES.email, PACIENTES.fecha_nacimiento,
                   HISTORIAS_CLINICAS.id_historia_clinica, HISTORIAS_CLINICAS.motivo_consulta, HISTORIAS_CLINICAS.fecha_consulta, HISTORIAS_CLINICAS.historia_familiar,
                   HISTORIAS_CLINICAS.alergias, HISTORIAS_CLINICAS.diagnostico, HISTORIAS_CLINICAS.tratamiento, HISTORIAS_CLINICAS.evolucion_clinica,
                   DOCTORES.nombre AS nombre_doctor, DOCTORES.apellido AS apellido_doctor
                      
            FROM PACIENTES 
            LEFT JOIN HISTORIAS_CLINICAS ON PACIENTES.id_paciente = HISTORIAS_CLINICAS.id_paciente
            LEFT JOIN DOCTORES DOCTORES ON PACIENTES.id_doctor = DOCTORES.id_doctor
                      
            WHERE PACIENTES.id_doctor = :doctor_id
        """)

        query.bindValue(":doctor_id", self.doctor_id)
        query.exec()
        self.model.setQuery(query)

        # Establecer nombres de columnas más descriptivos
        column_names = {
            0: "ID Paciente", 1: "Nombre", 2: "Apellido", 3: "Teléfono", 4: "Email", 5: "Fecha Nacimiento",
            6: "ID Historia", 7: "Motivo Consulta", 8: "Fecha Consulta", 9: "Historia Familiar",
            10: "Alergias", 11: "Diagnóstico", 12: "Tratamiento", 13: "Evolución Clínica",
            14: "Nombre Doctor", 15: "Apellido Doctor"
        }
        
        for i, name in column_names.items():
            self.model.setHeaderData(i, Qt.Orientation.Horizontal, name)

    #metodo para guardar la información en un archivo CSV 
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

    #filtrar pacientes según criterios seleccionados por el usuario 
    def open_filter_dialog(self):
        dialog = FiltroPacientes()
        dialog.filterApplied.connect(self.apply_filters) #aplicar filtros que fueron definidos en la ventana de dialogo de filtros 
        dialog.exec()
    
    def apply_filters(self, filters):
        query = QSqlQuery()
        query_str = """
            SELECT PACIENTES.id_paciente, PACIENTES.nombre, PACIENTES.apellido, 
                PACIENTES.telefono, PACIENTES.email, PACIENTES.fecha_nacimiento,
                HISTORIAS_CLINICAS.id_historia_clinica, HISTORIAS_CLINICAS.motivo_consulta, 
                HISTORIAS_CLINICAS.fecha_consulta, HISTORIAS_CLINICAS.historia_familiar,
                HISTORIAS_CLINICAS.alergias, HISTORIAS_CLINICAS.diagnostico, 
                HISTORIAS_CLINICAS.tratamiento, HISTORIAS_CLINICAS.evolucion_clinica,
                DOCTORES.nombre AS nombre_doctor, DOCTORES.apellido AS apellido_doctor

            FROM PACIENTES

            LEFT JOIN HISTORIAS_CLINICAS ON PACIENTES.id_paciente = HISTORIAS_CLINICAS.id_paciente
            LEFT JOIN DOCTORES ON PACIENTES.id_doctor = DOCTORES.id_doctor

            WHERE PACIENTES.id_doctor = :doctor_id
        """
        
        conditions = []
        #ciclo para crear sentencias sql con cada filtro aplicado
        for key, value in filters.items():
            if value:
                if key == 'id_paciente':
                    conditions.append(f"PACIENTES.{key} = :{key}")
                else:
                    conditions.append(f"PACIENTES.{key} LIKE :{key}")
        
        #crear sentencia general para filtros
        if conditions:
            query_str += " AND " + " AND ".join(conditions)
        
        query.prepare(query_str)
        query.bindValue(":doctor_id", self.doctor_id)
        
        #ciclo para agregar con bindValue cada dato aplicado para filtrar
        for key, value in filters.items():
            if value:
                if key == 'id_paciente':
                    query.bindValue(f":{key}", value)
                else:
                    query.bindValue(f":{key}", f"%{value}%")
        
        if not query.exec():
            QMessageBox.critical(self, "Error", f"Error al aplicar los filtros {query.lastError().text()}")
            print("Error en la consulta:", query.lastError().text())
            return

        self.model.setQuery(query)

        column_names = {
            0: "ID Paciente", 1: "Nombre", 2: "Apellido", 3: "Teléfono", 4: "Email", 5: "Fecha Nacimiento",
            6: "ID Historia", 7: "Motivo Consulta", 8: "Fecha Consulta", 9: "Historia Familiar",
            10: "Alergias", 11: "Diagnóstico", 12: "Tratamiento", 13: "Evolución Clínica",
            14: "Nombre Doctor", 15: "Apellido Doctor"
        }
        
        for i, name in column_names.items():
            self.model.setHeaderData(i, Qt.Orientation.Horizontal, name)

        self.tabla_consulta.reset()
        self.tabla_consulta.resizeColumnsToContents()