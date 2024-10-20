from PyQt6.QtSql import QSqlTableModel
from PyQt6.QtCore import Qt

class MyModel(QSqlTableModel):
    """
    -Modelo propio que hereda de QSqlTableModel para mostrar datos de una tabla MySQL.
    -Este modelo puede ser utilizado en cualquier QTableView o QTableWidget.
    -Permite modificar los flags de cada celda en función de las necesidades de la tabla.
    -No permite la edición de la primera columna, que suele ser la de identificacion (en mi caso se genera automaticamente).
    """

    def flags(self, index): #modificar flags para la tabla
        flags = super().flags(index)
        if index.column() == 0:  # Primera columna (ID)
            flags &= ~Qt.ItemFlag.ItemIsEditable  # Deshabilitar edición
        else:
            flags |= Qt.ItemFlag.ItemIsEditable  # Habilitar edición
        return flags