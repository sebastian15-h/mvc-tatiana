from models.base_model import BaseModel
from utils.exceptions import EntityNotFoundError, EntityInUseError, DatabaseOperationError
from utils.validators import Validator


class Parcelas(BaseModel):
    """Modelo para gestionar parcelas"""

    def __init__(self, db_connection):
        super().__init__(db_connection)
        self.table_name = "PARCELAS"
        self.entity_name = "Parcela"
        self.field_mapping = [
            'ID_PARCELA', 'AREA_HECTAREAS_PARCELA', 'SISTEMA_RIEGO',
            'HISTORIAL_DE_USO', 'ID_FINCA'
        ]

    def create(self, area_hectareas_parcela, sistema_riego=None, historial_de_uso=None, id_finca=None):
        """
        Crea una nueva parcela

        Args:
            area_hectareas_parcela (str): Área en hectáreas (requerido)
            sistema_riego (str): Sistema de riego (opcional)
            historial_de_uso (str): Historial de uso (opcional)
            id_finca (str): ID de la finca (opcional)

        Returns:
            int: ID de la parcela creada
        """
        validated_data = self._validate_parcela_data(
            area_hectareas_parcela, sistema_riego, historial_de_uso, id_finca
        )

        parameters = (
            validated_data['area_hectareas_parcela'],
            validated_data['sistema_riego'],
            validated_data['historial_de_uso'],
            validated_data['id_finca']
        )

        try:
            results = self.call_procedure('sp_InsertParcela', parameters)
            if results and len(results) > 0:
                return results[0][0]  # ID de la parcela creada
        except:
            # Fallback a consulta directa
            query = """
                INSERT INTO PARCELAS (AREA_HECTAREAS_PARCELA, SISTEMA_RIEGO, HISTORIAL_DE_USO, ID_FINCA)
                VALUES (?, ?, ?, ?)
            """
            self.db.execute_query(query, parameters)
            # Obtener el último ID insertado
            result = self.db.execute_query("SELECT @@IDENTITY")
            return result[0][0] if result else None

        raise DatabaseOperationError("No se pudo obtener el ID de la parcela creada")

    def get_by_id(self, parcela_id):
        """
        Obtiene una parcela por su ID

        Args:
            parcela_id (int): ID de la parcela

        Returns:
            dict: Datos de la parcela
        """
        validated_id = Validator.validate_integer(
            str(parcela_id), "ID de la Parcela", allow_empty=False, min_value=1
        )

        try:
            results = self.call_procedure('sp_GetParcelaById', (validated_id,))
        except:
            # Fallback a consulta directa
            query = "SELECT * FROM PARCELAS WHERE ID_PARCELA = ?"
            results = self.db.execute_query(query, (validated_id,))

        if not results:
            raise EntityNotFoundError(self.entity_name, parcela_id)

        return self._format_entity_data(results[0], self.field_mapping)

    def update(self, parcela_id, area_hectareas_parcela, sistema_riego=None, historial_de_uso=None, id_finca=None):
        """
        Actualiza una parcela existente

        Args:
            parcela_id (int): ID de la parcela
            area_hectareas_parcela (str): Área en hectáreas
            sistema_riego (str): Sistema de riego (opcional)
            historial_de_uso (str): Historial de uso (opcional)
            id_finca (str): ID de la finca (opcional)

        Returns:
            bool: True si se actualizó correctamente
        """
        validated_id = Validator.validate_integer(
            str(parcela_id), "ID de la Parcela", allow_empty=False, min_value=1
        )

        validated_data = self._validate_parcela_data(
            area_hectareas_parcela, sistema_riego, historial_de_uso, id_finca
        )

        parameters = (
            validated_id,
            validated_data['area_hectareas_parcela'],
            validated_data['sistema_riego'],
            validated_data['historial_de_uso'],
            validated_data['id_finca']
        )

        try:
            self.call_procedure('sp_UpdateParcela', parameters)
        except:
            # Fallback a consulta directa
            query = """
                UPDATE PARCELAS 
                SET AREA_HECTAREAS_PARCELA = ?, SISTEMA_RIEGO = ?, 
                    HISTORIAL_DE_USO = ?, ID_FINCA = ?
                WHERE ID_PARCELA = ?
            """
            self.db.execute_query(query, parameters)

        return True

    def delete(self, parcela_id):
        """
        Elimina una parcela

        Args:
            parcela_id (int): ID de la parcela

        Returns:
            bool: True si se eliminó correctamente
        """
        validated_id = Validator.validate_integer(
            str(parcela_id), "ID de la Parcela", allow_empty=False, min_value=1
        )

        try:
            self.call_procedure('sp_DeleteParcela', (validated_id,))
            return True
        except Exception as e:
            error_msg = str(e).lower()
            if "tiene cultivos asociados" in error_msg or "cultivos" in error_msg:
                raise EntityInUseError(self.entity_name, parcela_id, "cultivos")
            # Fallback a consulta directa
            query = "DELETE FROM PARCELAS WHERE ID_PARCELA = ?"
            self.db.execute_query(query, (validated_id,))
            return True

    def get_all(self):
        """
        Obtiene todas las parcelas

        Returns:
            list: Lista de diccionarios con datos de parcelas
        """
        try:
            print("🔍 Modelo Parcelas: Ejecutando get_all()...")

            # Intentar diferentes procedimientos almacenados
            try:
                results = self.call_procedure('sp_GetAllParcelas', ())
                print("✅ Usando sp_GetAllParcelas")
            except Exception as e1:
                try:
                    print("⚠️ sp_GetAllParcelas falló, intentando sp_GetParcelas...")
                    results = self.call_procedure('sp_GetParcelas', ())
                    print("✅ Usando sp_GetParcelas")
                except Exception as e2:
                    # Consulta directa como último recurso
                    print("⚠️ Todos los procedimientos fallaron, usando consulta directa...")
                    query = "SELECT * FROM PARCELAS"
                    results = self.db.execute_query(query)
                    print("✅ Usando consulta directa")

            print(f"📊 Modelo Parcelas: Resultados obtenidos: {len(results)} filas")

            if results:
                formatted_results = []
                for row in results:
                    formatted_parcela = self._format_entity_data(row, self.field_mapping)
                    formatted_results.append(formatted_parcela)

                print(f"✅ Modelo Parcelas: {len(formatted_results)} parcelas formateadas")
                return formatted_results
            else:
                print("⚠️ Modelo Parcelas: No se obtuvieron resultados")
                return []

        except Exception as e:
            print(f"❌ Error en Modelo Parcelas get_all(): {e}")
            import traceback
            traceback.print_exc()
            return []

    def search(self, search_term):
        """
        Busca parcelas por término

        Args:
            search_term (str): Término de búsqueda

        Returns:
            list: Lista de parcelas que coinciden
        """
        if not search_term or not search_term.strip():
            return []

        try:
            results = self.call_procedure('sp_SearchParcelas', (search_term.strip(),))
        except:
            # Fallback a consulta directa
            query = """
                SELECT * FROM PARCELAS 
                WHERE AREA_HECTAREAS_PARCELA LIKE ? OR SISTEMA_RIEGO LIKE ? 
                   OR HISTORIAL_DE_USO LIKE ? OR ID_FINCA LIKE ?
            """
            search_pattern = f"%{search_term}%"
            results = self.db.execute_query(query, (search_pattern, search_pattern, search_pattern, search_pattern))

        return [self._format_entity_data(row, self.field_mapping) for row in results]

    def _validate_parcela_data(self, area_hectareas_parcela, sistema_riego, historial_de_uso, id_finca):
        """
        Valida los datos de una parcela

        Args:
            area_hectareas_parcela (str): Área en hectáreas
            sistema_riego (str): Sistema de riego
            historial_de_uso (str): Historial de uso
            id_finca (str): ID de la finca

        Returns:
            dict: Datos validados
        """
        validated_data = {}

        validated_data['area_hectareas_parcela'] = Validator.validate_string_length(
            area_hectareas_parcela, "Área en Hectáreas", min_length=1, max_length=20, allow_empty=False
        )

        validated_data['sistema_riego'] = Validator.validate_string_length(
            sistema_riego if sistema_riego is not None else "",
            "Sistema de Riego", max_length=50, allow_empty=True
        )

        validated_data['historial_de_uso'] = Validator.validate_string_length(
            historial_de_uso if historial_de_uso is not None else "",
            "Historial de Uso", max_length=500, allow_empty=True
        )

        validated_data['id_finca'] = Validator.validate_string_length(
            id_finca if id_finca is not None else "",
            "ID Finca", max_length=10, allow_empty=True
        )

        return validated_data