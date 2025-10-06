from models.base_model import BaseModel
from utils.exceptions import EntityNotFoundError, DatabaseOperationError


class Clientes(BaseModel):
    """Modelo para gestionar clientes"""

    def __init__(self, db_connection):
        super().__init__(db_connection)
        self.table_name = "clientes"
        self.entity_name = "Cliente"

    def get_by_id(self, cliente_id):
        """Obtiene un cliente por su ID"""
        try:
            print(f"🔍 Buscando cliente ID: {cliente_id}")
            query = "SELECT * FROM clientes WHERE id_cliente = %s"
            results = self.db.execute_query(query, (cliente_id,))

            print(f"📊 Resultados de búsqueda: {results}")

            if not results:
                print(f"❌ Cliente {cliente_id} no encontrado")
                raise EntityNotFoundError(self.entity_name, cliente_id)

            print(f"✅ Cliente {cliente_id} encontrado")
            return self._map_cliente_data(results[0])

        except Exception as e:
            print(f"❌ Error en get_by_id: {e}")
            raise EntityNotFoundError(self.entity_name, cliente_id)

    def get_all(self):
        """Obtiene todos los clientes"""
        try:
            print("🔍 Obteniendo todos los clientes")
            query = "SELECT * FROM clientes ORDER BY id_cliente"
            results = self.db.execute_query(query)
            print(f"📊 Total de clientes encontrados: {len(results) if results else 0}")
            return [self._map_cliente_data(row) for row in results] if results else []

        except Exception as e:
            print(f"❌ Error en get_all: {e}")
            return []

    def create(self, form_data):
        """Crea un nuevo cliente"""
        try:
            print("🆕 Creando nuevo cliente")
            print(f"📝 Datos recibidos: {form_data}")

            # Extraer y validar datos
            nombre_val = form_data.get('NOMBRE', '').strip()
            apellido_val = form_data.get('APELLIDO', '').strip()
            documento_val = form_data.get('DOCUMENTO_IDENTIDAD', '').strip()
            nacionalidad_val = form_data.get('NACIONALIDAD', '').strip()
            fecha_nac_val = form_data.get('FECHA_NACIMIENTO', '').strip()
            direccion_val = form_data.get('DIRECCION', '').strip()
            telefono_val = form_data.get('TELEFONO', '').strip()
            correo_val = form_data.get('CORREO', '').strip()
            preferencias_val = form_data.get('PREFERENCIAS_ESPECIALES', '').strip()
            nivel_fidel_val = form_data.get('NIVEL_PROGRAMA_FIDELIZACION', '').strip()

            # Validaciones
            if not nombre_val:
                raise ValueError("Debe ingresar el nombre del cliente")
            if not apellido_val:
                raise ValueError("Debe ingresar el apellido del cliente")
            if not documento_val:
                raise ValueError("Debe ingresar el documento de identidad")

            # Preparar parámetros
            params = (
                nombre_val,
                apellido_val,
                int(documento_val) if documento_val else None,
                nacionalidad_val,
                fecha_nac_val,
                direccion_val,
                int(telefono_val) if telefono_val else None,
                correo_val,
                preferencias_val,
                nivel_fidel_val
            )

            print(f"📋 Parámetros para INSERT: {params}")

            # INSERT directo
            query = """
                INSERT INTO clientes 
                (nombre, apellido, documento_identidad, nacionalidad, fecha_nacimiento,
                 direccion, telefono, correo, preferencias_especiales, nivel_programa_fidelizacion)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            print(f"📝 Query: {query}")

            rows_affected = self.db.execute_query(query, params)
            print(f"✅ Filas insertadas: {rows_affected}")

            # Obtener el ID insertado
            result = self.db.execute_query("SELECT LAST_INSERT_ID()")
            new_id = result[0][0] if result else None
            print(f"✅ Nuevo ID insertado: {new_id}")

            return new_id

        except Exception as e:
            print(f"❌ Error en create: {e}")
            raise DatabaseOperationError(f"Error creando cliente: {str(e)}")

    def update(self, cliente_id, form_data):
        """Actualiza un cliente existente"""
        try:
            print(f"✏️ Actualizando cliente ID: {cliente_id}")
            print(f"📝 Datos recibidos: {form_data}")

            # Verificar que existe
            print(f"🔍 Verificando existencia del cliente {cliente_id}")
            existing = self.get_by_id(cliente_id)
            print(f"✅ Cliente existe: {existing}")

            # Extraer datos
            nombre_val = form_data.get('NOMBRE', '').strip()
            apellido_val = form_data.get('APELLIDO', '').strip()
            documento_val = form_data.get('DOCUMENTO_IDENTIDAD', '').strip()
            nacionalidad_val = form_data.get('NACIONALIDAD', '').strip()
            fecha_nac_val = form_data.get('FECHA_NACIMIENTO', '').strip()
            direccion_val = form_data.get('DIRECCION', '').strip()
            telefono_val = form_data.get('TELEFONO', '').strip()
            correo_val = form_data.get('CORREO', '').strip()
            preferencias_val = form_data.get('PREFERENCIAS_ESPECIALES', '').strip()
            nivel_fidel_val = form_data.get('NIVEL_PROGRAMA_FIDELIZACION', '').strip()

            # Preparar parámetros
            params = (
                nombre_val,
                apellido_val,
                int(documento_val) if documento_val else None,
                nacionalidad_val,
                fecha_nac_val,
                direccion_val,
                int(telefono_val) if telefono_val else None,
                correo_val,
                preferencias_val,
                nivel_fidel_val,
                cliente_id
            )

            print(f"📋 Parámetros para UPDATE: {params}")

            # UPDATE directo
            query = """
                UPDATE clientes 
                SET nombre = %s, apellido = %s, documento_identidad = %s,
                    nacionalidad = %s, fecha_nacimiento = %s, direccion = %s,
                    telefono = %s, correo = %s, preferencias_especiales = %s,
                    nivel_programa_fidelizacion = %s
                WHERE id_cliente = %s
            """
            print(f"📝 Query: {query}")

            rows_affected = self.db.execute_query(query, params)
            print(f"✅ Filas actualizadas: {rows_affected}")

            if rows_affected == 0:
                print(f"❌ No se actualizó ninguna fila para ID {cliente_id}")
                raise EntityNotFoundError(self.entity_name, cliente_id)

            print(f"✅ Cliente {cliente_id} actualizado correctamente")
            return True

        except EntityNotFoundError:
            print(f"❌ Cliente {cliente_id} no encontrado para actualizar")
            raise
        except Exception as e:
            print(f"❌ Error en update: {e}")
            raise DatabaseOperationError(f"Error actualizando cliente: {str(e)}")

    def delete(self, cliente_id):
        """Elimina un cliente"""
        try:
            print(f"🗑️ Eliminando cliente ID: {cliente_id}")

            # Verificar que existe
            print(f"🔍 Verificando existencia del cliente {cliente_id}")
            self.get_by_id(cliente_id)

            # DELETE directo
            query = "DELETE FROM clientes WHERE id_cliente = %s"
            print(f"📝 Query: {query}")

            rows_affected = self.db.execute_query(query, (cliente_id,))
            print(f"✅ Filas eliminadas: {rows_affected}")

            if rows_affected == 0:
                print(f"❌ No se eliminó ninguna fila para ID {cliente_id}")
                raise EntityNotFoundError(self.entity_name, cliente_id)

            print(f"✅ Cliente {cliente_id} eliminado correctamente")
            return True

        except EntityNotFoundError:
            print(f"❌ Cliente {cliente_id} no encontrado para eliminar")
            raise

    def _map_cliente_data(self, row):
        """Mapea una fila de la base de datos a un diccionario"""
        try:
            mapped_data = {
                'ID_CLIENTE': str(row[0]) if row[0] is not None else '',
                'NOMBRE': str(row[1]) if row[1] is not None else '',
                'APELLIDO': str(row[2]) if row[2] is not None else '',
                'DOCUMENTO_IDENTIDAD': str(row[3]) if row[3] is not None else '',
                'NACIONALIDAD': str(row[4]) if row[4] is not None else '',
                'FECHA_NACIMIENTO': str(row[5]) if row[5] is not None else '',
                'DIRECCION': str(row[6]) if row[6] is not None else '',
                'TELEFONO': str(row[7]) if row[7] is not None else '',
                'CORREO': str(row[8]) if row[8] is not None else '',
                'PREFERENCIAS_ESPECIALES': str(row[9]) if row[9] is not None else '',
                'NIVEL_PROGRAMA_FIDELIZACION': str(row[10]) if row[10] is not None else ''
            }
            print(f"🗺️ Datos mapeados: {mapped_data}")
            return mapped_data
        except Exception as e:
            print(f"❌ Error en mapeo de datos: {e}")
            print(f"📊 Fila recibida: {row}")
            return {}