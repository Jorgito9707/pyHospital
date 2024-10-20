from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QDateEdit, QFormLayout, QDialogButtonBox, QMessageBox, QTextEdit, QTabWidget, QWidget
from PyQt6.QtSql import QSqlQuery

class CrearHistoriaClinica(QDialog):
    """
    Ventana para crear una nueva historia clínica para un paciente determinado y agregarla a la base de datos.
    Se creo a forma de diferentes pestañas para mejorar organización y la legibilidad del texto introducido.
    """

    def __init__(self, id_paciente):
        super().__init__()
        self.id_paciente = id_paciente
        self.setWindowTitle("Crear Historia Clínica")
        self.setupUi()
    
    def setupUi(self):
        layout = QVBoxLayout()
        
        # Crear un widget de pestañas
        self.tab_widget = QTabWidget()
        
        # Pestaña de Motivo de Consulta
        tab1 = QWidget()
        tab1_layout = QVBoxLayout()
        self.descriptionField = QTextEdit()
        tab1_layout.addWidget(self.descriptionField)
        tab1.setLayout(tab1_layout)
        self.tab_widget.addTab(tab1, "Motivo de Consulta")
        
        # Pestaña de Fecha de Consulta
        tab2 = QWidget()
        tab2_layout = QVBoxLayout()
        self.fechaConsultaField = QDateEdit()
        tab2_layout.addWidget(self.fechaConsultaField)
        tab2.setLayout(tab2_layout)
        self.tab_widget.addTab(tab2, "Fecha de Consulta")
        
        # Pestaña de Historia Familiar
        tab3 = QWidget()
        tab3_layout = QVBoxLayout()
        self.familiarHistoryField = QTextEdit()
        tab3_layout.addWidget(self.familiarHistoryField)
        tab3.setLayout(tab3_layout)
        self.tab_widget.addTab(tab3, "Historia Familiar")
        
        # Pestaña de Alergias
        tab4 = QWidget()
        tab4_layout = QVBoxLayout()
        self.alergiesField = QTextEdit()
        tab4_layout.addWidget(self.alergiesField)
        tab4.setLayout(tab4_layout)
        self.tab_widget.addTab(tab4, "Alergias")
        
        # Pestaña de Diagnóstico
        tab5 = QWidget()
        tab5_layout = QVBoxLayout()
        self.diagnosticField = QTextEdit()
        tab5_layout.addWidget(self.diagnosticField)
        tab5.setLayout(tab5_layout)
        self.tab_widget.addTab(tab5, "Diagnóstico")
        
        # Pestaña de Tratamiento
        tab6 = QWidget()
        tab6_layout = QVBoxLayout()
        self.treatmetField = QTextEdit()
        tab6_layout.addWidget(self.treatmetField)
        tab6.setLayout(tab6_layout)
        self.tab_widget.addTab(tab6, "Tratamiento")
        
        # Pestaña de Evolución Clínica
        tab7 = QWidget()
        tab7_layout = QVBoxLayout()
        self.clinicEvolutionField = QTextEdit()
        tab7_layout.addWidget(self.clinicEvolutionField)
        tab7.setLayout(tab7_layout)
        self.tab_widget.addTab(tab7, "Evolución Clínica")
        
        layout.addWidget(self.tab_widget)
        
        # Botones de aceptar y cancelar
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        
        self.setLayout(layout)

    #funciones para conexion de botones --------------------------------------------
    def accept(self):
        description = self.descriptionField.toPlainText()
        fechaConsulta = self.fechaConsultaField.date().toString('dd-MM-yyyy')
        familiarHistory = self.familiarHistoryField.toPlainText()
        alergies = self.alergiesField.toPlainText()
        diagnostic = self.diagnosticField.toPlainText()
        treatmet = self.treatmetField.toPlainText()
        clinicEvolution = self.clinicEvolutionField.toPlainText()

        if description and familiarHistory and alergies and diagnostic and treatmet and clinicEvolution:
            query = QSqlQuery()
            query.prepare("INSERT INTO HISTORIAS_CLINICAS (motivo_consulta, fecha_consulta, historia_familiar, alergias, diagnostico, tratamiento, evolucion_clinica, id_paciente) VALUES (?,?,?,?,?,?,?,?)")
            query.addBindValue(description)
            query.addBindValue(fechaConsulta)
            query.addBindValue(familiarHistory)
            query.addBindValue(alergies)
            query.addBindValue(diagnostic)
            query.addBindValue(treatmet)
            query.addBindValue(clinicEvolution)
            query.addBindValue(self.id_paciente) #relacion con paciente seleccionado a traves de clave foranea

            if query.exec():
                QMessageBox.information(self, "Éxito", "Historia Clínica creada exitosamente.")
                super().accept() 
            else:
                QMessageBox.warning(self, "Error", "No se pudo crear historia clínica.")
        else:
            QMessageBox.warning(self, "Error", "Por favor, rellene todos los campos.")

    def reject(self):
        super().reject()