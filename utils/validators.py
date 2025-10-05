"""
Módulo de validaciones para la aplicación
"""
import re
from datetime import datetime


class Validator:
    """Clase con métodos estáticos para validar diferentes tipos de datos"""

    @staticmethod
    def validate_string(value, field_name, allow_empty=True, min_length=None, max_length=None):
        """
        Valida una cadena de texto
        """
        if value is None:
            if allow_empty:
                return ""
            else:
                raise ValueError(f"{field_name} es requerido")

        str_value = str(value).strip()

        if not str_value and not allow_empty:
            raise ValueError(f"{field_name} es requerido")

        if min_length is not None and len(str_value) < min_length:
            raise ValueError(f"{field_name} debe tener al menos {min_length} caracteres")

        if max_length is not None and len(str_value) > max_length:
            raise ValueError(f"{field_name} no puede tener más de {max_length} caracteres")

        return str_value

    @staticmethod
    def validate_integer(value, field_name, allow_empty=True, min_value=None, max_value=None):
        """
        Valida que un valor sea un entero
        """
        if value is None or (isinstance(value, str) and not value.strip()):
            if allow_empty:
                return None
            else:
                raise ValueError(f"{field_name} es requerido")

        try:
            if isinstance(value, str):
                value = value.strip()
            int_value = int(value)

            if min_value is not None and int_value < min_value:
                raise ValueError(f"{field_name} debe ser mayor o igual a {min_value}")

            if max_value is not None and int_value > max_value:
                raise ValueError(f"{field_name} debe ser menor o igual a {max_value}")

            return int_value

        except (ValueError, TypeError):
            raise ValueError(f"{field_name} debe ser un número entero válido")

    @staticmethod
    def validate_float(value, field_name, allow_empty=True, min_value=None, max_value=None):
        """
        Valida que un valor sea un número decimal
        """
        if value is None or (isinstance(value, str) and not value.strip()):
            if allow_empty:
                return None
            else:
                raise ValueError(f"{field_name} es requerido")

        try:
            if isinstance(value, str):
                value = value.strip()
            float_value = float(value)

            if min_value is not None and float_value < min_value:
                raise ValueError(f"{field_name} debe ser mayor o igual a {min_value}")

            if max_value is not None and float_value > max_value:
                raise ValueError(f"{field_name} debe ser menor o igual a {max_value}")

            return float_value

        except (ValueError, TypeError):
            raise ValueError(f"{field_name} debe ser un número válido")

    @staticmethod
    def validate_string_length(value, field_name, min_length=None, max_length=None, allow_empty=True):
        """
        Valida la longitud de una cadena
        """
        if value is None:
            if allow_empty:
                return ""
            else:
                raise ValueError(f"{field_name} es requerido")

        str_value = str(value).strip()

        if not str_value and not allow_empty:
            raise ValueError(f"{field_name} es requerido")

        if min_length is not None and len(str_value) < min_length:
            raise ValueError(f"{field_name} debe tener al menos {min_length} caracteres")

        if max_length is not None and len(str_value) > max_length:
            raise ValueError(f"{field_name} no puede tener más de {max_length} caracteres")

        return str_value