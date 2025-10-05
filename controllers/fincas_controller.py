"""
Controlador para la gestión de fincas
"""
from abc import ABC

from controllers.base_controller import BaseController
from utils.exceptions import DatabaseOperationError
from utils.validators import Validator
from utils.helpers import safe_str, DataFormatter


class FincasController(BaseController, ABC):
    """Controlador específico para fincas"""

    def __init__(self, fincas_model):
        super().__init__(fincas_model)
        self.required_fields = ['finca_name']
        self.string_fields = [
            'finca_name',
            'latitud',
            'longitud',
            'extension_total_hectareas',
            'altitud_metros',
            'temperatura_promedio_anual_fg',
            'tipo_suelo_predominante',
            'region_ubicacion'
        ]

    def create(self, finca_name=None, latitud=None, longitud=None,
               extension_total_hectareas=None, altitud_metros=None,
               temperatura_promedio_anual_fg=None, tipo_suelo_predominante=None,
               region_ubicacion=None):
        """
        Crea una nueva finca

        Args:
            finca_name (str): Nombre de la finca
            latitud (str): Latitud
            longitud (str): Longitud
            extension_total_hectareas (str/float): Extensión total en hectáreas
            altitud_metros (str/int): Altitud en metros
            temperatura_promedio_anual_fg (str/float): Temperatura promedio anual
            tipo_suelo_predominante (str): Tipo de suelo predominante
            region_ubicacion (str): Región o ubicación

        Returns:
            int: ID de la finca creada
        """
        data = {
            'finca_name': finca_name,
            'latitud': latitud,
            'longitud': longitud,
            'extension_total_hectareas': extension_total_hectareas,
            'altitud_metros': altitud_metros,
            'temperatura_promedio_anual_fg': temperatura_promedio_anual_fg,
            'tipo_suelo_predominante': tipo_suelo_predominante,
            'region_ubicacion': region_ubicacion
        }
        return super().create(**data)

    def update(self, finca_id, finca_name=None, latitud=None, longitud=None,
               extension_total_hectareas=None, altitud_metros=None,
               temperatura_promedio_anual_fg=None, tipo_suelo_predominante=None,
               region_ubicacion=None):
        """
        Actualiza una finca existente

        Args:
            finca_id (int): ID de la finca
            finca_name (str): Nombre de la finca
            latitud (str): Latitud
            longitud (str): Longitud
            extension_total_hectareas (str/float): Extensión total en hectáreas
            altitud_metros (str/int): Altitud en metros
            temperatura_promedio_anual_fg (str/float): Temperatura promedio anual
            tipo_suelo_predominante (str): Tipo de suelo predominante
            region_ubicacion (str): Región o ubicación

        Returns:
            bool: True si se actualizó correctamente
        """
        data = {
            'finca_name': finca_name,
            'latitud': latitud,
            'longitud': longitud,
            'extension_total_hectareas': extension_total_hectareas,
            'altitud_metros': altitud_metros,
            'temperatura_promedio_anual_fg': temperatura_promedio_anual_fg,
            'tipo_suelo_predominante': tipo_suelo_predominante,
            'region_ubicacion': region_ubicacion
        }
        return super().update(finca_id, **data)

    def _preprocess_create_data(self, **kwargs):
        """Pre-procesa los datos antes de crear una finca"""
        return self._validate_and_clean_finca_data(**kwargs)

    def _preprocess_update_data(self, entity_id, **kwargs):
        """Pre-procesa los datos antes de actualizar una finca"""
        return self._validate_and_clean_finca_data(**kwargs)

    def _validate_and_clean_finca_data(self, **kwargs):
        """
        Valida y limpia los datos de la finca

        Returns:
            dict: Datos validados y limpiados
        """
        cleaned_data = {}

        # Validar nombre de la finca (requerido)
        finca_name = kwargs.get('finca_name', '')
        if isinstance(finca_name, str):
            finca_name = finca_name.strip()

        cleaned_data['finca_name'] = Validator.validate_string_length(
            safe_str(finca_name), "Nombre de la Finca",
            min_length=1, max_length=100, allow_empty=False
        )
        cleaned_data['finca_name'] = DataFormatter.capitalize_name(cleaned_data['finca_name'])

        # Validar latitud (opcional, validar formato si quieres)
        latitud = kwargs.get('latitud', '')
        cleaned_data['latitud'] = Validator.validate_string_length(
            safe_str(latitud), "Latitud",
            max_length=20, allow_empty=True
        )

        # Validar longitud (opcional)
        longitud = kwargs.get('longitud', '')
        cleaned_data['longitud'] = Validator.validate_string_length(
            safe_str(longitud), "Longitud",
            max_length=20, allow_empty=True
        )

        # Validar extensión total en hectáreas (opcional, validar número)
        extension = kwargs.get('extension_total_hectareas', None)
        if extension is not None:
            try:
                extension_val = float(extension)
                if extension_val < 0:
                    raise ValueError("Extensión total debe ser un número positivo")
                cleaned_data['extension_total_hectareas'] = extension_val
            except Exception:
                raise ValueError("Extensión total debe ser un número válido")
        else:
            cleaned_data['extension_total_hectareas'] = None

        # Validar altitud en metros (opcional, validar número entero)
        altitud = kwargs.get('altitud_metros', None)
        if altitud is not None:
            try:
                altitud_val = int(altitud)
                if altitud_val < 0:
                    raise ValueError("Altitud debe ser un número positivo")
                cleaned_data['altitud_metros'] = altitud_val
            except Exception:
                raise ValueError("Altitud debe ser un número entero válido")
        else:
            cleaned_data['altitud_metros'] = None

        # Validar temperatura promedio anual (opcional, validar número float)
        temp = kwargs.get('temperatura_promedio_anual_fg', None)
        if temp is not None:
            try:
                temp_val = float(temp)
                cleaned_data['temperatura_promedio_anual_fg'] = temp_val
            except Exception:
                raise ValueError("Temperatura promedio anual debe ser un número válido")
        else:
            cleaned_data['temperatura_promedio_anual_fg'] = None

        # Validar tipo de suelo predominante (opcional)
        tipo_suelo = kwargs.get('tipo_suelo_predominante', '')
        cleaned_data['tipo_suelo_predominante'] = Validator.validate_string_length(
            safe_str(tipo_suelo), "Tipo de Suelo Predominante",
            max_length=50, allow_empty=True
        )
        if cleaned_data['tipo_suelo_predominante']:
            cleaned_data['tipo_suelo_predominante'] = DataFormatter.capitalize_name(cleaned_data['tipo_suelo_predominante'])

        # Validar región/ubicación (opcional)
        region = kwargs.get('region_ubicacion', '')
        cleaned_data['region_ubicacion'] = Validator.validate_string_length(
            safe_str(region), "Región de Ubicación",
            max_length=50, allow_empty=True
        )
        if cleaned_data['region_ubicacion']:
            cleaned_data['region_ubicacion'] = DataFormatter.capitalize_name(cleaned_data['region_ubicacion'])

        return cleaned_data

    def _postprocess_get_data(self, entity_data):
        """Post-procesa los datos obtenidos de una finca"""
        if not entity_data:
            return entity_data

        # Asegurar que los campos tengan valores por defecto
        entity_data['FincaName'] = entity_data.get('FincaName', '')
        entity_data['Latitud'] = entity_data.get('Latitud', '')
        entity_data['Longitud'] = entity_data.get('Longitud', '')
        entity_data['ExtensionTotalHectareas'] = entity_data.get('ExtensionTotalHectareas', None)
        entity_data['AltitudMetros'] = entity_data.get('AltitudMetros', None)
        entity_data['TemperaturaPromedioAnualFg'] = entity_data.get('TemperaturaPromedioAnualFg', None)
        entity_data['TipoSueloPredominante'] = entity_data.get('TipoSueloPredominante', '')
        entity_data['RegionUbicacion'] = entity_data.get('RegionUbicacion', '')

        return entity_data

    # Ejemplos de métodos de consulta personalizados que podrías agregar:

    def get_by_region(self, region_ubicacion):
        """
        Obtiene fincas por región

        Args:
            region_ubicacion (str): Región

        Returns:
            list: Lista de fincas en la región
        """
        try:
            if not region_ubicacion or not region_ubicacion.strip():
                return []

            formatted_region = DataFormatter.capitalize_name(region_ubicacion.strip())

            fincas = self.model.get_by_region(formatted_region)

            processed_fincas = [self._postprocess_get_data(finca) for finca in fincas]

            return processed_fincas

        except Exception as e:
            raise DatabaseOperationError(f"Error obteniendo fincas por región: {str(e)}")

    def validate_finca_data_for_ui(self, form_data):
        """
        Valida datos de finca desde la UI sin guardar

        Args:
            form_data (dict): Datos del formulario

        Returns:
            tuple: (is_valid, errors_dict)
        """
        errors = {}

        try:
            self._validate_and_clean_finca_data(**form_data)
        except Exception as e:
            error_msg = str(e)

            if "Nombre de la Finca" in error_msg:
                errors['finca_name'] = error_msg
            elif "Latitud" in error_msg:
                errors['latitud'] = error_msg
            elif "Longitud" in error_msg:
                errors['longitud'] = error_msg
            elif "Extensión total" in error_msg:
                errors['extension_total_hectareas'] = error_msg
            elif "Altitud" in error_msg:
                errors['altitud_metros'] = error_msg
            elif "Temperatura promedio anual" in error_msg:
                errors['temperatura_promedio_anual_fg'] = error_msg
            elif "Tipo de Suelo Predominante" in error_msg:
                errors['tipo_suelo_predominante'] = error_msg
            elif "Región de Ubicación" in error_msg:
                errors['region_ubicacion'] = error_msg
            else:
                errors['general'] = error_msg

        return len(errors) == 0, errors

    def get_finca_summary(self, finca_id):
        """
        Obtiene un resumen de la finca con información adicional

        Args:
            finca_id (int): ID de la finca

        Returns:
            dict: Resumen de la finca
        """
        try:
            finca = self.get_by_id(finca_id)

            summary = finca.copy()
            summary['HasLocation'] = bool(finca.get('Latitud') and finca.get('Longitud'))
            summary['HasExtension'] = finca.get('ExtensionTotalHectareas') is not None
            summary['IsComplete'] = all([
                finca.get('FincaName'),
                finca.get('Latitud'),
                finca.get('Longitud'),
                finca.get('ExtensionTotalHectareas'),
                finca.get('AltitudMetros'),
                finca.get('TemperaturaPromedioAnualFg'),
                finca.get('TipoSueloPredominante'),
                finca.get('RegionUbicacion')
            ])

            return summary

        except Exception as e:
            raise DatabaseOperationError(f"Error obteniendo resumen de la finca: {str(e)}")
