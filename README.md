🏨 Sistema de Gestión Hotelera
📋 Descripción del Proyecto
Sistema de gestión hotelera desarrollado en Python para la administración integral de hoteles, clientes y parcelas. La aplicación sigue una arquitectura MVC (Modelo-Vista-Controlador) y está diseñada para ser modular y escalable.

🏗️ Estructura del Proyecto
text
proyecto/
├── acciones/                    # Módulo principal de la aplicación
│   ├── controladores/          # Lógica de controladores
│   │   ├── base_controller.py
│   │   ├── clientes_controller.py
│   │   ├── hoteles_controller.py
│   │   └── parcelas_controller.py
│   ├── modelos/                # Modelos de datos
│   │   ├── base_model.py
│   │   ├── clientes.py
│   │   ├── hoteles.py
│   │   └── parcelas.py
│   ├── utilidades/             # Utilidades del sistema
│   │   ├── exceptions.py
│   │   ├── helpers.py
│   │   └── validators.py
│   └── database.py             # Configuración de base de datos
├── vistas/                     # Interfaz de usuario
│   └── principal.py            # Vista principal
├── imágenes/                   # Recursos visuales
├── empleados/                  # Gestión de empleados
├── temp/                       # Archivos temporales
├── configuración/              # Configuraciones del sistema
└── Documentación.docx          # Documentación técnica
🎯 Funcionalidades Principales
🔧 Módulos del Sistema
🏨 Gestión de Hoteles - Administración de propiedades hoteleras

👥 Gestión de Clientes - Registro y seguimiento de clientes

📊 Gestión de Parcelas - Control de áreas y espacios

👨‍💼 Gestión de Empleados - Administración del personal

⚙️ Utilidades - Herramientas y validaciones del sistema

🚀 Instalación y Configuración
bash
# Navegar al directorio del proyecto
cd proyecto

# Ejecutar la aplicación
python vistas/principal.py
🛠️ Tecnologías y Arquitectura
Patrón de Diseño
MVC (Modelo-Vista-Controlador) - Separación clara de responsabilidades

Modular - Componentes independientes y reutilizables

Escalable - Fácil adición de nuevos módulos

Características Técnicas
Controladores base para herencia

Modelos de datos estructurados

Sistema de excepciones personalizado

Validadores de datos

Helpers utilitarios

📁 Estructura Detallada
Controladores (acciones/controladores/)
base_controller.py - Controlador base con funcionalidades comunes

clientes_controller.py - Lógica de negocio para clientes

hoteles_controller.py - Gestión de operaciones hoteleras

parcelas_controller.py - Administración de parcelas

Modelos (acciones/modelos/)
base_model.py - Modelo base con métodos CRUD

clientes.py - Entidad Cliente con atributos y métodos

hoteles.py - Entidad Hotel con propiedades y servicios

parcelas.py - Entidad Parcela con características específicas

Utilidades (acciones/utilidades/)
exceptions.py - Excepciones personalizadas del sistema

helpers.py - Funciones auxiliares y helpers

validators.py - Validadores de datos y reglas de negocio

🔧 Configuración
El sistema utiliza archivos de configuración en la carpeta configuración/ para personalizar:

Parámetros de conexión a base de datos

Configuraciones de hotel

Preferencias del sistema

Parámetros de negocio

📊 Base de Datos
La configuración de la base de datos se maneja en acciones/database.py incluyendo:

Conexión a base de datos

Configuración de esquemas

Migraciones (si aplica)

🎨 Interfaz de Usuario
La interfaz principal se encuentra en vistas/principal.py y probablemente incluye:

Menú principal

Formularios de gestión

Paneles de control

Reportes y estadísticas

📝 Documentación
La documentación completa del sistema está disponible en Documentación.docx incluyendo:

Manual de usuario

Guía técnica

Diagramas de arquitectura

Flujos de trabajo

Desarrollado con Python 🐍 | Arquitectura MVC 🏗️ | Sistema de Gestión Hotelera 🏨
