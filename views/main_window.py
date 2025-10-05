"""
Ventana principal de la aplicación Northwind
"""
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from views.cultivos_view import CultivosView
from views.fincas_view import FincasView
from views.parcelas_view import ParcelasView
from controllers.cultivos_controller import CultivosController
from controllers.fincas_controller import FincasController
from controllers.parcelas_controller import ParcelasController
from models.cultivos import Cultivos
from models.fincas import Fincas
from models.parcelas import Parcelas
from utils.helpers import UIHelpers, ThemeManager  # ✅ Añadir ThemeManager
import os
import sys


class MainWindow:
    """Ventana principal con pestañas para cada entidad"""

    def __init__(self, root, db_connection):
        """
        Inicializa la ventana principal

        Args:
            root: Ventana raíz de Tkinter
            db_connection: Conexión a la base de datos
        """
        self.root = root
        self.db = db_connection
        self.views = {}  # ✅ Diccionario para almacenar las vistas

        # Configurar ventana principal
        self._setup_main_window()

        # Crear modelos
        self._create_models()

        # Crear controladores
        self._create_controllers()

        # Crear interfaz
        self._create_interface()

        # Cargar datos iniciales
        self._load_initial_data()

    def _setup_main_window(self):
        """Configura la ventana principal"""
        # Configuración básica de la ventana
        self.root.title("Sistema AGROCONTROL - Gestión de Datos")
        self.root.geometry('1400x800')
        self.root.state('zoomed')

        # Centrar ventana
        UIHelpers.center_window(self.root, 1400, 800)

        # CONFIGURAR FAVICON - Método robusto
        self._setup_favicon()

        # Configurar protocolo de cierre
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)

        # Configurar estilo
        self._setup_styles()

    def _setup_favicon(self):
        """Configura el favicon de la aplicación de forma robusta"""
        print("🔄 Intentando cargar favicon...")

        # Obtener el directorio actual del script
        current_dir = os.path.dirname(os.path.abspath(__file__))
        print(f"📁 Directorio actual: {current_dir}")

        # Lista de posibles ubicaciones del favicon
        favicon_paths = [
            os.path.join(current_dir, "favicon.ico"),
            os.path.join(current_dir, "../favicon.ico"),
            os.path.join(current_dir, "../../favicon.ico"),
            os.path.join(os.getcwd(), "favicon.ico"),
            "favicon.ico",
            "./favicon.ico",
            "../favicon.ico"
        ]

        # Verificar qué archivos existen
        print("🔍 Buscando favicon en las siguientes rutas:")
        for path in favicon_paths:
            exists = os.path.exists(path)
            print(f"   {path} - {'✅ EXISTE' if exists else '❌ NO EXISTE'}")

        # Intentar cargar el favicon
        favicon_loaded = False
        for path in favicon_paths:
            try:
                if os.path.exists(path):
                    self.root.iconbitmap(path)
                    print(f"✅ Favicon cargado exitosamente: {path}")
                    favicon_loaded = True
                    break
            except Exception as e:
                print(f"❌ Error cargando {path}: {str(e)}")
                continue

        if not favicon_loaded:
            print("⚠️ No se pudo cargar ningún favicon. La aplicación funcionará sin él.")

            # Intentar método alternativo con PhotoImage para PNG
            png_paths = [
                os.path.join(current_dir, "favicon.png"),
                os.path.join(current_dir, "../favicon.png"),
                os.path.join(os.getcwd(), "favicon.png"),
                "favicon.png"
            ]

            for path in png_paths:
                try:
                    if os.path.exists(path):
                        icon = tk.PhotoImage(file=path)
                        self.root.iconphoto(True, icon)
                        print(f"✅ Favicon PNG cargado: {path}")
                        favicon_loaded = True
                        break
                except Exception as e:
                    print(f"❌ Error cargando PNG {path}: {str(e)}")
                    continue

    def _setup_styles(self):
        """Configura estilos personalizados para la aplicación"""
        style = ttk.Style()

        # Configurar tema inicial
        try:
            style.theme_use('clam')
        except:
            pass

        # Personalizar estilos del Notebook
        style.configure('TNotebook', background='#f0f0f0')
        style.configure('TNotebook.Tab', padding=[20, 10])

        # Personalizar Treeview
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
        style.configure("Treeview", font=("Arial", 9))

    def _create_models(self):
        """Crea las instancias de los modelos"""
        self.cultivos_model = Cultivos(self.db)
        self.fincas_model = Fincas(self.db)
        self.parcelas_model = Parcelas(self.db)

    def _create_controllers(self):
        """Crea las instancias de los controladores"""
        self.cultivos_controller = CultivosController(self.cultivos_model)
        self.fincas_controller = FincasController(self.fincas_model)
        self.parcelas_controller = ParcelasController(self.parcelas_model)

    def _create_interface(self):
        """Crea la interfaz de usuario principal"""
        # Frame principal
        self.main_frame = tk.Frame(self.root, bg='#f0f0f0')
        self.main_frame.pack(fill="both", expand=True)

        # Título de la aplicación
        self.title_frame = tk.Frame(self.main_frame, bg='#2c3e50', height=60)
        self.title_frame.pack(fill="x", padx=0, pady=0)
        self.title_frame.pack_propagate(False)

        self.title_label = tk.Label(
            self.title_frame,
            text="Sistema de Gestión agrocontrol sas",
            font=("Arial", 18, "bold"),
            fg="white",
            bg='#2c3e50'
        )
        self.title_label.pack(expand=True)

        # Subtítulo con información de conexión
        self.subtitle_frame = tk.Frame(self.main_frame, bg='#34495e', height=30)
        self.subtitle_frame.pack(fill="x", padx=0, pady=0)
        self.subtitle_frame.pack_propagate(False)

        connection_status = "Conectado" if self.db.is_connected() else "Desconectado"
        self.subtitle_label = tk.Label(
            self.subtitle_frame,
            text=f"Base de Datos: {connection_status} | Usuario: root | DB: agrocontrol_sas_db",
            font=("Arial", 10),
            fg="white",
            bg='#34495e'
        )
        self.subtitle_label.pack(expand=True)

        # Crear el widget Notebook (pestañas)
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)

        # Crear pestañas
        self._create_tabs()

        # Barra de estado
        self._create_status_bar(self.main_frame)

    def _create_tabs(self):
        """Crea las pestañas y sus contenidos"""
        # Pestaña de Cultivos
        self.cultivos_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.cultivos_frame, text="🌿 Cultivos")
        self.cultivos_view = CultivosView(self.cultivos_frame, self.cultivos_controller)
        self.views['cultivos'] = self.cultivos_view  # ✅ Guardar referencia

        # Pestaña de Fincas
        self.fincas_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.fincas_frame, text="🏡 Fincas")
        self.fincas_view = FincasView(self.fincas_frame, self.fincas_controller)
        self.views['fincas'] = self.fincas_view  # ✅ Guardar referencia

        # Pestaña de Parcelas
        self.parcelas_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.parcelas_frame, text="🌾 Parcelas")
        self.parcelas_view = ParcelasView(self.parcelas_frame, self.parcelas_controller)
        self.views['parcelas'] = self.parcelas_view  # ✅ Guardar referencia

        # Configurar evento de cambio de pestaña
        self.notebook.bind("<<NotebookTabChanged>>", self._on_tab_changed)

    def _create_status_bar(self, parent):
        """Crea la barra de estado"""
        self.status_frame = tk.Frame(parent, bg='#34495e', height=25)
        self.status_frame.pack(fill="x", side="bottom", padx=0, pady=0)
        self.status_frame.pack_propagate(False)

        self.status_label = tk.Label(
            self.status_frame,
            text="Sistema listo | Northwind Database Management System",
            font=("Arial", 9),
            fg="white",
            bg='#34495e'
        )
        self.status_label.pack(side="left", padx=10)

        # Información de versión
        self.version_label = tk.Label(
            self.status_frame,
            text="v1.0.0",
            font=("Arial", 9),
            fg="white",
            bg='#34495e'
        )
        self.version_label.pack(side="right", padx=10)

    def _on_tab_changed(self, event):
        """Maneja el cambio de pestaña"""
        try:
            selected_tab = self.notebook.select()
            if selected_tab:
                tab_index = self.notebook.index(selected_tab)
                tab_text = self.notebook.tab(tab_index, "text")

                print(f"Cambiando a pestaña: {tab_text}")

                # Actualizar datos cuando se cambia de pestaña
                if hasattr(self, 'cultivos_view') and tab_text == "🌿 Cultivos":
                    self.cultivos_view._refresh_list()
                elif hasattr(self, 'fincas_view') and tab_text == "🏡 Fincas":
                    self.fincas_view._refresh_list()
                elif hasattr(self, 'parcelas_view') and tab_text == "🌾 Parcelas":
                    self.parcelas_view._refresh_list()

        except Exception as e:
            print(f"Error al cambiar pestaña: {e}")

    def _load_initial_data(self):
        """Carga datos iniciales en las vistas"""
        try:
            print("🔄 Cargando datos iniciales...")

            # Actualizar todas las listas inicialmente
            if hasattr(self, 'cultivos_view'):
                print("🌿 Cargando cultivos...")
                self.cultivos_view._refresh_list()

            if hasattr(self, 'fincas_view'):
                print("🏡 Cargando fincas...")
                self.fincas_view._refresh_list()

            if hasattr(self, 'parcelas_view'):
                print("🌾 Cargando parcelas...")
                self.parcelas_view._refresh_list()

            print("✅ Datos iniciales cargados correctamente")

        except Exception as e:
            print(f"❌ Error cargando datos iniciales: {e}")
            import traceback
            traceback.print_exc()

    def change_theme(self):
        """Cambia el tema de la aplicación"""
        try:
            # Cambiar tema
            ThemeManager.toggle_theme()

            # Aplicar nuevo tema a toda la ventana
            ThemeManager.apply_theme_to_window(self.root, self.views)

            # Mostrar mensaje
            current_theme = "oscuro" if ThemeManager.current_theme == "dark" else "claro"
            UIHelpers.show_success_message("Tema Cambiado", f"Tema cambiado a modo {current_theme}")

        except Exception as e:
            UIHelpers.show_error_message("Error", f"Error cambiando tema: {str(e)}")

    def update_status(self, message):
        """Actualiza el mensaje en la barra de estado"""
        if hasattr(self, 'status_label'):
            self.status_label.config(text=message)

    def show_loading(self, show=True):
        """Muestra u oculta indicador de carga (placeholder)"""
        pass

    def _on_closing(self):
        if messagebox.askokcancel("Salir", "¿Quieres salir de la aplicación?"):
            self.root.destroy()