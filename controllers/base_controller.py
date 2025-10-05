"""
Clase base para todos los controladores de la aplicación Northwind
"""
from abc import ABC, abstractmethod
from utils.exceptions import ValidationError, DatabaseOperationError, EntityNotFoundError


class BaseController(ABC):
    """Clase abstracta base para todos los controladores"""

    def __init__(self, model):
        """
        Inicializa el controlador con su modelo asociado

        Args:
            model: Instancia del modelo asociado
        """
        self.model = model
        self.entity_name = model.entity_name if hasattr(model, 'entity_name') else "Entidad"

    def create(self, **kwargs):
        """
        Crea una nueva entidad

        Args:
            **kwargs: Datos de la entidad

        Returns:
            int: ID de la entidad creada

        Raises:
            ValidationError: Si los datos no son válidos
            DatabaseOperationError: Si hay error en la base de datos
        """
        try:
            # Pre-procesamiento (puede ser sobrescrito por controladores específicos)
            processed_data = self._preprocess_create_data(**kwargs)

            # Crear entidad usando el modelo
            entity_id = self.model.create(**processed_data)

            # Post-procesamiento (puede ser sobrescrito por controladores específicos)
            self._postprocess_create(entity_id, **processed_data)

            return entity_id

        except ValidationError:
            raise  # Re-lanzar errores de validación tal como están
        except DatabaseOperationError:
            raise  # Re-lanzar errores de base de datos tal como están
        except Exception as e:
            raise DatabaseOperationError(f"Error inesperado creando {self.entity_name}: {str(e)}")

    def get_by_id(self, entity_id):
        """
        Obtiene una entidad por su ID

        Args:
            entity_id (int): ID de la entidad

        Returns:
            dict: Datos de la entidad

        Raises:
            EntityNotFoundError: Si la entidad no existe
            DatabaseOperationError: Si hay error en la base de datos
        """
        try:
            # Validar ID básico
            if not entity_id or entity_id <= 0:
                raise ValidationError("ID", "debe ser un número positivo")

            # Obtener entidad usando el modelo
            entity_data = self.model.get_by_id(entity_id)

            # Post-procesamiento (puede ser sobrescrito por controladores específicos)
            processed_data = self._postprocess_get_data(entity_data)

            return processed_data

        except (ValidationError, EntityNotFoundError):
            raise  # Re-lanzar estos errores tal como están
        except Exception as e:
            raise DatabaseOperationError(f"Error obteniendo {self.entity_name}: {str(e)}")

    def update(self, entity_id, **kwargs):
        """
        Actualiza una entidad existente

        Args:
            entity_id (int): ID de la entidad
            **kwargs: Datos a actualizar

        Returns:
            bool: True si se actualizó correctamente
        """
        try:
            # Validar ID básico
            if not entity_id or entity_id <= 0:
                raise ValidationError("ID", "debe ser un número positivo")

            # Pre-procesamiento
            processed_data = self._preprocess_update_data(entity_id, **kwargs)

            # Actualizar usando el modelo
            result = self.model.update(entity_id, **processed_data)

            # Post-procesamiento
            self._postprocess_update(entity_id, **processed_data)

            return result

        except (ValidationError, EntityNotFoundError):
            raise
        except Exception as e:
            raise DatabaseOperationError(f"Error actualizando {self.entity_name}: {str(e)}")

    def delete(self, entity_id):
        """
        Elimina una entidad

        Args:
            entity_id (int): ID de la entidad

        Returns:
            bool: True si se eliminó correctamente
        """
        try:
            # Validar ID básico
            if not entity_id or entity_id <= 0:
                raise ValidationError("ID", "debe ser un número positivo")

            # Pre-procesamiento (verificaciones adicionales)
            self._preprocess_delete(entity_id)

            # Eliminar usando el modelo
            result = self.model.delete(entity_id)

            # Post-procesamiento (limpieza adicional)
            self._postprocess_delete(entity_id)

            return result

        except (ValidationError, EntityNotFoundError):
            raise
        except Exception as e:
            raise DatabaseOperationError(f"Error eliminando {self.entity_name}: {str(e)}")

    def get_all(self):
        """
        Obtiene todas las entidades

        Returns:
            list: Lista de entidades
        """
        try:
            entities = self.model.get_all()

            # Post-procesar cada entidad
            processed_entities = []
            for entity in entities:
                processed_entity = self._postprocess_get_data(entity)
                processed_entities.append(processed_entity)

            return processed_entities

        except Exception as e:
            raise DatabaseOperationError(f"Error obteniendo lista de {self.entity_name}s: {str(e)}")

    def search(self, search_term):
        """
        Busca entidades por término

        Args:
            search_term (str): Término de búsqueda

        Returns:
            list: Lista de entidades que coinciden
        """
        try:
            if not search_term or not search_term.strip():
                return []

            # Pre-procesar término de búsqueda
            processed_term = self._preprocess_search_term(search_term)

            # Buscar usando el modelo
            results = self.model.search(processed_term)

            # Post-procesar resultados
            processed_results = []
            for result in results:
                processed_result = self._postprocess_search_result(result)
                processed_results.append(processed_result)

            return processed_results

        except Exception as e:
            raise DatabaseOperationError(f"Error buscando {self.entity_name}s: {str(e)}")

    def exists(self, entity_id):
        """
        Verifica si una entidad existe

        Args:
            entity_id (int): ID de la entidad

        Returns:
            bool: True si existe
        """
        try:
            return self.model.exists(entity_id)
        except Exception:
            return False

    def get_count(self):
        """
        Obtiene el número total de entidades

        Returns:
            int: Número total
        """
        try:
            return self.model.get_count()
        except Exception:
            return 0

    # Métodos de procesamiento que pueden ser sobrescritos por controladores específicos

    def _preprocess_create_data(self, **kwargs):
        """
        Pre-procesa los datos antes de crear
        Puede ser sobrescrito por controladores específicos

        Args:
            **kwargs: Datos originales

        Returns:
            dict: Datos procesados
        """
        return kwargs

    def _postprocess_create(self, entity_id, **kwargs):
        """
        Post-procesa después de crear
        Puede ser sobrescrito por controladores específicos

        Args:
            entity_id (int): ID de la entidad creada
            **kwargs: Datos utilizados para crear
        """
        pass

    def _preprocess_update_data(self, entity_id, **kwargs):
        """
        Pre-procesa los datos antes de actualizar
        Puede ser sobrescrito por controladores específicos

        Args:
            entity_id (int): ID de la entidad
            **kwargs: Datos originales

        Returns:
            dict: Datos procesados
        """
        return kwargs

    def _postprocess_update(self, entity_id, **kwargs):
        """
        Post-procesa después de actualizar
        Puede ser sobrescrito por controladores específicos

        Args:
            entity_id (int): ID de la entidad actualizada
            **kwargs: Datos utilizados para actualizar
        """
        pass

    def _preprocess_delete(self, entity_id):
        """
        Pre-procesa antes de eliminar
        Puede ser sobrescrito por controladores específicos

        Args:
            entity_id (int): ID de la entidad a eliminar
        """
        pass

    def _postprocess_delete(self, entity_id):
        """
        Post-procesa después de eliminar
        Puede ser sobrescrito por controladores específicos

        Args:
            entity_id (int): ID de la entidad eliminada
        """
        pass

    def _postprocess_get_data(self, entity_data):
        """
        Post-procesa los datos obtenidos
        Puede ser sobrescrito por controladores específicos

        Args:
            entity_data (dict): Datos originales de la entidad

        Returns:
            dict: Datos procesados
        """
        return entity_data

    def _preprocess_search_term(self, search_term):
        """
        Pre-procesa el término de búsqueda
        Puede ser sobrescrito por controladores específicos

        Args:
            search_term (str): Término original

        Returns:
            str: Término procesado
        """
        return search_term.strip()

    def _postprocess_search_result(self, result_data):
        """
        Post-procesa los resultados de búsqueda
        Puede ser sobrescrito por controladores específicos

        Args:
            result_data (dict): Datos originales del resultado

        Returns:
            dict: Datos procesados
        """
        return self._postprocess_get_data(result_data)

    # Métodos de utilidad

    def validate_required_fields(self, data, required_fields):
        """
        Valida que los campos requeridos estén presentes

        Args:
            data (dict): Datos a validar
            required_fields (list): Lista de campos requeridos

        Raises:
            ValidationError: Si falta algún campo requerido
        """
        for field in required_fields:
            if field not in data or not data[field]:
                field_name = field.replace('_', ' ').title()
                raise ValidationError(field_name, "es requerido")

    def clean_string_data(self, data_dict, string_fields):
        """
        Limpia los datos de string (trim, None si vacío)

        Args:
            data_dict (dict): Datos a limpiar
            string_fields (list): Lista de campos string

        Returns:
            dict: Datos limpiados
        """
        cleaned_data = data_dict.copy()

        for field in string_fields:
            if field in cleaned_data and cleaned_data[field] is not None:
                value = str(cleaned_data[field]).strip()
                cleaned_data[field] = value if value else None

        return cleaned_data
