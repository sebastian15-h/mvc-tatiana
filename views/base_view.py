"""
Clase base para todas las vistas de la aplicación Northwind
"""
import tkinter as tk
from tkinter import ttk
from abc import ABC, abstractmethod
from utils.helpers import UIHelpers
from utils.exceptions import ValidationError, DatabaseOperationError


class BaseView(ABC):
    """Clase abstracta base para todas las vistas"""

    def __init__(self, parent_frame, controller):
        """
        Inicializa la vista base

        Args:
            parent_frame: Frame padre donde se colocará esta vista
            controller: Controlador asociado a esta vista
        """
        self.parent_frame = parent_frame
        self.controller = controller
        self.main_frame = None
        self.form_frame = None
        self.list_frame = None
        self.form_fields = {}
        self.tree = None
        self.entity_name = ""  # Debe ser definido por cada vista hija, esto es para qye se muestre en los mensajes


        self._setup_ui()
        self._bind_events()

    def _setup_ui(self):
        """Configura la interfaz de usuario base"""
        # Frame principal
        self.main_frame = tk.Frame(self.parent_frame)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Frame izquierdo para formulario
        self.left_frame = tk.Frame(self.main_frame)
        self.left_frame.pack(side="left", fill="y", padx=(0, 10))

        # Frame derecho para lista
        self.right_frame = tk.Frame(self.main_frame)
        self.right_frame.pack(side="right", fill="both", expand=True)

        # Crear componentes específicos
        self._create_form_section()
        self._create_list_section()

    def _create_form_section(self):
        """Crea la sección del formulario"""
        # Título
        title_text = getattr(self, 'form_title', f"GESTIÓN DE AGROCONTROL SAS")
        title_label = tk.Label(
            self.left_frame,
            text=title_text,
            font=("Arial", 16, "bold"),
            fg="green"
        )
        title_label.pack(pady=20)

        # Frame para el formulario
        self.form_frame = tk.Frame(self.left_frame)
        self.form_frame.pack(pady=20, anchor="w", padx=20)

        # Crear campos específicos del formulario
        self._create_form_fields()

        # Frame para botones
        self.button_frame = tk.Frame(self.left_frame)
        self.button_frame.pack(pady=20)

        # Crear botones
        self._create_buttons()

    def _create_list_section(self):
        """Crea la sección de la lista"""
        # Título de la lista
        list_title = tk.Label(
            self.right_frame,
            text=f"LISTA DE {self.entity_name.upper()}S",
            font=("Arial", 14, "bold")
        )
        list_title.pack(pady=10)

        # Frame para el TreeView y scrollbar
        tree_frame = tk.Frame(self.right_frame)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Crear TreeView PRIMERO (esto establece self.tree)
        self._create_treeview(tree_frame)

        # SOLO crear scrollbar si self.tree existe
        if hasattr(self, 'tree') and self.tree is not None:
            scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
            self.tree.configure(yscrollcommand=scrollbar.set)
            scrollbar.pack(side="right", fill="y")
        else:
            print(f"Advertencia: {self.entity_name} no creó un TreeView")
    def _create_buttons(self):
        """Crea los botones de acción"""
        buttons_config = [
            ("Guardar", "#4CAF50", self._on_save),
            ("Actualizar", "#2196F3", self._on_update),
            ("Eliminar", "#f44336", self._on_delete),
            ("Buscar", "#FF9800", self._on_search),
            ("Limpiar", "#9E9E9E", self._on_clear)
        ]

        for text, color, command in buttons_config:
            btn = tk.Button(
                self.button_frame,
                text=text,
                font=("Arial", 10),
                bg=color,
                fg="white",
                width=10,
                command=command
            )
            btn.pack(side=tk.LEFT, padx=3)

    @abstractmethod
    def _create_form_fields(self):
        """Crea los campos específicos del formulario - debe ser implementado por cada vista hija"""
        pass

    @abstractmethod
    def _create_treeview(self, parent):
        """Crea el TreeView específico - debe ser implementado por cada vista hija"""
        pass

    @abstractmethod
    def _get_form_data(self):
        """Obtiene los datos del formulario - debe ser implementado por cada vista hija"""
        pass

    @abstractmethod
    def _populate_form(self, data):
        """Puebla el formulario con datos - debe ser implementado por cada vista hija"""
        pass

    def _bind_events(self):
        """Asocia eventos a los componentes"""
        # El TreeView se asocia después de crearse
        pass

    def _on_tree_select(self, event):
        """Maneja la selección en el TreeView"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            values = item['values']
            if values:
                # Convertir valores del TreeView a diccionario
                data = self._tree_values_to_dict(values)
                self._populate_form(data)

    def _tree_values_to_dict(self, values):
        """
        Convierte los valores del TreeView a un diccionario
        Debe ser implementado por cada vista hija
        """
        return {}

    def _on_save(self):
        """Maneja la acción de guardar"""
        try:
            data = self._get_form_data()
            result = self.controller.create(**data)
            if result:
                UIHelpers.show_success_message("Éxito", f"{self.entity_name} guardado correctamente")
                self._clear_form()
                self._refresh_list()
        except ValidationError as e:
            UIHelpers.show_error_message("Error de Validación", str(e))
        except DatabaseOperationError as e:
            UIHelpers.show_error_message("Error de Base de Datos", str(e))
        except Exception as e:
            UIHelpers.show_error_message("Error", f"Error inesperado: {str(e)}")

    def _on_update(self):
        """Maneja la acción de actualizar"""
        try:
            data = self._get_form_data()
            entity_id = self._get_entity_id_from_form()

            if not entity_id:
                UIHelpers.show_error_message("Error", f"Debe ingresar un ID de {self.entity_name} válido")
                return

            result = self.controller.update(entity_id, **data)
            if result:
                UIHelpers.show_success_message("Éxito", f"{self.entity_name} actualizado correctamente")
                self._refresh_list()
        except ValidationError as e:
            UIHelpers.show_error_message("Error de Validación", str(e))
        except DatabaseOperationError as e:
            UIHelpers.show_error_message("Error de Base de Datos", str(e))
        except Exception as e:
            UIHelpers.show_error_message("Error", f"Error inesperado: {str(e)}")

    def _on_delete(self):
        """Maneja la acción de eliminar"""
        try:
            entity_id = self._get_entity_id_from_form()

            if not entity_id:
                UIHelpers.show_error_message("Error", f"Debe ingresar un ID de {self.entity_name} válido")
                return

            if UIHelpers.show_confirmation_dialog("Confirmar",
                                                  f"¿Está seguro de eliminar este {self.entity_name.lower()}?"):
                result = self.controller.delete(entity_id)
                if result:
                    UIHelpers.show_success_message("Éxito", f"{self.entity_name} eliminado correctamente")
                    self._clear_form()
                    self._refresh_list()
        except ValidationError as e:
            UIHelpers.show_error_message("Error de Validación", str(e))
        except DatabaseOperationError as e:
            UIHelpers.show_error_message("Error de Base de Datos", str(e))
        except Exception as e:
            UIHelpers.show_error_message("Error", f"Error inesperado: {str(e)}")

    def _on_search(self):
        """Maneja la acción de buscar"""
        try:
            entity_id = self._get_entity_id_from_form()

            if not entity_id:
                UIHelpers.show_error_message("Error", f"Debe ingresar un ID de {self.entity_name} válido")
                return

            data = self.controller.get_by_id(entity_id)
            if data:
                self._populate_form(data)
            else:
                UIHelpers.show_error_message("No encontrado", f"{self.entity_name} no encontrado")
        except ValidationError as e:
            UIHelpers.show_error_message("Error de Validación", str(e))
        except DatabaseOperationError as e:
            UIHelpers.show_error_message("Error de Base de Datos", str(e))
        except Exception as e:
            UIHelpers.show_error_message("Error", f"Error inesperado: {str(e)}")

    def _on_clear(self):
        """Maneja la acción de limpiar el formulario"""
        self._clear_form()

    def _clear_form(self):
        """Limpia todos los campos del formulario"""
        for field_name, field_widget in self.form_fields.items():
            if isinstance(field_widget, tk.Entry):
                field_widget.delete(0, tk.END)
            elif isinstance(field_widget, tk.Text):
                field_widget.delete('1.0', tk.END)
            elif hasattr(field_widget, 'set'):  # Para variables de Tkinter
                field_widget.set("")

    def _refresh_list(self):
        """Actualiza la lista de entidades"""
        try:
            # Limpiar TreeView
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Cargar datos
            entities = self.controller.get_all()
            for entity in entities:
                values = self._entity_to_tree_values(entity)
                self.tree.insert('', 'end', values=values)
        except Exception as e:
            UIHelpers.show_error_message("Error", f"Error cargando lista: {str(e)}")

    def _entity_to_tree_values(self, entity):
        """
        Convierte una entidad a valores para el TreeView
        Debe ser implementado por cada vista hija
        """
        return ()

    def _get_entity_id_from_form(self):
        """
        Obtiene el ID de la entidad desde el formulario
        Debe ser implementado por cada vista hija
        """
        return None

    def create_form_field(self, row, label_text, field_name, field_type="entry", **kwargs):
        """
        Crea un campo de formulario estándar

        Args:
            row (int): Fila donde colocar el campo
            label_text (str): Texto de la etiqueta
            field_name (str): Nombre del campo para referencia
            field_type (str): Tipo de campo ("entry", "text", "combobox")
            **kwargs: Argumentos adicionales para el widget

        Returns:
            Widget: El widget creado
        """
        # Crear etiqueta
        label = tk.Label(
            self.form_frame,
            text=label_text,
            font=("Arial", 12)
        )
        label.grid(row=row, column=0, sticky="w", padx=(0, 10), pady=8)

        # Crear campo según el tipo
        if field_type == "entry":
            field = tk.Entry(
                self.form_frame,
                width=kwargs.get('width', 25),
                font=("Arial", 12),
                relief="solid",
                bd=1
            )
        elif field_type == "text":
            field = tk.Text(
                self.form_frame,
                width=kwargs.get('width', 25),
                height=kwargs.get('height', 4),
                font=("Arial", 12),
                relief="solid",
                bd=1
            )
        elif field_type == "combobox":
            field = ttk.Combobox(
                self.form_frame,
                width=kwargs.get('width', 22),
                font=("Arial", 12),
                values=kwargs.get('values', [])
            )
        else:
            # Por defecto, crear Entry
            field = tk.Entry(
                self.form_frame,
                width=kwargs.get('width', 25),
                font=("Arial", 12),
                relief="solid",
                bd=1
            )

        # Posicionar campo
        sticky = kwargs.get('sticky', "w")
        field.grid(row=row, column=1, sticky=sticky, pady=8)

        # Guardar referencia del campo
        self.form_fields[field_name] = field

        return field

    def get_field_value(self, field_name):
        """
        Obtiene el valor de un campo del formulario

        Args:
            field_name (str): Nombre del campo

        Returns:
            str: Valor del campo o cadena vacía si no existe
        """
        field = self.form_fields.get(field_name)
        if not field:
            return ""

        if isinstance(field, tk.Entry):
            return field.get()
        elif isinstance(field, tk.Text):
            return field.get('1.0', tk.END).strip()
        elif isinstance(field, ttk.Combobox):
            return field.get()
        elif hasattr(field, 'get'):
            return field.get()

        return ""

    def set_field_value(self, field_name, value):
        """
        Establece el valor de un campo del formulario

        Args:
            field_name (str): Nombre del campo
            value: Valor a establecer
        """
        field = self.form_fields.get(field_name)
        if not field:
            return

        # Limpiar campo primero
        if isinstance(field, tk.Entry):
            field.delete(0, tk.END)
            if value is not None:
                field.insert(0, str(value))
        elif isinstance(field, tk.Text):
            field.delete('1.0', tk.END)
            if value is not None:
                field.insert('1.0', str(value))
        elif isinstance(field, ttk.Combobox):
            if value is not None:
                field.set(str(value))
        elif hasattr(field, 'set'):
            if value is not None:
                field.set(str(value))

    def validate_required_fields(self, required_fields):
        """
        Valida que los campos requeridos no estén vacíos

        Args:
            required_fields (list): Lista de nombres de campos requeridos

        Returns:
            bool: True si todos los campos requeridos tienen valor

        Raises:
            ValidationError: Si algún campo requerido está vacío
        """
        for field_name in required_fields:
            value = self.get_field_value(field_name)
            if not value or not value.strip():
                # Obtener nombre legible del campo
                readable_name = field_name.replace('_', ' ').title()
                raise ValidationError(readable_name, "es requerido")

        return True

    def focus_field(self, field_name):
        """
        Enfoca un campo específico

        Args:
            field_name (str): Nombre del campo a enfocar
        """
        field = self.form_fields.get(field_name)
        if field:
            field.focus_set()

    def disable_field(self, field_name):
        """
        Deshabilita un campo

        Args:
            field_name (str): Nombre del campo a deshabilitar
        """
        field = self.form_fields.get(field_name)
        if field:
            field.config(state='disabled')

    def enable_field(self, field_name):
        """
        Habilita un campo

        Args:
            field_name (str): Nombre del campo a habilitar
        """
        field = self.form_fields.get(field_name)
        if field:
            field.config(state='normal')

    def show_loading(self, message="Cargando..."):
        """
        Muestra un indicador de carga (placeholder para implementación futura)

        Args:
            message (str): Mensaje de carga
        """
        # TODO: Implementar indicador de carga visual
        pass

    def hide_loading(self):
        """
        Oculta el indicador de carga (placeholder para implementación futura)
        """
        # TODO: Implementar ocultación del indicador de carga
        pass

    def setup_search_functionality(self, search_field_name, search_callback=None):
        """
        Configura funcionalidad de búsqueda en tiempo real

        Args:
            search_field_name (str): Nombre del campo de búsqueda
            search_callback (function): Función callback para búsqueda personalizada
        """
        field = self.form_fields.get(search_field_name)
        if field and isinstance(field, tk.Entry):
            # Vincular evento de tecla para búsqueda en tiempo real
            field.bind('<KeyRelease>', lambda e: self._on_search_changed(search_callback))

    def _on_search_changed(self, callback=None):
        """
        Maneja cambios en el campo de búsqueda

        Args:
            callback (function): Función callback personalizada
        """
        if callback:
            callback()
        else:
            # Implementación por defecto: filtrar lista
            search_term = self.get_field_value('search')
            if hasattr(self.controller, 'search'):
                try:
                    results = self.controller.search(search_term)
                    self._update_tree_with_results(results)
                except Exception as e:
                    print(f"Error en búsqueda: {e}")

    def _update_tree_with_results(self, results):
        """
        Actualiza el TreeView con resultados de búsqueda

        Args:
            results (list): Lista de resultados
        """
        # Limpiar TreeView
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Agregar resultados
        for result in results:
            values = self._entity_to_tree_values(result)
            self.tree.insert('', 'end', values=values)