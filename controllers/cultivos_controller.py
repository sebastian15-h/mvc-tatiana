from controllers.base_controller import BaseController
from utils.exceptions import EntityNotFoundError, EntityInUseError, DatabaseOperationError


class CultivosController(BaseController):
    def __init__(self, model):
        super().__init__(model)

    def get_by_id(self, entity_id):
        """Obtiene un cultivo por ID"""
        try:
            print(f"Controller get_by_id: {entity_id}")
            result = self.model.get_by_id(entity_id)
            print(f"Resultado de get_by_id: {result}")
            return result
        except EntityNotFoundError:
            print(f"Cultivo no encontrado: {entity_id}")
            raise
        except Exception as e:
            print(f"Error en controller get_by_id: {e}")
            raise Exception(f"Error obteniendo cultivo: {str(e)}")

    def get_all(self):
        """Obtiene todos los cultivos"""
        try:
            result = self.model.get_all()
            print(f"Controller get_all: {len(result)} cultivos")
            return result
        except Exception as e:
            print(f"Error en controller get_all: {e}")
            raise Exception(f"Error obteniendo cultivos: {str(e)}")

    def create(self, form_data):
        """Crea un nuevo cultivo"""
        try:
            print("Controller create - Datos recibidos:", form_data)

            # Validaciones básicas en controlador
            nombre_cientifico = form_data.get('NOMBRE_CIENTIFICO', '').strip()
            nombre_comun = form_data.get('NOMBRE_COMUN', '').strip()
            tiempo_crecimiento = form_data.get('TIEMPO_CRECIMIENTO_DIAS', '').strip()
            temperaturas_optimas = form_data.get('TEMPERATURAS_OPTIMAS', '').strip()

            if not nombre_cientifico:
                raise ValueError("Debe ingresar el nombre científico")
            if not nombre_comun:
                raise ValueError("Debe ingresar el nombre común")
            if not tiempo_crecimiento:
                raise ValueError("Debe ingresar el tiempo de crecimiento (días)")
            if not temperaturas_optimas:
                raise ValueError("Debe ingresar la temperatura óptima")

            # Validar numéricos
            try:
                tiempo_int = int(tiempo_crecimiento)
                if tiempo_int <= 0:
                    raise ValueError("Tiempo de crecimiento debe ser mayor a 0")
            except ValueError:
                raise ValueError("Tiempo de crecimiento debe ser número entero válido")

            try:
                temp_float = float(temperaturas_optimas)
            except ValueError:
                raise ValueError("Temperatura óptima debe ser número válido")

            # Pasar form_data completo al modelo
            new_id = self.model.create(form_data)
            print(f"Controller create - Nuevo ID: {new_id}")
            return new_id

        except ValueError as ve:
            print(f"Error de validación en controller: {ve}")
            raise ve
        except Exception as e:
            print(f"Error en controller create: {e}")
            raise Exception(f"Error creando cultivo: {str(e)}")

    def update(self, entity_id, form_data):
        """Actualiza un cultivo"""
        try:
            print(f"Controller update - ID: {entity_id}, datos: {form_data}")

            # Validaciones básicas
            nombre_cientifico = form_data.get('NOMBRE_CIENTIFICO', '').strip()
            nombre_comun = form_data.get('NOMBRE_COMUN', '').strip()
            tiempo_crecimiento = form_data.get('TIEMPO_CRECIMIENTO_DIAS', '').strip()
            temperaturas_optimas = form_data.get('TEMPERATURAS_OPTIMAS', '').strip()

            if not nombre_cientifico:
                raise ValueError("Debe ingresar el nombre científico")
            if not nombre_comun:
                raise ValueError("Debe ingresar el nombre común")
            if not tiempo_crecimiento:
                raise ValueError("Debe ingresar el tiempo de crecimiento (días)")
            if not temperaturas_optimas:
                raise ValueError("Debe ingresar la temperatura óptima")

            # Validar numéricos
            try:
                tiempo_int = int(tiempo_crecimiento)
                if tiempo_int <= 0:
                    raise ValueError("Tiempo de crecimiento debe ser mayor a 0")
            except ValueError:
                raise ValueError("Tiempo de crecimiento debe ser número entero válido")

            try:
                temp_float = float(temperaturas_optimas)
            except ValueError:
                raise ValueError("Temperatura óptima debe ser número válido")

            # Pasar form_data completo al modelo
            success = self.model.update(entity_id, form_data)
            print(f"Controller update - Resultado: {success}")
            return success

        except ValueError as ve:
            print(f"Error de validación en controller update: {ve}")
            raise ve
        except Exception as e:
            print(f"Error en controller update: {e}")
            raise Exception(f"Error actualizando cultivo: {str(e)}")

    def delete(self, entity_id):
        """Elimina un cultivo"""
        try:
            print(f"Controller delete - ID: {entity_id}")
            success = self.model.delete(entity_id)
            print(f"Controller delete - Resultado: {success}")
            return success
        except EntityNotFoundError as enfe:
            print(f"EntityNotFoundError en controller delete: {enfe}")
            raise enfe
        except EntityInUseError as eiue:
            print(f"EntityInUseError en controller delete: {eiue}")
            raise eiue
        except Exception as e:
            print(f"Error en controller delete: {e}")
            raise Exception(f"Error eliminando cultivo: {str(e)}")