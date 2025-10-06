from models.base_model import BaseModel
from utils.exceptions import EntityNotFoundError, DatabaseOperationError


class Hoteles(BaseModel):
    """Modelo para gestionar hoteles"""

    def __init__(self, db_connection):
        super().__init__(db_connection)
        self.table_name = "hoteles"
        self.entity_name = "Hotel"

    def get_by_id(self, hotel_id):
        """Obtiene un hotel por su ID"""
        try:
            query = "SELECT * FROM hoteles WHERE id_hotel = %s"
            results = self.db.execute_query(query, (hotel_id,))

            if not results:
                raise EntityNotFoundError(self.entity_name, hotel_id)

            return self._map_hotel_data(results[0])

        except Exception as e:
            raise EntityNotFoundError(self.entity_name, hotel_id)

    def get_all(self):
        """Obtiene todos los hoteles"""
        try:
            query = "SELECT * FROM hoteles ORDER BY id_hotel"
            results = self.db.execute_query(query)
            return [self._map_hotel_data(row) for row in results] if results else []

        except Exception as e:
            return []

    def create(self, form_data):
        """Crea un nuevo hotel"""
        try:
            # Extraer y validar datos
            nombre_val = form_data.get('NOMBRE_HOTEL', '').strip()
            categoria_val = form_data.get('CATEGORIA', '').strip()
            direccion_val = form_data.get('DIRECCION', '').strip()
            telefono_val = form_data.get('TELEFONO', '').strip()
            correo_val = form_data.get('CORREO', '').strip()
            año_inauguracion_val = form_data.get('AÑO_INAUGURACION', '').strip()
            habitantes_val = form_data.get('HABITANTES', '').strip()
            servicios_val = form_data.get('SERVICIOS', '').strip()
            checkin_val = form_data.get('CHECKIN', '').strip()
            checkout_val = form_data.get('CHECKOUT', '').strip()
            gerente_val = form_data.get('GERENTE', '').strip()

            # Validaciones
            if not nombre_val:
                raise ValueError("Debe ingresar el nombre del hotel")
            if not direccion_val:
                raise ValueError("Debe ingresar la dirección")

            # Preparar parámetros
            params = (
                nombre_val,
                int(categoria_val) if categoria_val else None,
                direccion_val,
                int(telefono_val) if telefono_val else None,
                correo_val,
                año_inauguracion_val,
                int(habitantes_val) if habitantes_val else None,
                servicios_val,
                checkin_val,
                checkout_val,
                gerente_val
            )

            # INSERT directo
            query = """
                INSERT INTO hoteles 
                (nombre_hotel, categoria, direccion, telefono, correo,
                 año_inauguracion, numero_total_habitantes, servicios_disponibles,
                 horarios_check_in, horarios_check_out, gerente_responsable)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            rows_affected = self.db.execute_query(query, params)
            print(f"✅ Filas insertadas: {rows_affected}")

            # Obtener el ID insertado
            result = self.db.execute_query("SELECT LAST_INSERT_ID()")
            new_id = result[0][0] if result else None

            return new_id

        except Exception as e:
            raise DatabaseOperationError(f"Error creando hotel: {str(e)}")

    def update(self, hotel_id, form_data):
        """Actualiza un hotel existente"""
        try:
            # Verificar que existe
            self.get_by_id(hotel_id)

            # Extraer datos
            nombre_val = form_data.get('NOMBRE_HOTEL', '').strip()
            categoria_val = form_data.get('CATEGORIA', '').strip()
            direccion_val = form_data.get('DIRECCION', '').strip()
            telefono_val = form_data.get('TELEFONO', '').strip()
            correo_val = form_data.get('CORREO', '').strip()
            año_inauguracion_val = form_data.get('AÑO_INAUGURACION', '').strip()
            habitantes_val = form_data.get('HABITANTES', '').strip()
            servicios_val = form_data.get('SERVICIOS', '').strip()
            checkin_val = form_data.get('CHECKIN', '').strip()
            checkout_val = form_data.get('CHECKOUT', '').strip()
            gerente_val = form_data.get('GERENTE', '').strip()

            # Preparar parámetros
            params = (
                nombre_val,
                int(categoria_val) if categoria_val else None,
                direccion_val,
                int(telefono_val) if telefono_val else None,
                correo_val,
                año_inauguracion_val,
                int(habitantes_val) if habitantes_val else None,
                servicios_val,
                checkin_val,
                checkout_val,
                gerente_val,
                hotel_id
            )

            # UPDATE directo
            query = """
                UPDATE hoteles 
                SET nombre_hotel = %s, categoria = %s, direccion = %s,
                    telefono = %s, correo = %s, año_inauguracion = %s,
                    numero_total_habitantes = %s, servicios_disponibles = %s,
                    horarios_check_in = %s, horarios_check_out = %s,
                    gerente_responsable = %s
                WHERE id_hotel = %s
            """

            rows_affected = self.db.execute_query(query, params)

            if rows_affected == 0:
                raise EntityNotFoundError(self.entity_name, hotel_id)

            return True

        except EntityNotFoundError:
            raise
        except Exception as e:
            raise DatabaseOperationError(f"Error actualizando hotel: {str(e)}")

    def delete(self, hotel_id):
        """Elimina un hotel"""
        try:
            # Verificar que existe
            self.get_by_id(hotel_id)

            # DELETE directo
            query = "DELETE FROM hoteles WHERE id_hotel = %s"
            rows_affected = self.db.execute_query(query, (hotel_id,))

            if rows_affected == 0:
                raise EntityNotFoundError(self.entity_name, hotel_id)

            return True

        except EntityNotFoundError:
            raise
        except Exception as e:
            raise DatabaseOperationError(f"Error eliminando hotel: {str(e)}")

    def _map_hotel_data(self, row):
        """Mapea una fila de la base de datos a un diccionario"""
        try:
            return {
                'ID_HOTEL': str(row[0]) if row[0] is not None else '',
                'NOMBRE_HOTEL': str(row[1]) if row[1] is not None else '',
                'CATEGORIA': str(row[2]) if row[2] is not None else '',
                'DIRECCION': str(row[3]) if row[3] is not None else '',
                'TELEFONO': str(row[4]) if row[4] is not None else '',
                'CORREO': str(row[5]) if row[5] is not None else '',
                'AÑO_INAUGURACION': str(row[6]) if row[6] is not None else '',
                'HABITANTES': str(row[7]) if row[7] is not None else '',
                'SERVICIOS': str(row[8]) if row[8] is not None else '',
                'CHECKIN': str(row[9]) if row[9] is not None else '',
                'CHECKOUT': str(row[10]) if row[10] is not None else '',
                'GERENTE': str(row[11]) if row[11] is not None else ''
            }
        except Exception as e:
            print(f"Error en mapeo de datos: {e}")
            return {}