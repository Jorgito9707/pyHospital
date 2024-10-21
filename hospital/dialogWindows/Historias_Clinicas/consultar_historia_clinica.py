from PyQt6.QtWidgets import (
    QDialog, 
    QVBoxLayout, 
    QHBoxLayout, 
    QPushButton, 
    QTableView, 
    QHeaderView, 
    QMessageBox
)

from PyQt6.QtSql import QSqlQuery
from PyQt6.QtCore import Qt

from hospital.dialogWindows.Historias_Clinicas.crear_historia_clinica import CrearHistoriaClinica
from hospital.model.model import MyModel

class ConsultarHistoriaClinica(QDialog):
    """
    Permite consultar y administrar las historias clínicas de un paciente seleccionado.
    Un mismo paciente puede tener varias historias clínicas.
    """

    def __init__(self, paciente_id):
        super().__init__()
        self.paciente_id = paciente_id
        self.setWindowTitle("Consultar Historia Clínica")
        self.resize(1280, 800)

        self.model = MyModel()
        self.model.setTable("HISTORIAS_CLINICAS")
        self.selected_row = None
        self.setupUi()
        self.cargar_datos()

    def setupUi(self):
        layout = QVBoxLayout()
        
        # Crear la tabla
        self.tabla_historia = QTableView()
        self.tabla_historia.setModel(self.model)
        layout.addWidget(self.tabla_historia)

        self.tabla_historia.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.tabla_historia.setSelectionMode(QTableView.SelectionMode.SingleSelection)
        self.tabla_historia.verticalHeader().setVisible(False) 

        #expandir columnas para llenar espacio disponible de la tabla -------------------------
        self.tabla_historia.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # habilitar edicion de la tabla por doble click o presionar la tecla enter ----------
        self.tabla_historia.setEditTriggers(QTableView.EditTrigger.DoubleClicked | QTableView.EditTrigger.EditKeyPressed)
        
        # Botones
        button_layout = QHBoxLayout()
        self.btn_crear = QPushButton("Crear Historia")
        self.btn_crear.clicked.connect(self.crear_historia_clinica)
        button_layout.addWidget(self.btn_crear)
        
        self.btn_eliminar = QPushButton("Eliminar Historia")
        self.btn_eliminar.clicked.connect(self.delete_clinnical_record)
        button_layout.addWidget(self.btn_eliminar)
        
        self.btn_cerrar = QPushButton("Cerrar")
        self.btn_cerrar.clicked.connect(self.close_table)
        button_layout.addWidget(self.btn_cerrar)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
        # Conectar la selección de fila
        self.tabla_historia.selectionModel().selectionChanged.connect(self.select_row)

    def select_row(self, selected, deselected):
        if selected.indexes():
            self.selected_row = selected.indexes()[0].row()
        else:
            self.selected_row = None 

    def cargar_datos(self):
        self.model.setFilter(f"id_paciente = {self.paciente_id}")
        self.model.select()
        
        self.tabla_historia.hideColumn(self.model.fieldIndex("id_paciente"))
        self.tabla_historia.resizeColumnsToContents()

        column_names = {
            "id_historia_clinica": "ID",
            "motivo_consulta": "Motivo de Consulta",
            "fecha_consulta": "Fecha",
            "historia_familiar": "Historia Familiar",
            "alergias": "Alergias",
            "diagnostico": "Diagnóstico",
            "tratamiento": "Tratamiento",
            "evolucion_clinica": "Evolución Clínica",
        }

        #mejorar la visibilidad del encabezado de la tabla --------
        for column, name in column_names.items():
            self.model.setHeaderData(self.model.fieldIndex(column), Qt.Orientation.Horizontal, name)

        #reajustar el tamaño de las columnas para adaptarse al contenido ---------------------------------
        self.tabla_historia.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
    
    def crear_historia_clinica(self):
        dialog = CrearHistoriaClinica(self.paciente_id)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.cargar_datos() 
    
    def delete_clinnical_record(self):
        if self.selected_row is not None:
            id_historia_clinica = self.model.record(self.selected_row).value("id_historia_clinica")
            self.remove_clinnical_record(id_historia_clinica)
        else:
            QMessageBox.warning(self, "Advertencia", "No has seleccionado ninguna fila")      

    def remove_clinnical_record(self, id_hisotria_clinica):
        query = QSqlQuery()
        query.prepare("DELETE FROM HISTORIAS_CLINICAS WHERE id_historia_clinica = ?")
        query.addBindValue(id_hisotria_clinica)
        if query.exec():
            self.cargar_datos()  # Actualizar la tabla
            QMessageBox.information(self, "Éxito", "Historia clínica eliminada correctamente")
        else:
            QMessageBox.warning(self, "Advertencia", f"La historia clínica con ID: {id_hisotria_clinica}, no existe")

    def close_table(self):
        self.close()