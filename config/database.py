"""
Configuración y manejo de conexión a base de datos
"""
import mysql.connector
from mysql.connector import Error
from utils.exceptions import DatabaseConnectionError, DatabaseOperationError


class DatabaseConnection:
    """Clase para manejar la conexión a la base de datos MySQL"""

    def __init__(self):
        self.connection = None
        self.cursor = None
        self.config = {
            'host': 'localhost',
            'database': 'agrocontrol_sas_db',
            'user': 'root',
            'password': '',
            'autocommit': False,
            'buffered': True
        }

    def connect(self):
        """Establece conexión con la base de datos"""
        try:
            if self.connection is None or not self.connection.is_connected():
                self.connection = mysql.connector.connect(**self.config)
                self.cursor = self.connection.cursor(buffered=True)
            return True
        except Error as e:
            raise DatabaseConnectionError(f"Error conectando a la base de datos: {e}")

    def disconnect(self):
        """Cierra la conexión con la base de datos"""
        try:
            if self.cursor:
                self.cursor.close()
                self.cursor = None
            if self.connection and self.connection.is_connected():
                self.connection.close()
                self.connection = None
        except Error as e:
            print(f"Error al cerrar conexión: {e}")

    def test_connection(self):
        """Prueba la conexión a la base de datos"""
        try:
            self.connect()
            self.cursor.execute("SELECT 1")
            result = self.cursor.fetchone()
            return result is not None
        except Exception:
            return False

    def call_procedure(self, procedure_name, parameters=None):
        """
        Ejecuta un procedimiento almacenado

        Args:
            procedure_name (str): Nombre del procedimiento
            parameters (tuple): Parámetros del procedimiento

        Returns:
            tuple: (success, results) donde success es bool y results es list
        """
        try:
            self.connect()

            if parameters:
                self.cursor.callproc(procedure_name, parameters)
            else:
                self.cursor.callproc(procedure_name)

            # Obtener resultados
            results = []
            for result in self.cursor.stored_results():
                results.extend(result.fetchall())

            return True, results

        except Error as e:
            if self.connection:
                self.connection.rollback()
            raise DatabaseOperationError(f"Error ejecutando procedimiento {procedure_name}: {e}")

    def execute_query(self, query, parameters=None):
        """
        Ejecuta una consulta SQL directa - CORREGIDO

        Args:
            query (str): Consulta SQL
            parameters (tuple): Parámetros de la consulta

        Returns:
            list: Resultados de la consulta (solo para SELECT)
            int: Número de filas afectadas (para INSERT, UPDATE, DELETE)
        """
        try:
            self.connect()
            print(f"📝 Ejecutando query: {query}")
            print(f"📋 Parámetros: {parameters}")

            if parameters:
                self.cursor.execute(query, parameters)
            else:
                self.cursor.execute(query)

            # Verificar tipo de consulta
            query_type = query.strip().upper()

            if query_type.startswith('SELECT') or query_type.startswith('SHOW') or query_type.startswith('DESCRIBE'):
                # Para consultas que retornan datos
                results = self.cursor.fetchall()
                print(f"📊 Resultados obtenidos: {len(results)} filas")
                return results
            else:
                # Para INSERT, UPDATE, DELETE - hacer commit y retornar filas afectadas
                self.connection.commit()
                rows_affected = self.cursor.rowcount
                print(f"✅ Query ejecutada. Filas afectadas: {rows_affected}")
                return rows_affected

        except Error as e:
            if self.connection:
                self.connection.rollback()
            print(f"❌ Error en execute_query: {e}")
            raise DatabaseOperationError(f"Error ejecutando consulta: {e}")

    def commit(self):
        """Confirma las transacciones pendientes"""
        if self.connection:
            self.connection.commit()

    def rollback(self):
        """Revierte las transacciones pendientes"""
        if self.connection:
            self.connection.rollback()

    def is_connected(self):
        """Verifica si la conexión está activa"""
        return self.connection is not None and self.connection.is_connected()