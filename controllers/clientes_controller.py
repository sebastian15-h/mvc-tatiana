from controllers.base_controller import BaseController
from utils.exceptions import EntityNotFoundError, DatabaseOperationError


class ClientesController(BaseController):
    def __init__(self, model):
        super().__init__(model)

    def get_by_id(self, entity_id):
        """Obtiene un cliente por ID"""
        try:
            print(f"Controller get_by_id: {entity_id}")
            result = self.model.get_by_id(entity_id)
            print(f"Resultado de get_by_id: {result}")
            return result
        except EntityNotFoundError:
            print(f"Cliente no encontrado: {entity_id}")
            raise
        except Exception as e:
            print(f"Error en controller get_by_id: {e}")
            raise Exception(f"Error obteniendo cliente: {str(e)}")

    def get_all(self):
        """Obtiene todos los clientes"""
        try:
            result = self.model.get_all()
            print(f"Controller get_all: {len(result)} clientes")
            return result
        except Exception as e:
            print(f"Error en controller get_all: {e}")
            raise Exception(f"Error obteniendo clientes: {str(e)}")

    def create(self, form_data):
        """Crea un nuevo cliente"""
        try:
            print("Controller create - Datos recibidos:", form_data)

            # Validaciones básicas
            nombre_val = form_data.get('NOMBRE', '').strip()
            apellido_val = form_data.get('APELLIDO', '').strip()
            documento_val = form_data.get('DOCUMENTO_IDENTIDAD', '').strip()

            if not nombre_val:
                raise ValueError("Debe ingresar el nombre del cliente")
            if not apellido_val:
                raise ValueError("Debe ingresar el apellido del cliente")
            if not documento_val:
                raise ValueError("Debe ingresar el documento de identidad")

            # Validar campos numéricos
            try:
                documento_int = int(documento_val)
            except ValueError:
                raise ValueError("Documento de identidad debe ser un número entero")

            telefono_val = form_data.get('TELEFONO', '').strip()
            if telefono_val:
                try:
                    telefono_int = int(telefono_val)
                except ValueError:
                    raise ValueError("Teléfono debe ser un número entero")

            # Llamar al modelo
            new_id = self.model.create(form_data)
            print(f"Controller create - Nuevo ID: {new_id}")
            return new_id

        except ValueError as ve:
            print(f"Error de validación en controller: {ve}")
            raise ve
        except Exception as e:
            print(f"Error en controller create: {e}")
            raise Exception(f"Error creando cliente: {str(e)}")

    def update(self, entity_id, form_data):
        """Actualiza un cliente"""
        try:
            print(f"Controller update - ID: {entity_id}, datos: {form_data}")

            # Validaciones básicas
            nombre_val = form_data.get('NOMBRE', '').strip()
            apellido_val = form_data.get('APELLIDO', '').strip()
            documento_val = form_data.get('DOCUMENTO_IDENTIDAD', '').strip()

            if not nombre_val:
                raise ValueError("Debe ingresar el nombre del cliente")
            if not apellido_val:
                raise ValueError("Debe ingresar el apellido del cliente")
            if not documento_val:
                raise ValueError("Debe ingresar el documento de identidad")

            # Validar campos numéricos
            try:
                documento_int = int(documento_val)
            except ValueError:
                raise ValueError("Documento de identidad debe ser un número entero")

            telefono_val = form_data.get('TELEFONO', '').strip()
            if telefono_val:
                try:
                    telefono_int = int(telefono_val)
                except ValueError:
                    raise ValueError("Teléfono debe ser un número entero")

            # Llamar al modelo
            success = self.model.update(entity_id, form_data)
            print(f"Controller update - Resultado: {success}")
            return success

        except ValueError as ve:
            print(f"Error de validación en controller update: {ve}")
            raise ve
        except Exception as e:
            print(f"Error en controller update: {e}")
            raise Exception(f"Error actualizando cliente: {str(e)}")

    def delete(self, entity_id):
        """Elimina un cliente"""
        try:
            print(f"Controller delete - ID: {entity_id}")
            success = self.model.delete(entity_id)
            print(f"Controller delete - Resultado: {success}")
            return success
        except EntityNotFoundError as enfe:
            print(f"EntityNotFoundError en controller delete: {enfe}")
            raise enfe
        except Exception as e:
            print(f"Error en controller delete: {e}")
            raise Exception(f"Error eliminando cliente: {str(e)}")