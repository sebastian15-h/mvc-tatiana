"""
Clase base para todos los modelos de la aplicación Northwind
"""
from abc import ABC, abstractmethod
from utils.exceptions import EntityNotFoundError, DatabaseOperationError


class BaseModel(ABC):
    """Clase abstracta base para todos los modelos"""

    def __init__(self, db_connection):
        """
        Inicializa el modelo con una conexión a base de datos

        Args:
            db_connection: Instancia de DatabaseConnection
        """
        self.db = db_connection
        self.table_name = None  # Debe ser definido por cada modelo hijo
        self.entity_name = None  # Nombre legible de la entidad

    def call_procedure(self, procedure_name, parameters=None):
        """
        Ejecuta un procedimiento almacenado y maneja errores

        Args:
            procedure_name (str): Nombre del procedimiento
            parameters (tuple): Parámetros del procedimiento

        Returns:
            list: Resultados del procedimiento

        Raises:
            DatabaseOperationError: Si hay error en la operación
        """
        try:
            success, results = self.db.call_procedure(procedure_name, parameters)
            if success:
                return results
            else:
                raise DatabaseOperationError(f"Error en procedimiento {procedure_name}")
        except Exception as e:
            raise DatabaseOperationError(f"Error ejecutando {procedure_name}: {str(e)}")

    @abstractmethod
    def create(self, **kwargs):
        """
        Crea una nueva entidad

        Args:
            **kwargs: Datos de la entidad

        Returns:
            int: ID de la entidad creada
        """
        pass

    @abstractmethod
    def get_by_id(self, entity_id):
        """
        Obtiene una entidad por su ID

        Args:
            entity_id (int): ID de la entidad

        Returns:
            dict: Datos de la entidad

        Raises:
            EntityNotFoundError: Si la entidad no existe
        """
        pass

    @abstractmethod
    def update(self, entity_id, **kwargs):
        """
        Actualiza una entidad existente

        Args:
            entity_id (int): ID de la entidad
            **kwargs: Datos a actualizar

        Returns:
            bool: True si se actualizó correctamente
        """
        pass

    @abstractmethod
    def delete(self, entity_id):
        """
        Elimina una entidad

        Args:
            entity_id (int): ID de la entidad

        Returns:
            bool: True si se eliminó correctamente
        """
        pass

    @abstractmethod
    def get_all(self):
        """
        Obtiene todas las entidades

        Returns:
            list: Lista de todas las entidades
        """
        pass

    def search(self, search_term):
        """
        Busca entidades por término de búsqueda

        Args:
            search_term (str): Término a buscar

        Returns:
            list: Lista de entidades que coinciden
        """
        # Implementación base, puede ser sobrescrita por modelos específicos
        return []

    def exists(self, entity_id):
        """
        Verifica si una entidad existe

        Args:
            entity_id (int): ID de la entidad

        Returns:
            bool: True si existe, False si no
        """
        try:
            self.get_by_id(entity_id)
            return True
        except EntityNotFoundError:
            return False

    def get_count(self):
        """
        Obtiene el número total de entidades

        Returns:
            int: Número total de entidades
        """
        try:
            query = f"SELECT COUNT(*) FROM {self.table_name}"
            results = self.db.execute_query(query)
            return results[0][0] if results else 0
        except Exception:
            return 0

    def validate_foreign_key(self, fk_value, fk_table, fk_column='ID'):
        """
        Valida que una clave foránea exista

        Args:
            fk_value (int): Valor de la clave foránea
            fk_table (str): Tabla de la clave foránea
            fk_column (str): Columna de la clave foránea

        Returns:
            bool: True si la clave existe
        """
        if fk_value is None:
            return True  # NULL es válido para claves foráneas opcionales

        try:
            query = f"SELECT COUNT(*) FROM {fk_table} WHERE {fk_column} = %s"
            results = self.db.execute_query(query, (fk_value,))
            return results[0][0] > 0 if results else False
        except Exception:
            return False

    def _format_entity_data(self, raw_data, field_mapping):
        """
        Formatea los datos crudos de la base de datos a un diccionario

        Args:
            raw_data (tuple): Datos crudos de la consulta
            field_mapping (list): Lista de nombres de campos

        Returns:
            dict: Datos formateados
        """
        if not raw_data:
            return {}

        return {field: value for field, value in zip(field_mapping, raw_data)}

    def _prepare_insert_data(self, data_dict):
        """
        Prepara los datos para inserción eliminando None y campos vacíos

        Args:
            data_dict (dict): Diccionario con los datos

        Returns:
            dict: Datos limpiados
        """
        cleaned_data = {}
        for key, value in data_dict.items():
            if value is not None and value != '':
                cleaned_data[key] = value
        return cleaned_data