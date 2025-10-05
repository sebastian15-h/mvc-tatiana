from controllers.base_controller import BaseController


class ParcelasController(BaseController):
    def __init__(self, model):
        super().__init__(model)

    def validate_parcela_data_for_ui(self, form_data):
        """
        Valida los datos del formulario de parcelas para la UI

        Args:
            form_data (dict): Datos del formulario

        Returns:
            tuple: (is_valid, errors)
        """
        errors = {}

        # Validar ID_PARCELA
        if not form_data.get('ID_PARCELA'):
            errors['id_parcela'] = "El ID de parcela es requerido"

        # Validar HECTAREAS
        if not form_data.get('AREA_HECTAREAS_PARCELA'):
            errors['hectareas'] = "Las hectáreas son requeridas"

        # Validar ID_FINCA
        if not form_data.get('ID_FINCA'):
            errors['id_finca'] = "El ID de finca es requerido"

        return (len(errors) == 0, errors)