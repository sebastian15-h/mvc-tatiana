from controllers.base_controller import BaseController
from utils.exceptions import EntityNotFoundError, DatabaseOperationError


class HotelesController(BaseController):
    def __init__(self, model):
        super().__init__(model)

    def get_by_id(self, entity_id):
        """Obtiene un hotel por ID"""
        try:
            return self.model.get_by_id(entity_id)
        except EntityNotFoundError:
            raise
        except Exception as e:
            raise Exception(f"Error obteniendo hotel: {str(e)}")

    def get_all(self):
        """Obtiene todos los hoteles"""
        try:
            return self.model.get_all()
        except Exception as e:
            raise Exception(f"Error obteniendo hoteles: {str(e)}")

    def create(self, form_data):
        """Crea un nuevo hotel"""
        try:
            # Validaciones básicas
            nombre_val = form_data.get('NOMBRE_HOTEL', '').strip()
            direccion_val = form_data.get('DIRECCION', '').strip()

            if not nombre_val:
                raise ValueError("Debe ingresar el nombre del hotel")
            if not direccion_val:
                raise ValueError("Debe ingresar la dirección del hotel")

            # Validar campos numéricos
            categoria_val = form_data.get('CATEGORIA', '').strip()
            if categoria_val:
                try:
                    int(categoria_val)
                except ValueError:
                    raise ValueError("Categoría debe ser un número entero")

            telefono_val = form_data.get('TELEFONO', '').strip()
            if telefono_val:
                try:
                    int(telefono_val)
                except ValueError:
                    raise ValueError("Teléfono debe ser un número entero")

            habitantes_val = form_data.get('HABITANTES', '').strip()
            if habitantes_val:
                try:
                    int(habitantes_val)
                except ValueError:
                    raise ValueError("Número de habitantes debe ser un número entero")

            # Llamar al modelo
            return self.model.create(form_data)

        except ValueError as ve:
            raise ve
        except Exception as e:
            raise Exception(f"Error creando hotel: {str(e)}")

    def update(self, entity_id, form_data):
        """Actualiza un hotel"""
        try:
            # Validaciones básicas
            nombre_val = form_data.get('NOMBRE_HOTEL', '').strip()
            direccion_val = form_data.get('DIRECCION', '').strip()

            if not nombre_val:
                raise ValueError("Debe ingresar el nombre del hotel")
            if not direccion_val:
                raise ValueError("Debe ingresar la dirección del hotel")

            # Validar campos numéricos
            categoria_val = form_data.get('CATEGORIA', '').strip()
            if categoria_val:
                try:
                    int(categoria_val)
                except ValueError:
                    raise ValueError("Categoría debe ser un número entero")

            telefono_val = form_data.get('TELEFONO', '').strip()
            if telefono_val:
                try:
                    int(telefono_val)
                except ValueError:
                    raise ValueError("Teléfono debe ser un número entero")

            habitantes_val = form_data.get('HABITANTES', '').strip()
            if habitantes_val:
                try:
                    int(habitantes_val)
                except ValueError:
                    raise ValueError("Número de habitantes debe ser un número entero")

            # Llamar al modelo
            return self.model.update(entity_id, form_data)

        except ValueError as ve:
            raise ve
        except Exception as e:
            raise Exception(f"Error actualizando hotel: {str(e)}")

    def delete(self, entity_id):
        """Elimina un hotel"""
        try:
            return self.model.delete(entity_id)
        except EntityNotFoundError as enfe:
            raise enfe
        except Exception as e:
            raise Exception(f"Error eliminando hotel: {str(e)}")