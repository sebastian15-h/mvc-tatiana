from models.base_model import BaseModel
from utils.exceptions import EntityNotFoundError, EntityInUseError, DatabaseOperationError
from utils.validators import Validator


class Fincas(BaseModel):
    """Modelo para gestionar fincas"""

    def __init__(self, db_connection):
        super().__init__(db_connection)
        self.table_name = "FINCAS"
        self.entity_name = "Finca"
        self.field_mapping = [
            'ID_finca', 'NOMBRE', 'latitud', 'longitud',
            'EXTENSION_TOTAL_HECTAREAS', 'ALTITUD_METROS',
            'TEMPERATURA_PROMEDIO_ANUAL_fg', 'TIPO_SUELO_PREDOMINANTE', 'region_ubicacion'
        ]

    def create(self, nombre, latitud=None, longitud=None,
               extension_total_hectareas=None, altitud_metros=None,
               temperatura_promedio_anual_fg=None, tipo_suelo_predominante=None,
               region_ubicacion=None):
        """
        Crea una nueva finca

        Args:
            nombre (str): Nombre de la finca (requerido)
            latitud (str): Latitud (opcional)
            longitud (str): Longitud (opcional)
            extension_total_hectareas (str): Extensión total en hectáreas (opcional)
            altitud_metros (str): Altitud en metros (opcional)
            temperatura_promedio_anual_fg (str): Temperatura promedio anual (opcional)
            tipo_suelo_predominante (str): Tipo de suelo predominante (opcional)
            region_ubicacion (str): Región de ubicación (opcional)

        Returns:
            int: ID de la finca creada
        """
        validated_data = self._validate_finca_data(
            nombre, latitud, longitud, extension_total_hectareas, altitud_metros,
            temperatura_promedio_anual_fg, tipo_suelo_predominante, region_ubicacion
        )

        parameters = (
            validated_data['nombre'],
            validated_data['latitud'],
            validated_data['longitud'],
            validated_data['extension_total_hectareas'],
            validated_data['altitud_metros'],
            validated_data['temperatura_promedio_anual_fg'],
            validated_data['tipo_suelo_predominante'],
            validated_data['region_ubicacion']
        )

        results = self.call_procedure('sp_insertfinca', parameters)

        if results and len(results) > 0:
            return results[0][0]  # ID de la finca creada

        raise DatabaseOperationError("No se pudo obtener el ID de la finca creada")

    def get_by_id(self, finca_id):
        """
        Obtiene una finca por su ID

        Args:
            finca_id (int): ID de la finca

        Returns:
            dict: Datos de la finca
        """
        validated_id = Validator.validate_integer(
            str(finca_id), "ID de la Finca", allow_empty=False, min_value=1
        )

        results = self.call_procedure('sp_GetFinca', (validated_id,))

        if not results:
            raise EntityNotFoundError(self.entity_name, finca_id)

        return self._format_entity_data(results[0], self.field_mapping)

    def update(self, finca_id, nombre, latitud=None, longitud=None,
               extension_total_hectareas=None, altitud_metros=None,
               temperatura_promedio_anual_fg=None, tipo_suelo_predominante=None,
               region_ubicacion=None):
        """
        Actualiza una finca existente

        Args:
            finca_id (int): ID de la finca
            nombre (str): Nombre de la finca
            latitud (str): Latitud (opcional)
            longitud (str): Longitud (opcional)
            extension_total_hectareas (str): Extensión total en hectáreas (opcional)
            altitud_metros (str): Altitud en metros (opcional)
            temperatura_promedio_anual_fg (str): Temperatura promedio anual (opcional)
            tipo_suelo_predominante (str): Tipo de suelo predominante (opcional)
            region_ubicacion (str): Región de ubicación (opcional)

        Returns:
            bool: True si se actualizó correctamente
        """
        validated_id = Validator.validate_integer(
            str(finca_id), "ID de la Finca", allow_empty=False, min_value=1
        )

        validated_data = self._validate_finca_data(
            nombre, latitud, longitud, extension_total_hectareas, altitud_metros,
            temperatura_promedio_anual_fg, tipo_suelo_predominante, region_ubicacion
        )

        parameters = (
            validated_id,
            validated_data['nombre'],
            validated_data['latitud'],
            validated_data['longitud'],
            validated_data['extension_total_hectareas'],
            validated_data['altitud_metros'],
            validated_data['temperatura_promedio_anual_fg'],
            validated_data['tipo_suelo_predominante'],
            validated_data['region_ubicacion']
        )

        self.call_procedure('actualizar_finca', parameters)
        return True

    def delete(self, finca_id):
        """
        Elimina una finca

        Args:
            finca_id (int): ID de la finca

        Returns:
            bool: True si se eliminó correctamente
        """
        validated_id = Validator.validate_integer(
            str(finca_id), "ID de la Finca", allow_empty=False, min_value=1
        )

        try:
            self.call_procedure('eliminar_finca', (validated_id,))
            return True
        except Exception as e:
            error_msg = str(e).lower()
            if "tiene órdenes asociadas" in error_msg or "orders" in error_msg:
                raise EntityInUseError(self.entity_name, finca_id, "órdenes")
            raise

    def get_all(self):
        """
        Obtiene todas las fincas

        Returns:
            list: Lista de diccionarios con datos de fincas
        """
        try:
            print("🔍 Modelo Fincas: Ejecutando get_all()...")

            # Intentar diferentes procedimientos almacenados
            try:
                # Opción 1: Procedimiento específico para todas las fincas
                results = self.call_procedure('sp_GetAllFincas', ())
                print("✅ Usando sp_GetAllFincas")
            except Exception as e1:
                try:
                    # Opción 2: Procedimiento con parámetro vacío
                    print("⚠️ sp_GetAllFincas falló, intentando sp_GetFincaByName...")
                    results = self.call_procedure('sp_GetFincaByName', ('',))
                    print("✅ Usando sp_GetFincaByName")
                except Exception as e2:
                    try:
                        # Opción 3: Procedimiento básico
                        print("⚠️ sp_GetFincaByName falló, intentando sp_GetFinca...")
                        results = self.call_procedure('sp_GetFinca', (0,))
                        print("✅ Usando sp_GetFinca")
                    except Exception as e3:
                        # Opción 4: Consulta directa como último recurso
                        print("⚠️ Todos los procedimientos fallaron, usando consulta directa...")
                        query = "SELECT * FROM FINCAS"
                        results = self.db.execute_query(query)
                        print("✅ Usando consulta directa")

            print(f"📊 Modelo Fincas: Resultados obtenidos: {len(results)} filas")

            if results:
                formatted_results = []
                for row in results:
                    formatted_finca = self._format_entity_data(row, self.field_mapping)
                    formatted_results.append(formatted_finca)

                    # DEBUG: Mostrar primera finca
                    if len(formatted_results) == 1:
                        print(f"🔍 Primera finca formateada: {formatted_finca}")

                print(f"✅ Modelo Fincas: {len(formatted_results)} fincas formateadas")
                return formatted_results
            else:
                print("⚠️ Modelo Fincas: No se obtuvieron resultados")
                return []

        except Exception as e:
            print(f"❌ Error en Modelo Fincas get_all(): {e}")
            import traceback
            traceback.print_exc()
            return []

    def search(self, search_term):
        """
        Busca fincas por nombre o región

        Args:
            search_term (str): Término de búsqueda

        Returns:
            list: Lista de fincas que coinciden
        """
        if not search_term or not search_term.strip():
            return []

        results = self.call_procedure('sp_SearchFincas', (search_term.strip(),))
        return [self._format_entity_data(row, self.field_mapping) for row in results]

    def _validate_finca_data(self, nombre, latitud, longitud, extension_total_hectareas,
                             altitud_metros, temperatura_promedio_anual_fg,
                             tipo_suelo_predominante, region_ubicacion):
        """
        Valida los datos de una finca

        Args:
            nombre (str): Nombre de la finca
            latitud (str): Latitud
            longitud (str): Longitud
            extension_total_hectareas (str): Extensión total en hectáreas
            altitud_metros (str): Altitud en metros
            temperatura_promedio_anual_fg (str): Temperatura promedio anual
            tipo_suelo_predominante (str): Tipo de suelo predominante
            region_ubicacion (str): Región de ubicación

        Returns:
            dict: Datos validados
        """
        validated_data = {}

        validated_data['nombre'] = Validator.validate_string_length(
            nombre, "Nombre de la Finca", min_length=1, max_length=100, allow_empty=False
        )

        validated_data['latitud'] = Validator.validate_string_length(
            latitud if latitud is not None else "",
            "Latitud", max_length=20, allow_empty=True
        )

        validated_data['longitud'] = Validator.validate_string_length(
            longitud if longitud is not None else "",
            "Longitud", max_length=20, allow_empty=True
        )

        validated_data['extension_total_hectareas'] = Validator.validate_string_length(
            extension_total_hectareas if extension_total_hectareas is not None else "",
            "Extensión Total Hectáreas", max_length=20, allow_empty=True
        )

        validated_data['altitud_metros'] = Validator.validate_string_length(
            altitud_metros if altitud_metros is not None else "",
            "Altitud Metros", max_length=10, allow_empty=True
        )

        validated_data['temperatura_promedio_anual_fg'] = Validator.validate_string_length(
            temperatura_promedio_anual_fg if temperatura_promedio_anual_fg is not None else "",
            "Temperatura Promedio Anual", max_length=10, allow_empty=True
        )

        validated_data['tipo_suelo_predominante'] = Validator.validate_string_length(
            tipo_suelo_predominante if tipo_suelo_predominante is not None else "",
            "Tipo Suelo Predominante", max_length=50, allow_empty=True
        )

        validated_data['region_ubicacion'] = Validator.validate_string_length(
            region_ubicacion if region_ubicacion is not None else "",
            "Región Ubicación", max_length=50, allow_empty=True
        )

        return validated_data