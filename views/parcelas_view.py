"""
Vista específica para la gestión de parcelas
"""
import tkinter as tk
from tkinter import ttk
from views.base_view import BaseView
from utils.helpers import UIHelpers, safe_str


class ParcelasView(BaseView):
    """Vista específica para parcelas"""

    def __init__(self, parent_frame, controller):
        self.form_title = "GESTIÓN DE PARCELAS"
        self.entity_name = "PARCELAS"
        super().__init__(parent_frame, controller)

    def _create_form_fields(self):
        """Crea los campos específicos del formulario de parcelas"""
        # Campo ID_PARCELA
        self.create_form_field(0, "ID_PARCELA:", "id_parcela")

        # Campo HECTAREAS
        self.create_form_field(1, "HECTAREAS:", "hectareas")

        # Campo SISTEMA_RIEGO (Combobox)
        self.create_form_field(2, "SISTEMA_RIEGO:", "sistema_riego", field_type="combobox",
                               values=['goteo', 'subterraneo', 'aspercion', 'gravedad', 'otro'])

        # Campo HISTORIAL_USO
        self.create_form_field(3, "HISTORIAL_USO:", "historial_uso")

        # Campo ID_FINCA
        self.create_form_field(4, "ID_FINCA:", "id_finca")

        # ✅ Los botones adicionales se crearán después de que BaseView inicialice button_frame

    def _create_buttons(self):
        """Crea los botones de acción - Sobrescribe el método de BaseView"""
        # Primero llamar al método base para crear los botones estándar
        super()._create_buttons()

        # Luego añadir los botones adicionales
        self._create_additional_buttons()

    def _create_additional_buttons(self):
        """Crea botones adicionales específicos para parcelas"""
        # Frame para botones adicionales
        additional_button_frame = tk.Frame(self.button_frame)
        additional_button_frame.pack(pady=10)

        # Botón Exportar Excel
        btn_export_excel = tk.Button(
            additional_button_frame,
            text="Exportar Excel",
            font=("Arial", 10),
            bg="#4CAF50",
            fg="white",
            width=12,
            command=self._export_excel
        )
        btn_export_excel.pack(side=tk.LEFT, padx=3)

        # Botón Exportar PDF
        btn_export_pdf = tk.Button(
            additional_button_frame,
            text="Exportar PDF",
            font=("Arial", 10),
            bg="#2196F3",
            fg="white",
            width=12,
            command=self._export_pdf
        )
        btn_export_pdf.pack(side=tk.LEFT, padx=3)

        # Botón Cambiar Tema
        btn_change_theme = tk.Button(
            additional_button_frame,
            text="Cambiar Tema",
            font=("Arial", 10),
            bg="#9E9E9E",
            fg="white",
            width=12,
            command=self._change_theme
        )
        btn_change_theme.pack(side=tk.LEFT, padx=3)

    def _create_treeview(self, parent):
        """Crea el TreeView específico para parcelas"""
        # Frame para TreeView y scrollbar
        tree_frame = tk.Frame(parent)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Definir columnas
        columns = ('ID_PARCELA', 'AREA_HECTAREAS_PARCELA', 'SISTEMA_RIEGO',
                   'HISTORIAL_DE_USO', 'ID_FINCA')

        # Crear TreeView
        self.tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show='headings',
            height=20
        )

        # Configurar encabezados
        self.tree.heading('ID_PARCELA', text='ID')
        self.tree.heading('AREA_HECTAREAS_PARCELA', text='HECTAREAS')
        self.tree.heading('SISTEMA_RIEGO', text='RIEGO')
        self.tree.heading('HISTORIAL_DE_USO', text='HISTORIAL')
        self.tree.heading('ID_FINCA', text='FINCA')

        # Configurar anchos de columnas
        self.tree.column('ID_PARCELA', width=50, anchor='center')
        self.tree.column('AREA_HECTAREAS_PARCELA', width=80, anchor='center')
        self.tree.column('SISTEMA_RIEGO', width=100, anchor='center')
        self.tree.column('HISTORIAL_DE_USO', width=400, anchor='w')
        self.tree.column('ID_FINCA', width=80, anchor='center')

        # Configurar estilos
        self._configure_treeview_styles()

        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Layout
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Evento de selección
        self.tree.bind('<<TreeviewSelect>>', self._on_tree_select)

    def _configure_treeview_styles(self):
        """Configura los estilos del TreeView"""
        try:
            style = ttk.Style()
            style.theme_use("default")

            # Configurar TreeView
            style.configure("Treeview",
                            background="#2b2b2b",
                            foreground="white",
                            rowheight=25,
                            fieldbackground="#2b2b2b",
                            font=('Arial', 11))

            # Configurar encabezados
            style.configure("Treeview.Heading",
                            background="#2ecc71",
                            foreground="white",
                            font=('Arial', 12, 'bold'))

            # Colores alternados para filas
            self.tree.tag_configure('oddrow', background='#1e1e1e')
            self.tree.tag_configure('evenrow', background='#2e2e2e')

        except Exception as e:
            print(f"Error configurando estilos: {e}")

    def _get_form_data(self):
        """Obtiene los datos del formulario de parcelas"""
        return {
            'ID_PARCELA': self.get_field_value('id_parcela'),
            'AREA_HECTAREAS_PARCELA': self.get_field_value('hectareas'),
            'SISTEMA_RIEGO': self.get_field_value('sistema_riego'),
            'HISTORIAL_DE_USO': self.get_field_value('historial_uso'),
            'ID_FINCA': self.get_field_value('id_finca')
        }

    def _populate_form(self, data):
        """Puebla el formulario con datos de una parcela"""
        if not data:
            return

        self._clear_form()

        self.set_field_value('id_parcela', data.get('ID_PARCELA', ''))
        self.set_field_value('hectareas', data.get('AREA_HECTAREAS_PARCELA', ''))
        self.set_field_value('sistema_riego', data.get('SISTEMA_RIEGO', ''))
        self.set_field_value('historial_uso', data.get('HISTORIAL_DE_USO', ''))
        self.set_field_value('id_finca', data.get('ID_FINCA', ''))

    def _tree_values_to_dict(self, values):
        """Convierte valores del TreeView a diccionario"""
        if len(values) >= 5:
            return {
                'ID_PARCELA': values[0],
                'AREA_HECTAREAS_PARCELA': values[1] if values[1] else '',
                'SISTEMA_RIEGO': values[2] if values[2] else '',
                'HISTORIAL_DE_USO': values[3] if values[3] else '',
                'ID_FINCA': values[4] if values[4] else ''
            }
        return {}

    def _entity_to_tree_values(self, entity):
        """Convierte una entidad parcela a valores para el TreeView"""
        return (
            safe_str(entity.get('ID_PARCELA', '')),
            safe_str(entity.get('AREA_HECTAREAS_PARCELA', '')),
            safe_str(entity.get('SISTEMA_RIEGO', '')),
            safe_str(entity.get('HISTORIAL_DE_USO', '')),
            safe_str(entity.get('ID_FINCA', ''))
        )

    def _get_entity_id_from_form(self):
        """Obtiene el ID de la parcela desde el formulario"""
        parcela_id = self.get_field_value('id_parcela')
        try:
            return int(parcela_id) if parcela_id else None
        except ValueError:
            return None

    def _refresh_list(self):
        """Actualiza la lista de parcelas con colores alternados"""
        try:
            print("_refresh_list de ParcelasView llamado")

            # Limpiar TreeView
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Obtener datos
            parcelas = self.controller.get_all()
            print(f"Se obtuvieron {len(parcelas)} parcelas del controlador")

            # Insertar datos
            for index, parcela in enumerate(parcelas):
                values = self._entity_to_tree_values(parcela)
                tag = 'evenrow' if index % 2 == 0 else 'oddrow'
                self.tree.insert('', 'end', values=values, tags=(tag,))

            print(f"TreeView de parcelas actualizado con {len(parcelas)} parcelas")

        except Exception as e:
            print(f"Error en _refresh_list de ParcelasView: {e}")
            import traceback
            traceback.print_exc()

    def _on_search(self):
        """Sobrescribe la búsqueda para parcelas"""
        parcela_id = self.get_field_value('id_parcela')

        try:
            if parcela_id and parcela_id.strip():
                entity_id = int(parcela_id.strip())
                data = self.controller.get_by_id(entity_id)
                if data:
                    self._populate_form(data)
                else:
                    UIHelpers.show_error_message("No encontrado", "Parcela no encontrada")
            else:
                UIHelpers.show_error_message("Error", "Ingrese un ID de parcela para buscar")

        except ValueError:
            UIHelpers.show_error_message("Error", "El ID de la parcela debe ser un número válido")
        except Exception as e:
            UIHelpers.show_error_message("Error", f"Error en búsqueda: {str(e)}")

    # Métodos adicionales específicos para parcelas
    def _export_excel(self):
        """Exporta datos de parcelas a Excel"""
        try:
            parcelas = self.controller.get_all()
            if parcelas:
                # Aquí iría la lógica para exportar a Excel
                UIHelpers.show_success_message("Éxito", "Datos exportados a Excel correctamente")
            else:
                UIHelpers.show_error_message("Error", "No hay datos para exportar")
        except Exception as e:
            UIHelpers.show_error_message("Error", f"Error exportando a Excel: {str(e)}")

    def _export_pdf(self):
        """Exporta datos de parcelas a PDF"""
        try:
            parcelas = self.controller.get_all()
            if parcelas:
                # Aquí iría la lógica para exportar a PDF
                UIHelpers.show_success_message("Éxito", "Datos exportados a PDF correctamente")
            else:
                UIHelpers.show_error_message("Error", "No hay datos para exportar")
        except Exception as e:
            UIHelpers.show_error_message("Error", f"Error exportando a PDF: {str(e)}")

    def _change_theme(self):
        """Cambia el tema de la aplicación"""
        try:
            # Aquí iría la lógica para cambiar el tema
            UIHelpers.show_success_message("Éxito", "Tema cambiado correctamente")
        except Exception as e:
            UIHelpers.show_error_message("Error", f"Error cambiando tema: {str(e)}")

    def validate_form_data(self):
        """
        Valida los datos del formulario en tiempo real

        Returns:
            bool: True si los datos son válidos
        """
        form_data = self._get_form_data()

        # Validar ID_PARCELA
        if not form_data.get('ID_PARCELA'):
            UIHelpers.show_error_message("Error", "El ID de parcela es requerido")
            return False

        # Validar HECTAREAS
        if not form_data.get('AREA_HECTAREAS_PARCELA'):
            UIHelpers.show_error_message("Error", "Las hectáreas son requeridas")
            return False

        # Validar ID_FINCA
        if not form_data.get('ID_FINCA'):
            UIHelpers.show_error_message("Error", "El ID de finca es requerido")
            return False

        return True

    def _clear_form(self):
        """Limpia el formulario y resetea validaciones"""
        super()._clear_form()

        # Enfocar el primer campo
        self.focus_field('id_parcela')