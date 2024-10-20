from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QTableView, QPushButton, QMessageBox, QHeaderView
from PyQt6.QtSql import QSqlTableModel, QSqlQuery
from PyQt6.QtCore import Qt
from hospital.dialogWindows.Doctores.agregar_doctores import AgregarDoctores

class TablaDoctores(QDialog):
    """
    Tabla que muestra la lista de doctores en la base de datos.
    Permite modificar valores de los doctores y eliminarlos de la base de datos.
    Solo tienen acceso a ella los doctores que son administradores.
    """
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Doctores")
        self.resize(1000, 700)

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        
        self.model = QSqlTableModel()
        self.model.setTable("DOCTORES")
        self.model.setEditStrategy(QSqlTableModel.EditStrategy.OnFieldChange)
        
        self.selected_row = None
        
        #cargar interfaz de usuario ----
        self.setupUi()

        #actualizar la tabla de doctores segun la base de datos
        self.cargar_doctores()
    
    def setupUi(self):
        # Crear la tabla
        self.tabla_doctores = QTableView()
        self.tabla_doctores.setModel(self.model)
        self.tabla_doctores.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.tabla_doctores.setSelectionMode(QTableView.SelectionMode.SingleSelection)
        self.main_layout.addWidget(self.tabla_doctores)
        
        # Botones
        button_layout = QHBoxLayout()
        
        self.btn_agregar = QPushButton("Agregar Doctor")
        self.btn_agregar.clicked.connect(self.add_doctor_toDb)
        button_layout.addWidget(self.btn_agregar)
        
        self.btn_eliminar = QPushButton("Eliminar Doctor")
        self.btn_eliminar.clicked.connect(self.delete_doctor_from_db)
        button_layout.addWidget(self.btn_eliminar)
        
        self.btn_cerrar = QPushButton("Cerrar")
        self.btn_cerrar.clicked.connect(self.close_table)
        button_layout.addWidget(self.btn_cerrar)
        
        self.main_layout.addLayout(button_layout)
        
        # Conectar la selección de fila
        self.tabla_doctores.selectionModel().selectionChanged.connect(self.select_row)
    
    def cargar_doctores(self):
        """
        Método que se ejecuta para actualizar la lista de doctores.
        Se obtiene de la base de datos y para poder acceder hay que tener permiso de administrador
        """
        self.model.select() #actualizar la tabla con los datos obtenidos
        self.tabla_doctores.resizeColumnsToContents()

        column_names = {
            "id_doctor": "ID",
            "nombre": "Nombre",
            "apellido": "Apellido",
            "password": "Contraseña",
            "telefono": "Teléfono",
            "email": "Correo Electrónico",
            "administrador": "Privilegio Administrador"
        }

        for column, name in column_names.items():
            self.model.setHeaderData(self.model.fieldIndex(column), Qt.Orientation.Horizontal, name)

    #accion a realizar cuando se seleccione una fila ----
    def select_row(self, selected, deselected):
        if selected.indexes():
            self.selected_row = selected.indexes()[0].row()
        else:
            self.selected_row = None 

    #funciones para botones ---------------------------
    def delete_doctor_from_db(self):
        if self.selected_row is not None:
            doctor_id = self.model.record(self.selected_row).value("id_doctor")
            self.remove_doctor(doctor_id)
        else:
            QMessageBox.warning(self, "Advertencia", "No has seleccionado ninguna fila")        

    def remove_doctor(self, doctor_id):
        query = QSqlQuery()
        query.prepare("DELETE FROM DOCTORES WHERE id_doctor = ?")
        query.addBindValue(doctor_id)
        if query.exec():
            self.cargar_doctores()  # Actualizar la tabla
            QMessageBox.information(self, "Éxito", "Doctor eliminado correctamente")
        else:
            QMessageBox.warning(self, "Advertencia", f"El doctor con ID: {doctor_id}, no existe") 
            
    def add_doctor_toDb(self):
        dialog = AgregarDoctores()
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.cargar_doctores()
    
    def close_table(self):
        self.close()