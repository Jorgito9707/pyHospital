from PyQt6.QtSql import QSqlDatabase, QSqlQuery
from PyQt6.QtWidgets import QMessageBox

def crear_conexion(nombre_db):
    """
    Crea una conexión a la base de datos SQLite.
    
    Args:
    nombre_db (str): Nombre del archivo de la base de datos SQLite.

    Returns:
    bool: True si la conexión se estableció correctamente, False en caso contrario.
    """
    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName(nombre_db)
    
    if not db.open():
        QMessageBox.critical(None, "Error", f"No se pudo abrir la base de datos: {db.lastError().text()}")
        return False

    # Verificar si las tablas necesarias existen, si no, crearlas
    if not crear_tablas():
        return False

    return True

def crear_tablas():
    """
    Crea las tablas necesarias en la base de datos si no existen.

    Returns:
    bool: True si las tablas se crearon correctamente o ya existían, False en caso de error.
    """
    query = QSqlQuery()

    # Habilitar claves foráneas
    if not query.exec("PRAGMA foreign_keys = ON"):
        QMessageBox.critical(None, "Error", f"Error al habilitar claves foráneas: {query.lastError().text()}")
        return False
    
    # Crear tabla DOCTORES
    if not query.exec("""
        CREATE TABLE IF NOT EXISTS DOCTORES (
            id_doctor INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            password TEXT NOT NULL,
            telefono TEXT,
            email TEXT,
            administrador BOOLEAN NOT NULL DEFAULT False
        )
    """):
        QMessageBox.critical(None, "Error", f"Error al crear la tabla DOCTORES: {query.lastError().text()}")
        return False

    # Crear tabla PACIENTES
    if not query.exec("""
        CREATE TABLE IF NOT EXISTS PACIENTES (
            id_paciente INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            telefono TEXT,
            email TEXT,
            fecha_nacimiento DATE,
            id_doctor INTEGER,
            FOREIGN KEY (id_doctor) REFERENCES DOCTORES(id_doctor) ON DELETE CASCADE
        )
    """):
        QMessageBox.critical(None, "Error", f"Error al crear la tabla PACIENTES: {query.lastError().text()}")
        return False

    # Crear tabla HISTORIAS_CLINICAS
    if not query.exec("""
        CREATE TABLE IF NOT EXISTS HISTORIAS_CLINICAS (
            id_historia_clinica INTEGER PRIMARY KEY AUTOINCREMENT,
            id_paciente INTEGER,
            motivo_consulta TEXT,
            fecha_consulta DATE,
            historia_familiar TEXT,
            alergias TEXT,
            diagnostico TEXT,
            tratamiento TEXT,
            evolucion_clinica TEXT,
            FOREIGN KEY (id_paciente) REFERENCES PACIENTES(id_paciente) ON DELETE CASCADE
        )
    """):
        QMessageBox.critical(None, "Error", f"Error al crear la tabla HISTORIAS_CLINICAS: {query.lastError().text()}")
        return False

    return True