from models.base_model import BaseModel
from utils.exceptions import EntityNotFoundError, EntityInUseError, DatabaseOperationError


class Cultivos(BaseModel):
    """Modelo para gestionar cultivos"""

    def __init__(self, db_connection):
        super().__init__(db_connection)
        self.table_name = "cultivos"
        self.entity_name = "Cultivo"

    def get_by_id(self, cultivo_id):
        """Obtiene un cultivo por su ID"""
        try:
            print(f"🔍 Buscando cultivo ID: {cultivo_id}")
            query = "SELECT * FROM cultivos WHERE id_cultivo = %s"
            results = self.db.execute_query(query, (cultivo_id,))

            print(f"📊 Resultados de búsqueda: {results}")

            if not results:
                print(f"❌ Cultivo {cultivo_id} no encontrado")
                raise EntityNotFoundError(self.entity_name, cultivo_id)

            print(f"✅ Cultivo {cultivo_id} encontrado")
            return self._map_cultivo_data(results[0])

        except Exception as e:
            print(f"❌ Error en get_by_id: {e}")
            raise EntityNotFoundError(self.entity_name, cultivo_id)

    def get_all(self):
        """Obtiene todos los cultivos"""
        try:
            print("🔍 Obteniendo todos los cultivos")
            query = "SELECT * FROM cultivos ORDER BY id_cultivo"
            results = self.db.execute_query(query)
            print(f"📊 Total de cultivos encontrados: {len(results) if results else 0}")
            return [self._map_cultivo_data(row) for row in results] if results else []

        except Exception as e:
            print(f"❌ Error en get_all: {e}")
            return []

    def create(self, form_data):
        """Crea un nuevo cultivo"""
        try:
            print("🆕 Creando nuevo cultivo")
            print(f"📝 Datos recibidos: {form_data}")

            # Extraer datos del form_data
            nombre_cientifico = form_data.get('NOMBRE_CIENTIFICO', '').strip()
            nombre_comun = form_data.get('NOMBRE_COMUN', '').strip()
            tiempo_crecimiento = form_data.get('TIEMPO_CRECIMIENTO_DIAS', '').strip()
            temperaturas_optimas = form_data.get('TEMPERATURAS_OPTIMAS', '').strip()
            requerimiento_agua = form_data.get('REQUERIMIENTO_AGUA_SEMANAL', '').strip()
            photo = form_data.get('PHOTO', '').strip()

            # Validaciones
            if not nombre_cientifico:
                raise ValueError("Debe ingresar el nombre científico")
            if not nombre_comun:
                raise ValueError("Debe ingresar el nombre común")

            # Preparar parámetros
            params = (
                nombre_cientifico,
                nombre_comun,
                int(tiempo_crecimiento) if tiempo_crecimiento else 0,
                float(temperaturas_optimas) if temperaturas_optimas else 0.0,
                requerimiento_agua if requerimiento_agua else '',
                photo if photo else ''
            )

            print(f"📋 Parámetros para INSERT: {params}")

            # INSERT directo
            query = """
                INSERT INTO cultivos 
                (nombre_cientifico, nombre_comun, tiempo_crecimiento_dias,
                 temperaturas_optimas, requerimiento_agua_semanal, photo)
                VALUES (%s, %s, %s, %s, %s, %s)
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
            raise DatabaseOperationError(f"Error creando cultivo: {str(e)}")

    def update(self, cultivo_id, form_data):
        """Actualiza un cultivo existente"""
        try:
            print(f"✏️ Actualizando cultivo ID: {cultivo_id}")
            print(f"📝 Datos recibidos: {form_data}")

            # Verificar que el cultivo existe
            print(f"🔍 Verificando existencia del cultivo {cultivo_id}")
            existing = self.get_by_id(cultivo_id)
            print(f"✅ Cultivo existe: {existing}")

            # Extraer datos
            nombre_cientifico = form_data.get('NOMBRE_CIENTIFICO', '').strip()
            nombre_comun = form_data.get('NOMBRE_COMUN', '').strip()
            tiempo_crecimiento = form_data.get('TIEMPO_CRECIMIENTO_DIAS', '').strip()
            temperaturas_optimas = form_data.get('TEMPERATURAS_OPTIMAS', '').strip()
            requerimiento_agua = form_data.get('REQUERIMIENTO_AGUA_SEMANAL', '').strip()
            photo = form_data.get('PHOTO', '').strip()

            # Preparar parámetros
            params = (
                nombre_cientifico,
                nombre_comun,
                int(tiempo_crecimiento) if tiempo_crecimiento else 0,
                float(temperaturas_optimas) if temperaturas_optimas else 0.0,
                requerimiento_agua if requerimiento_agua else '',
                photo if photo else '',
                cultivo_id
            )

            print(f"📋 Parámetros para UPDATE: {params}")

            # UPDATE directo
            query = """
                UPDATE cultivos 
                SET nombre_cientifico = %s, nombre_comun = %s, 
                    tiempo_crecimiento_dias = %s, temperaturas_optimas = %s,
                    requerimiento_agua_semanal = %s, photo = %s
                WHERE id_cultivo = %s
            """
            print(f"📝 Query: {query}")

            rows_affected = self.db.execute_query(query, params)
            print(f"✅ Filas actualizadas: {rows_affected}")

            if rows_affected == 0:
                print(f"❌ No se actualizó ninguna fila para ID {cultivo_id}")
                raise EntityNotFoundError(self.entity_name, cultivo_id)

            print(f"✅ Cultivo {cultivo_id} actualizado correctamente")
            return True

        except EntityNotFoundError:
            print(f"❌ Cultivo {cultivo_id} no encontrado para actualizar")
            raise
        except Exception as e:
            print(f"❌ Error en update: {e}")
            raise DatabaseOperationError(f"Error actualizando cultivo: {str(e)}")

    def delete(self, cultivo_id):
        """Elimina un cultivo"""
        try:
            print(f"🗑️ Eliminando cultivo ID: {cultivo_id}")

            # Verificar que existe
            print(f"🔍 Verificando existencia del cultivo {cultivo_id}")
            self.get_by_id(cultivo_id)

            # DELETE directo
            query = "DELETE FROM cultivos WHERE id_cultivo = %s"
            print(f"📝 Query: {query}")

            rows_affected = self.db.execute_query(query, (cultivo_id,))
            print(f"✅ Filas eliminadas: {rows_affected}")

            if rows_affected == 0:
                print(f"❌ No se eliminó ninguna fila para ID {cultivo_id}")
                raise EntityNotFoundError(self.entity_name, cultivo_id)

            print(f"✅ Cultivo {cultivo_id} eliminado correctamente")
            return True

        except EntityNotFoundError:
            print(f"❌ Cultivo {cultivo_id} no encontrado para eliminar")
            raise
        except Exception as e:
            error_msg = str(e).lower()
            print(f"❌ Error en delete: {e}")
            if "tiene parcelas asociadas" in error_msg or "foreign key" in error_msg:
                raise EntityInUseError(self.entity_name, cultivo_id, "parcelas")
            else:
                raise DatabaseOperationError(f"Error eliminando cultivo: {str(e)}")

    def _map_cultivo_data(self, row):
        """Mapea una fila de la base de datos a un diccionario"""
        try:
            mapped_data = {
                'ID_CULTIVO': str(row[0]) if row[0] is not None else '',
                'NOMBRE_CIENTIFICO': str(row[1]) if row[1] is not None else '',
                'NOMBRE_COMUN': str(row[2]) if row[2] is not None else '',
                'TIEMPO_CRECIMIENTO_DIAS': str(row[3]) if row[3] is not None else '',
                'TEMPERATURAS_OPTIMAS': str(row[4]) if row[4] is not None else '',
                'REQUERIMIENTO_AGUA_SEMANAL': str(row[5]) if row[5] is not None else '',
                'PHOTO': str(row[6]) if row[6] is not None else ''
            }
            print(f"🗺️ Datos mapeados: {mapped_data}")
            return mapped_data
        except Exception as e:
            print(f"❌ Error en mapeo de datos: {e}")
            print(f"📊 Fila recibida: {row}")
            return {}