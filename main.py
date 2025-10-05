import tkinter as tk
from views.main_window import MainWindow
from config.database import DatabaseConnection
import sys


def main():
    """Función principal de la aplicación"""
    try:
        # Inicializar conexión a base de datos
        db = DatabaseConnection()
        if not db.test_connection():
            print("Error: No se pudo conectar a la base de datos")
            sys.exit(1)

        # Crear ventana principal
        root = tk.Tk()
        app = MainWindow(root, db)

        # Configurar cierre de aplicación
        def on_closing():
            db.disconnect()
            root.destroy()

        root.protocol("WM_DELETE_WINDOW", on_closing)

        # Iniciar aplicación
        root.mainloop()

    except Exception as e:
        print(f"Error al iniciar la aplicación: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()