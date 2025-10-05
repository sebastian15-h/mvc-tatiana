"""
Vista específica para la gestión de fincas
"""
import tkinter as tk
from tkinter import ttk
from views.base_view import BaseView
from utils.helpers import UIHelpers, safe_str


class FincasView(BaseView):
    """Vista específica para fincas"""

    def __init__(self, parent_frame, controller):
        self.form_title = "GESTIÓN DE FINCAS"
        self.entity_name = "FINCAS"
        super().__init__(parent_frame, controller)

    def _create_treeview(self, parent):
        """Crea el TreeView específico para fincas"""
        self.create_treeview_fincas(parent)

    def _get_form_data(self):
        """Obtiene los datos del formulario de fincas"""
        return {
            'ID_finca': self.get_field_value('id_finca'),
            'NOMBRE': self.get_field_value('nombre'),
            'latitud': self.get_field_value('latitud'),
            'longitud': self.get_field_value('longitud'),
            'EXTENSION_TOTAL_HECTAREAS': self.get_field_value('extension_total_hectareas'),
            'ALTITUD_METROS': self.get_field_value('altitud_metros'),
            'TEMPERATURA_PROMEDIO_ANUAL_fg': self.get_field_value('temperatura_promedio_anual'),
            'TIPO_SUELO_PREDOMINANTE': self.get_field_value('tipo_suelo_predominante'),
            'region_ubicacion': self.get_field_value('region_ubicacion')
        }

    def _populate_form(self, data):
        """Puebla el formulario con datos de una finca"""
        if not data:
            return

        self._clear_form()

        self.set_field_value('id_finca', data.get('ID_finca', ''))
        self.set_field_value('nombre', data.get('NOMBRE', ''))
        self.set_field_value('latitud', data.get('latitud', ''))
        self.set_field_value('longitud', data.get('longitud', ''))
        self.set_field_value('extension_total_hectareas', data.get('EXTENSION_TOTAL_HECTAREAS', ''))
        self.set_field_value('altitud_metros', data.get('ALTITUD_METROS', ''))
        self.set_field_value('temperatura_promedio_anual', data.get('TEMPERATURA_PROMEDIO_ANUAL_fg', ''))
        self.set_field_value('tipo_suelo_predominante', data.get('TIPO_SUELO_PREDOMINANTE', ''))
        self.set_field_value('region_ubicacion', data.get('region_ubicacion', ''))

    def _tree_values_to_dict(self, values):
        """Convierte los valores del TreeView de fincas a un diccionario"""
        if len(values) >= 5:
            return {
                'ID_finca': values[0],
                'NOMBRE': values[1],
                'latitud': values[2] if values[2] else '',
                'longitud': values[3] if values[3] else '',
                'EXTENSION_TOTAL_HECTAREAS': values[4] if values[4] else '',
                'ALTITUD_METROS': '',
                'TEMPERATURA_PROMEDIO_ANUAL_fg': '',
                'TIPO_SUELO_PREDOMINANTE': '',
                'region_ubicacion': ''
            }
        return {}

    def _entity_to_tree_values(self, entity):
        """Convierte una entidad finca a valores para insertar en el TreeView"""
        return (
            safe_str(entity.get('ID_finca', '')),
            safe_str(entity.get('NOMBRE', '')),
            safe_str(entity.get('latitud', '')),
            safe_str(entity.get('longitud', '')),
            safe_str(entity.get('EXTENSION_TOTAL_HECTAREAS', ''))
        )

    def _get_entity_id_from_form(self):
        """Obtiene el ID de la finca desde el formulario"""
        finca_id = self.get_field_value('id_finca')
        try:
            return int(finca_id) if finca_id else None
        except ValueError:
            return None

    def _refresh_list(self):
        """Actualiza la lista de fincas"""
        try:
            print("_refresh_list llamado - actualizando TreeView...")

            # Limpiar TreeView
            for item in self.fincas_tree.get_children():
                self.fincas_tree.delete(item)

            # Obtener datos del controlador
            fincas = self.controller.get_all()
            print(f"Se obtuvieron {len(fincas)} fincas del controlador")

            # Insertar datos
            for index, finca in enumerate(fincas):
                values = self._entity_to_tree_values(finca)
                tag = 'evenrow' if index % 2 == 0 else 'oddrow'
                self.fincas_tree.insert('', 'end', values=values, tags=(tag,))

            print(f"TreeView actualizado con {len(fincas)} fincas")

        except Exception as e:
            print(f"Error en _refresh_list: {e}")
            import traceback
            traceback.print_exc()

    # Mantén el resto de tus métodos personalizados pero elimina los duplicados
    def _create_form_fields(self):
        """Crea los campos específicos del formulario de fincas"""
        # Campo ID_finca
        self.create_form_field(0, "ID FINCA:", "id_finca")

        # Campo NOMBRE (requerido)
        self.create_form_field(1, "NOMBRE:", "nombre")

        # Campo latitud
        self.create_form_field(2, "LATITUD:", "latitud")

        # Campo longitud
        self.create_form_field(3, "LONGITUD:", "longitud")

        # Campo EXTENSION_TOTAL_HECTAREAS
        self.create_form_field(4, "EXTENSIÓN TOTAL (HECTÁREAS):", "extension_total_hectareas")

        # Campo ALTITUD_METROS
        self.create_form_field(5, "ALTITUD (METROS):", "altitud_metros")

        # Campo TEMPERATURA_PROMEDIO_ANUAL
        self.create_form_field(6, "TEMPERATURA PROMEDIO ANUAL (°C):", "temperatura_promedio_anual")

        # Campo TIPO_SUELO_PREDOMINANTE
        self.create_form_field(7, "TIPO SUELO PREDOMINANTE:", "tipo_suelo_predominante")

        # Campo region_ubicacion
        self.create_form_field(8, "REGIÓN UBICACIÓN:", "region_ubicacion")

        # Etiqueta de campos requeridos
        required_label = tk.Label(
            self.form_frame,
            text="* Campos requeridos",
            font=("Arial", 9),
            fg="red"
        )
        required_label.grid(row=9, column=0, columnspan=2, sticky="w", pady=(10, 0))

    def create_treeview_fincas(self, parent):
        """Crea el TreeView específico para mostrar las fincas"""
        try:
            print("Creando TreeView de fincas...")

            # Frame principal simple
            main_frame = tk.Frame(parent)
            main_frame.pack(fill="both", expand=True, padx=10, pady=10)

            # Definir columnas
            columns = ('ID_finca', 'NOMBRE', 'latitud', 'longitud', 'EXTENSION_TOTAL_HECTAREAS')

            # Crear TreeView
            self.fincas_tree = ttk.Treeview(
                main_frame,
                columns=columns,
                show='headings',
                height=12
            )

            # Configurar encabezados básicos
            self.fincas_tree.heading('ID_finca', text='ID')
            self.fincas_tree.heading('NOMBRE', text='Nombre')
            self.fincas_tree.heading('latitud', text='Latitud')
            self.fincas_tree.heading('longitud', text='Longitud')
            self.fincas_tree.heading('EXTENSION_TOTAL_HECTAREAS', text='Hectáreas')

            # Configurar columnas
            self.fincas_tree.column('ID_finca', width=60, anchor='center')
            self.fincas_tree.column('NOMBRE', width=150, anchor='w')
            self.fincas_tree.column('latitud', width=80, anchor='center')
            self.fincas_tree.column('longitud', width=80, anchor='center')
            self.fincas_tree.column('EXTENSION_TOTAL_HECTAREAS', width=100, anchor='center')

            # Empacar el TreeView primero
            self.fincas_tree.pack(side="left", fill="both", expand=True)

            # Scrollbar
            scrollbar = ttk.Scrollbar(main_frame, orient="vertical")
            scrollbar.pack(side="right", fill="y")

            # Configurar la conexión entre TreeView y scrollbar
            self.fincas_tree.configure(yscrollcommand=scrollbar.set)
            scrollbar.configure(command=self.fincas_tree.yview)

            print("TreeView y scrollbar creados exitosamente")

            # Configurar estilos básicos
            self._configure_treeview_styles()

            # Evento de selección
            self.fincas_tree.bind('<<TreeviewSelect>>', self._on_finca_select)

            # Cargar datos inmediatamente
            self._refresh_list()

        except Exception as e:
            print(f"Error crítico creando TreeView: {e}")
            import traceback
            traceback.print_exc()

    def _configure_treeview_styles(self):
        """Configura los estilos del TreeView"""
        try:
            style = ttk.Style()
            style.theme_use("default")

            style.configure("Treeview",
                            background="black",
                            foreground="white",
                            fieldbackground="black",
                            rowheight=25,
                            font=('Calibri', 10))

            style.configure("Treeview.Heading",
                            background="black",
                            foreground="green",
                            font=('Arial', 11, 'bold'))

            # Colores alternados para filas
            self.fincas_tree.tag_configure('oddrow', background='#1e1e1e')
            self.fincas_tree.tag_configure('evenrow', background='#2e2e2e')

        except Exception as e:
            print(f"Error configurando estilos: {e}")

    def _on_finca_select(self, event):
        """Maneja la selección de una finca en el TreeView"""
        try:
            selected = self.fincas_tree.selection()
            if not selected:
                return

            selected_item = selected[0]
            values = self.fincas_tree.item(selected_item, 'values')

            if values:
                finca_data = self._tree_values_to_dict(values)
                self._populate_form(finca_data)

        except Exception as e:
            print(f"Error en selección de finca: {e}")

    def export_fincas_summary(self):
        """Exporta un resumen de fincas"""
        try:
            fincas = self.controller.get_all()
            regiones = {}
            suelos = {}

            for finca in fincas:
                region = finca.get('region_ubicacion', 'Sin especificar')
                suelo = finca.get('TIPO_SUELO_PREDOMINANTE', 'Sin especificar')

                regiones[region] = regiones.get(region, 0) + 1
                suelos[suelo] = suelos.get(suelo, 0) + 1

            # Crear ventana de resumen
            summary_window = tk.Toplevel(self.parent_frame)
            summary_window.title("Resumen de Fincas")
            summary_window.geometry("500x400")
            summary_window.transient(self.parent_frame)

            UIHelpers.center_window(summary_window, 500, 400)

            # Texto del resumen
            summary_text = tk.Text(summary_window, font=("Arial", 10), wrap=tk.WORD)
            scrollbar = ttk.Scrollbar(summary_window, orient="vertical", command=summary_text.yview)

            summary_text.configure(yscrollcommand=scrollbar.set)

            # Contenido del resumen
            content = f"RESUMEN DE FINCAS\n"
            content += f"{'=' * 50}\n\n"
            content += f"Total de fincas: {len(fincas)}\n\n"

            content += f"DISTRIBUCIÓN POR REGIONES:\n"
            content += f"{'-' * 30}\n"
            for region, count in sorted(regiones.items()):
                content += f"{region}: {count} finca(s)\n"

            content += f"\nDISTRIBUCIÓN POR TIPO DE SUELO:\n"
            content += f"{'-' * 30}\n"
            for suelo, count in sorted(suelos.items()):
                content += f"{suelo}: {count} finca(s)\n"

            summary_text.insert('1.0', content)
            summary_text.config(state='disabled')

            summary_text.pack(side="left", fill="both", expand=True, padx=10, pady=10)
            scrollbar.pack(side="right", fill="y", pady=10)

        except Exception as e:
            UIHelpers.show_error_message("Error", f"Error generando resumen: {str(e)}")