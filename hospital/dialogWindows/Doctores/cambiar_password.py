from PyQt6.QtWidgets import QLineEdit, QDialog, QFormLayout, QDialogButtonBox, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtSql import QSqlQuery

class CambiarContraseña(QDialog):
    def __init__(self, doctor_id, parent=None):
        super().__init__()
        self.doctor_id = doctor_id

        self.setWindowTitle("Cambiar Contraseña")
        self.setupUi()
    
    def setupUi(self):
        layout = QFormLayout(self)

        self.new_password = QLineEdit(self)
        self.new_password.setPlaceholderText("Nueva contraseña")
        self.new_password.setEchoMode(QLineEdit.EchoMode.Password)

        layout.addRow("Nueva contraseña:", self.new_password)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel,
            Qt.Orientation.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addRow(buttons)

    def accept(self):
        new_password = self.new_password.text()

        if new_password:
            if self.update_password(new_password):
                super().accept()
                QMessageBox.information(self, "Éxito", "Contraseña actualizada correctamente.")
            else:
                QMessageBox.warning(self, "Error", "No se pudo actualizar la contraseña.")
        else:
            QMessageBox.warning(self, "Error", "Por favor, ingrese una nueva contraseña.")

    def update_password(self, new_password):
        query = QSqlQuery()
        query.prepare("UPDATE DOCTORES SET password=? WHERE id_doctor=?")
        query.addBindValue(new_password)
        query.addBindValue(self.doctor_id)

        return query.exec()