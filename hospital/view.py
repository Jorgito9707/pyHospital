from PyQt6.QtWidgets import (
    QMainWindow, 
    QWidget, 
    QVBoxLayout, 
    QHBoxLayout, 
    QPushButton, 
    QTableView, 
    QHeaderView, 
    QStatusBar, 
    QMessageBox, 
    QSpacerItem, 
    QSizePolicy)

from PyQt6.QtCore import Qt, QEvent
from PyQt6.QtSql import QSqlQuery
from hospital.model.model import MyModel
from hospital.dialogWindows.Pacientes.agregar_pacientes import AgregarPacientes
from hospital.dialogWindows.Historias_Clinicas.crear_historia_clinica import CrearHistoriaClinica
from hospital.dialogWindows.Historias_Clinicas.consultar_historia_clinica import ConsultarHistoriaClinica
from hospital.dialogWindows.consulta_general import ConsultarPacientesHistoria
from hospital.dialogWindows.Doctores.tabla_doctores import TablaDoctores
from hospital.dialogWindows.Doctores.cambiar_password import CambiarContraseña

class MainWindow(QMainWindow):
    def __init__(self, doctor_id, nombre, apellido, es_admin):
        super().__init__()
        self.doctor_id = doctor_id
        self.nombre = nombre
        self.apellido = apellido
        self.es_admin = es_admin.lower() == 'true' #almaceno resultado de comparacion -> conversion a booleano
        
        self.setWindowTitle("Sistema de Gestión Hospitalaria")
        self.resize(1280, 800)

        # Configurar la barra de estado -----------
        self.myStatusBar = QStatusBar()
        self.setStatusBar(self.myStatusBar)
        self.myStatusBar.showMessage(f"Hola, Dr. {self.nombre} {self.apellido}")

        self.setupUi()

    def setupUi(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)

        # Layout izquierdo para la tabla
        left_layout = QVBoxLayout()
        main_layout.addLayout(left_layout)

        # Configuracion de la Tabla de pacientes -------
        self.table_view = QTableView()
        self.model = MyModel()
        self.model.setTable("PACIENTES")
        self.model.setFilter(f"id_doctor = {self.doctor_id}")
        self.model.select()
        self.table_view.setModel(self.model)

        self.setHeaderNames()

        #ocultar campo ID Doctor de la tabla pacientes ----------
        id_doctor_column = self.model.fieldIndex("id_doctor")
        self.table_view.setColumnHidden(id_doctor_column, True)
        
        #expandir columnas para llenar espacio disponible de la tabla -------------------------
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # habilitar edicion de la tabla por doble click o presionar la tecla enter ----------
        self.table_view.setEditTriggers(QTableView.EditTrigger.DoubleClicked | QTableView.EditTrigger.EditKeyPressed)

        #establecer comportamiento al seleccionar elementos ---------------------------------
        self.table_view.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.table_view.setSelectionMode(QTableView.SelectionMode.SingleSelection)
        self.table_view.verticalHeader().setVisible(False)
        
        left_layout.addWidget(self.table_view)

        # Conectar la señal de cambio de datos al método de actualización
        self.model.dataChanged.connect(self.actualizar_base_de_datos)

        # Layout derecho para los botones de la interfaz -----------------
        right_layout = QVBoxLayout()
        main_layout.addLayout(right_layout)

        # Botones para diferentes funcionalidades ----------------------------------
        self.add_button(right_layout, "Agregar Paciente", self.open_add_patient)
        self.delete_patient_button = self.add_button(right_layout, "Eliminar Paciente", self.delete_patient)
        self.consult_history_button = self.add_button(right_layout, "Historia Clínica", self.open_consult_clinical_history)
        self.add_button(right_layout, "Consulta General", self.open_general_consultation)

        #modificar la contraseña de cualquier doctor ----------------------------
        self.add_button(right_layout, "Cambiar Contraseña", self.open_change_password)

        # Agregar un spacer para empujar los botones hacia arriba
        spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        right_layout.addItem(spacer)

        # Botón para gestionar doctores (solo para administradores) --------------
        self.manage_doctors_button = self.add_button(right_layout, "Gestionar Doctores", self.open_manage_doctors)
        self.manage_doctors_button.setEnabled(self.es_admin)

        # Botón para eliminar todos los pacientes del doctor y cerrar sesión ------
        self.delete_all_button = self.add_button(right_layout, "Eliminar Todo", self.delete_all_patients)
        self.add_button(right_layout, "Cerrar Sesión", self.logout)

        # Actualizar estado de botones al seleleccionar -----------------------------
        self.table_view.selectionModel().selectionChanged.connect(self.update_buttons)

        # Llamar funcion que maneja estado de botones al seleccionar una fila
        self.update_buttons()

        # Instalar el filtro de eventos en el viewport de la tabla
        #todos los eventos que ocurran en el viewport de la tabla serán interceptados por el metodo eventFilter
        self.table_view.viewport().installEventFilter(self)

    #Metodo que permite agregar botones a la interfaz
    def add_button(self, layout, text, slot):
        button = QPushButton(text)
        button.clicked.connect(slot)
        button.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed) #politica de tamaño en horizontal, vertical
        layout.addWidget(button)
        return button 
    
    #Habilita o deshabilita botones según el estado de la selección
    def update_buttons(self):
        selected = len(self.table_view.selectionModel().selectedRows()) > 0
        self.delete_patient_button.setEnabled(selected)
        self.consult_history_button.setEnabled(selected)

    #QPushButton ===================================================>
    #Eliminar todos los pacientes del doctor --------
    def delete_all_patients(self):
        mensaje_confirmacion = QMessageBox.question(
            self, 
            'Confirmar eliminación', 
            '¿Estás seguro de que quieres eliminar todos tus pacientes?', 
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if mensaje_confirmacion == QMessageBox.StandardButton.Yes:
            query = QSqlQuery()
            query.prepare(f"DELETE FROM PACIENTES WHERE id_doctor = {self.doctor_id}")
            if query.exec():
                self.model.select()
                QMessageBox.information(self, "Eliminación exitosa", "Todos los pacientes han sido eliminados correctamente")
            else:
                QMessageBox.warning(self, "Error", "No se pudieron eliminar los pacientes")
    
    def open_change_password(self):
        dialog = CambiarContraseña(self.doctor_id)
        dialog.exec()

    def open_consult_clinical_history(self):
        selected = self.table_view.selectionModel().selectedRows() #lista de elementos seleccionados
        if selected:
            #obtener id del paciente seleccionado ------
            patient_id = self.model.data(self.model.index(selected[0].row(), 0))
            dialog = ConsultarHistoriaClinica(patient_id)
            dialog.exec()
        else:
            QMessageBox.warning(self, "Advertencia", "Por favor, seleccione un paciente primero.")

    def delete_patient(self):
        selected = self.table_view.selectionModel().selectedRows()
        if selected:
            patient_id = self.model.data(self.model.index(selected[0].row(), 0))
            reply = QMessageBox.question(
                self, 
                'Confirmar eliminación', 
                '¿Estás seguro de que quieres eliminar este paciente?', 
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            
            if reply == QMessageBox.StandardButton.Yes:
                query = QSqlQuery()
                query.prepare("DELETE FROM PACIENTES WHERE id_paciente = ?")
                query.addBindValue(patient_id)
                if query.exec():
                    self.model.select()
                    QMessageBox.information(self, "Eliminación exitosa", "El paciente ha sido eliminado correctamente")
                else:
                    QMessageBox.warning(self, "Error", "No se pudo eliminar el paciente")

    def actualizar_base_de_datos(self):
        if self.model.submitAll():
            QMessageBox.information(self, "Actualización exitosa", "Los datos han sido actualizados correctamente")
        else:
            QMessageBox.warning(self, "Error", "No se pudieron actualizar los datos: " + self.model.lastError().text())

    def open_add_patient(self):
        dialog = AgregarPacientes(self.doctor_id)
        if dialog.exec():
            self.model.select()  # Actualizar la tabla después de agregar

    def open_create_clinical_history(self):
        dialog = CrearHistoriaClinica(self.doctor_id)
        dialog.exec()

    def open_general_consultation(self):
        dialog = ConsultarPacientesHistoria(self.doctor_id)
        dialog.exec()

    def open_manage_doctors(self):
        if self.es_admin:
            dialog = TablaDoctores()
            dialog.exec()
        else:
            QMessageBox.warning(self, "Acceso Denegado", "No tienes permisos de administrador.")

    def logout(self):
        self.close()
        from hospital.autentication import AutenticationWindow
        self.auth_window = AutenticationWindow()
        self.auth_window.show()

    #Metodo que maneja el evento interceptado
    def eventFilter(self, source, event):
        #source -> objeto que genero el evento
        #event -> evento que generó la señal
        #si el evento es hacer click y la fuente es el viewport de la tabala, limpia la seleccion de la misma
        if (event.type() == QEvent.Type.MouseButtonPress and source is self.table_view.viewport()):
            index = self.table_view.indexAt(event.pos())
            if not index.isValid(): #si el indice no es valido es xq no hay una celda seleccionada
                self.table_view.clearSelection()
                self.update_buttons()
                return True
        return super().eventFilter(source, event) #pasar evenFilter al padre
    
    #funcion que permite mostrar los encabezados de la tabla como yo quiero
    def setHeaderNames(self):
        column_names = {
            "id_paciente": "ID",
            "nombre": "Nombre",
            "apellido": "Apellido",
            "telefono": "Teléfono",
            "email": "Correo Electrónico",
            "fecha_nacimiento": "Fecha de Nacimiento",
        }

        for column, name in column_names.items():
            self.model.setHeaderData(self.model.fieldIndex(column), Qt.Orientation.Horizontal, name)