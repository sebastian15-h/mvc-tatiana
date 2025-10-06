-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 22-09-2025 a las 16:33:55
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `hoteel`
--

DELIMITER $$
--
-- Procedimientos
--
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_actualizar_cliente` (IN `p_id_cliente` INT, IN `p_nombre` VARCHAR(100), IN `p_apellido` VARCHAR(100), IN `p_documento_identidad` INT, IN `p_nacionalidad` VARCHAR(50), IN `p_fecha_nacimiento` DATE, IN `p_direccion` VARCHAR(100), IN `p_telefono` INT, IN `p_correo` VARCHAR(100), IN `p_preferencias_especiales` VARCHAR(100), IN `p_nivel_programa_fidelizacion` VARCHAR(100))   BEGIN
    UPDATE clientes
    SET 
        nombre = p_nombre,
        apellido = p_apellido,
        documento_identidad = p_documento_identidad,
        nacionalidad = p_nacionalidad,
        fecha_nacimiento = p_fecha_nacimiento,
        direccion = p_direccion,
        telefono = p_telefono,
        correo = p_correo,
        preferencias_especiales = p_preferencias_especiales,
        nivel_programa_fidelizacion = p_nivel_programa_fidelizacion
    WHERE id_cliente = p_id_cliente;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_buscarEmpleado` (IN `p_id_empleado` INT)   BEGIN
    SELECT id_empleado, nombres, apellidos, cargo, telefono, correo, id_hotel
    FROM empleados
    WHERE id_empleado = p_id_empleado;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_buscar_cliente` (IN `p_id_cliente` INT)   BEGIN
    SELECT * FROM clientes WHERE id_cliente = p_id_cliente;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_buscar_temporada` (IN `p_id_temporada` INT)   BEGIN
    SELECT id_temporada, nombre_temporada, fecha_inicio, fecha_fin, factor_multiplicador_tarifa
    FROM temporadas
    WHERE id_temporada = p_id_temporada;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_deleteEmpleadoById` (IN `p_id_empleado` INT)   BEGIN
    DELETE FROM empleados WHERE id_empleado = p_id_empleado;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_deleteHotelById` (IN `p_id_hotel` INT)   BEGIN
    DELETE FROM hoteles WHERE id_hotel = p_id_hotel;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_deleteTemporada` (IN `p_id_temporada` INT)   BEGIN
    DELETE FROM temporadas WHERE id_temporada = p_id_temporada;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_eliminar_cliente` (IN `p_id_cliente` INT)   BEGIN
    DELETE FROM clientes WHERE id_cliente = p_id_cliente;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_getHotelById` (IN `p_id_hotel` INT)   BEGIN
    SELECT 
        id_hotel,
        nombre_hotel,
        categoria,
        direccion,
        telefono,
        correo,
        año_inauguracion,
        numero_total_habitantes,
        servicios_disponibles,
        horarios_check_in,
        horarios_check_out,
        gerente_responsable
    FROM hoteles
    WHERE id_hotel = p_id_hotel;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_guardarEmpleado` (IN `p_id_empleado` INT, IN `p_nombres` VARCHAR(100), IN `p_apellidos` VARCHAR(100), IN `p_cargo` VARCHAR(100), IN `p_telefono` VARCHAR(50), IN `p_correo` VARCHAR(100), IN `p_id_hotel` INT)   BEGIN
    INSERT INTO empleados (id_empleado, nombres, apellidos, cargo, telefono, correo, id_hotel)
    VALUES (p_id_empleado, p_nombres, p_apellidos, p_cargo, p_telefono, p_correo, p_id_hotel);
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_insertar_cliente` (IN `p_nombre` VARCHAR(100), IN `p_apellido` VARCHAR(100), IN `p_documento_identidad` INT, IN `p_nacionalidad` VARCHAR(50), IN `p_fecha_nacimiento` DATE, IN `p_direccion` VARCHAR(100), IN `p_telefono` INT, IN `p_correo` VARCHAR(100), IN `p_preferencias_especiales` VARCHAR(100), IN `p_nivel_programa_fidelizacion` VARCHAR(100))   BEGIN
    INSERT INTO clientes (
        nombre,
        apellido,
        documento_identidad,
        nacionalidad,
        fecha_nacimiento,
        direccion,
        telefono,
        correo,
        preferencias_especiales,
        nivel_programa_fidelizacion
    ) VALUES (
        p_nombre,
        p_apellido,
        p_documento_identidad,
        p_nacionalidad,
        p_fecha_nacimiento,
        p_direccion,
        p_telefono,
        p_correo,
        p_preferencias_especiales,
        p_nivel_programa_fidelizacion
    );
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_insertHotel` (IN `p_id_hotel` INT, IN `p_nombre_hotel` VARCHAR(50), IN `p_categoria` INT, IN `p_direccion` VARCHAR(100), IN `p_telefono` INT, IN `p_correo` VARCHAR(100), IN `p_año_inauguracion` DECIMAL(10,0), IN `p_numero_total_habitantes` INT, IN `p_servicios_disponibles` VARCHAR(1000), IN `p_horarios_check_in` TIME, IN `p_horarios_check_out` TIME, IN `p_gerente_responsable` VARCHAR(50))   BEGIN
    INSERT INTO hoteles (
        id_hotel, nombre_hotel, categoria, direccion, telefono, correo,
        año_inauguracion, numero_total_habitantes, servicios_disponibles,
        horarios_check_in, horarios_check_out, gerente_responsable
    ) VALUES (
        p_id_hotel, p_nombre_hotel, p_categoria, p_direccion, p_telefono, p_correo,
        p_año_inauguracion, p_numero_total_habitantes, p_servicios_disponibles,
        p_horarios_check_in, p_horarios_check_out, p_gerente_responsable
    );
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_insertTemporada` (IN `p_nombre_temporada` VARCHAR(255), IN `p_fecha_inicio` DATE, IN `p_fecha_fin` DATE, IN `p_factor_multiplicador_tarifa` DECIMAL(10,2))   BEGIN
    INSERT INTO temporadas(nombre_temporada, fecha_inicio, fecha_fin, factor_multiplicador_tarifa)
    VALUES (p_nombre_temporada, p_fecha_inicio, p_fecha_fin, p_factor_multiplicador_tarifa);
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_updateEmpleado` (IN `p_id_empleado` INT, IN `p_nombres` VARCHAR(100), IN `p_apellidos` VARCHAR(100), IN `p_cargo` VARCHAR(100), IN `p_telefono` VARCHAR(50), IN `p_correo` VARCHAR(100), IN `p_id_hotel` INT)   BEGIN
    UPDATE empleados
    SET
        nombres = p_nombres,
        apellidos = p_apellidos,
        cargo = p_cargo,
        telefono = p_telefono,
        correo = p_correo,
        id_hotel = p_id_hotel
    WHERE id_empleado = p_id_empleado;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_updateHotel` (IN `p_id_hotel` INT, IN `p_nombre_hotel` VARCHAR(50), IN `p_categoria` INT, IN `p_direccion` VARCHAR(100), IN `p_telefono` INT, IN `p_correo` VARCHAR(100), IN `p_año_inauguracion` DECIMAL(10,0), IN `p_numero_total_habitantes` INT, IN `p_servicios_disponibles` VARCHAR(1000), IN `p_horarios_check_in` TIME, IN `p_horarios_check_out` TIME, IN `p_gerente_responsable` VARCHAR(50))   BEGIN
    UPDATE hoteles
    SET
        nombre_hotel = p_nombre_hotel,
        categoria = p_categoria,
        direccion = p_direccion,
        telefono = p_telefono,
        correo = p_correo,
        año_inauguracion = p_año_inauguracion,
        numero_total_habitantes = p_numero_total_habitantes,
        servicios_disponibles = p_servicios_disponibles,
        horarios_check_in = p_horarios_check_in,
        horarios_check_out = p_horarios_check_out,
        gerente_responsable = p_gerente_responsable
    WHERE id_hotel = p_id_hotel;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_updateTemporada` (IN `p_id_temporada` INT, IN `p_nombre_temporada` VARCHAR(255), IN `p_fecha_inicio` DATE, IN `p_fecha_fin` DATE, IN `p_factor_multiplicador_tarifa` DECIMAL(10,2))   BEGIN
    UPDATE temporadas
    SET nombre_temporada = p_nombre_temporada,
        fecha_inicio = p_fecha_inicio,
        fecha_fin = p_fecha_fin,
        factor_multiplicador_tarifa = p_factor_multiplicador_tarifa
    WHERE id_temporada = p_id_temporada;
END$$

DELIMITER ;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `check_in_out`
--

CREATE TABLE `check_in_out` (
  `id_check` int(11) NOT NULL,
  `id_reserva` int(11) DEFAULT NULL,
  `id_habitacion` int(11) DEFAULT NULL,
  `fecha_llegada` date DEFAULT NULL,
  `hora_llegada` varchar(20) DEFAULT NULL,
  `fecha_salida` date DEFAULT NULL,
  `hora_salida` varchar(20) DEFAULT NULL,
  `id_empleado` int(11) DEFAULT NULL,
  `forma_pago` varchar(20) DEFAULT NULL,
  `deposito_garantia` varchar(50) DEFAULT NULL,
  `observaciones` varchar(200) DEFAULT NULL,
  `id_cliente` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `check_in_out`
--

INSERT INTO `check_in_out` (`id_check`, `id_reserva`, `id_habitacion`, `fecha_llegada`, `hora_llegada`, `fecha_salida`, `hora_salida`, `id_empleado`, `forma_pago`, `deposito_garantia`, `observaciones`, `id_cliente`) VALUES
(1, 1, 1, '2024-04-20', '10:00am', '2024-04-22', '6:00pm', 1, 'tarjeta', 'fijo', 'el cliente prefiere una habitacon con vista a la ciudad', 1),
(2, 2, 2, '2024-12-10', '7:00am', '2024-12-15', '3:00pm', 2, 'efectivo', 'variable', 'el cliente prefiere una habitacion con vista a la montaña', 2),
(3, 3, 3, '2024-06-13', '11:00am', '2024-06-15', '1:00pm', 3, 'tarjeta', 'fijo', 'el cliente prefiere una habitacion con vista al mar', 3),
(4, 4, 4, '2024-04-30', '9:00am', '2024-05-06', '4:00pm', 4, 'tarjeta', 'prolongada', 'el cliente prefiere una habitacion con vista a la montaña', 4);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `clientes`
--

CREATE TABLE `clientes` (
  `id_cliente` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `apellido` varchar(100) NOT NULL,
  `documento_identidad` int(11) NOT NULL,
  `nacionalidad` varchar(50) DEFAULT NULL,
  `fecha_nacimiento` date DEFAULT NULL,
  `direccion` varchar(100) DEFAULT NULL,
  `telefono` int(11) DEFAULT NULL,
  `correo` varchar(100) DEFAULT NULL,
  `preferencias_especiales` varchar(100) DEFAULT NULL,
  `nivel_programa_fidelizacion` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `clientes`
--

INSERT INTO `clientes` (`id_cliente`, `nombre`, `apellido`, `documento_identidad`, `nacionalidad`, `fecha_nacimiento`, `direccion`, `telefono`, `correo`, `preferencias_especiales`, `nivel_programa_fidelizacion`) VALUES
(1, 'fernando', 'lopez', 1983739, 'colombiano', '1987-12-11', 'calle 13 av 23 #26-19', 3109764, 'fernando_lopez12@gmail.com', 'tipo de cama', 'oro'),
(2, 'adriana', 'figueroa', 1109273, 'española', '1989-06-28', 'calle 18 av 12 #33-16', 31297355, 'adriana_figueroa3@gmail.com', 'vista', 'elite'),
(3, 'carola', 'ramirez', 1387252, 'argentino', '1998-05-22', 'calle 16 av 10 #26-32', 32298736, 'cristian_ramirez09@gmail.com', 'ubicacion de la habitacion', 'ihg rewards club'),
(0, 'tatiana', 'ramirez', 1387252, 'mexicana', '1998-05-22', 'calle 16 av 10 #26-32', 32298736, 'cristian_ramirez09@gmail.com', 'ubicacion de la habitacion', 'ihg rewards club'),
(0, 'james', 'mosquera', 1387252, 'mexicana', '1998-05-22', 'calle 16 av 10 #26-32', 32298736, 'cristian_ramirez09@gmail.com', 'ubicacion de la habitacion', 'ihg rewards club');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `consumo_servicos`
--

CREATE TABLE `consumo_servicos` (
  `id_consumo_servicios` int(11) NOT NULL,
  `id_cliente` int(11) DEFAULT NULL,
  `id_habitacion` int(11) DEFAULT NULL,
  `id_servicio` int(10) DEFAULT NULL,
  `fecha` date DEFAULT NULL,
  `hora` varchar(20) DEFAULT NULL,
  `cantidad` int(11) DEFAULT NULL,
  `precio_aplicado` decimal(10,0) DEFAULT NULL,
  `id_empleado` int(11) DEFAULT NULL,
  `observaciones` varchar(200) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `consumo_servicos`
--

INSERT INTO `consumo_servicos` (`id_consumo_servicios`, `id_cliente`, `id_habitacion`, `id_servicio`, `fecha`, `hora`, `cantidad`, `precio_aplicado`, `id_empleado`, `observaciones`) VALUES
(1, 1, 1, 1, '2024-04-21', '3:00pm', 1, 50, 1, 'spa relajante'),
(2, 2, 2, 2, '2024-12-12', '10:00am', 1, 30, 2, 'masaje relajante'),
(3, 3, 3, 3, '2024-06-14', '8:00pm', 1, 100, 3, 'baño turco relajante'),
(4, 4, 4, 4, '2024-04-04', '2:00pm', 1, 40, 4, 'tratamiento facial relajante');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `empleados`
--

CREATE TABLE `empleados` (
  `id_empleado` int(10) NOT NULL,
  `nombres` varchar(100) NOT NULL,
  `apellidos` varchar(100) NOT NULL,
  `cargo` varchar(50) DEFAULT NULL,
  `telefono` int(10) DEFAULT NULL,
  `correo` varchar(100) DEFAULT NULL,
  `id_hotel` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `empleados`
--

INSERT INTO `empleados` (`id_empleado`, `nombres`, `apellidos`, `cargo`, `telefono`, `correo`, `id_hotel`) VALUES
(1, 'andres', 'roman', 'gerente general', 31362825, 'andres_ospina11@gmail.com', 1),
(2, 'juan', 'calderon', 'subgerente', 31293736, 'juan_calderon67@gmail.com', 2),
(3, 'fabian', 'cortez', 'recepcionista', 3225245, 'fabian_cortez19@gmail.com', 3),
(5, 'facundo', 'batista', 'subgerente', 343434, 'batista@gmail.com', 2);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `eventos`
--

CREATE TABLE `eventos` (
  `id_eventos` int(11) NOT NULL,
  `id_cliente` int(11) DEFAULT NULL,
  `tipo_evento` varchar(50) DEFAULT NULL,
  `cliente_organizador` varchar(100) DEFAULT NULL,
  `fecha_inicio` date DEFAULT NULL,
  `hora_inicio` varchar(20) DEFAULT NULL,
  `duracion_horas` int(11) DEFAULT NULL,
  `numero_asistentes` int(11) DEFAULT NULL,
  `servicios_catering_solicitados` int(11) DEFAULT NULL,
  `equipamento_tecnico_requerido` int(11) DEFAULT NULL,
  `montaje_solicitado` varchar(50) DEFAULT NULL,
  `precio_total` decimal(10,0) DEFAULT NULL,
  `estado` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `eventos`
--

INSERT INTO `eventos` (`id_eventos`, `id_cliente`, `tipo_evento`, `cliente_organizador`, `fecha_inicio`, `hora_inicio`, `duracion_horas`, `numero_asistentes`, `servicios_catering_solicitados`, `equipamento_tecnico_requerido`, `montaje_solicitado`, `precio_total`, `estado`) VALUES
(1, 1, 'luna de miel', 'fernando lopez', '2024-04-21', '5:00pm', 3, 2, 5, 3, 'mesa grande y sillas alrededor', 250, 'en progreso'),
(2, 2, 'cumpleaños', 'adriana figueroa', '2024-12-12', '3:00pm', 2, 4, 7, 5, 'mesa unica', 200, 'en preparacion'),
(3, 3, 'aniversario', 'cristian ramirez', '2024-06-14', '3:00pm', 3, 2, 3, 2, 'mesa redonda y dos sillas', 150, 'programado'),
(4, 4, 'reunion familiar', 'andrea peralta', '2024-04-05', '3:00pm', 4, 8, 10, 8, 'mesa grande y sillas alrededor', 300, 'en progreso');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `habitaciones`
--

CREATE TABLE `habitaciones` (
  `id_habitacion` int(11) NOT NULL,
  `id_hotel` int(11) DEFAULT NULL,
  `numero` int(11) DEFAULT NULL,
  `piso` int(11) DEFAULT NULL,
  `id_tipo_habitacion` int(11) DEFAULT NULL,
  `orientacion` varchar(100) DEFAULT NULL,
  `estado_actual` varchar(20) DEFAULT NULL,
  `caracteristicas_especiales` varchar(200) DEFAULT NULL,
  `tarifa_base` decimal(10,0) DEFAULT NULL,
  `id_salon` int(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `habitaciones`
--

INSERT INTO `habitaciones` (`id_habitacion`, `id_hotel`, `numero`, `piso`, `id_tipo_habitacion`, `orientacion`, `estado_actual`, `caracteristicas_especiales`, `tarifa_base`, `id_salon`) VALUES
(1, 1, 200, 8, 1, 'vista a la ciudad', 'disponible', 'suite', 200, 1),
(2, 2, 201, 3, 2, 'vista a la montaña', 'ocupada', 'doble', 150, 2),
(3, 3, 202, 5, 3, 'vista al mar', 'en mantenimiento', 'individual', 100, 3),
(4, 4, 203, 2, 4, 'vista a la montaña', 'disponible', 'familiar', 200, 4);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `habitacion_servicio`
--

CREATE TABLE `habitacion_servicio` (
  `id_habitacion_servicio` int(11) NOT NULL,
  `id_habitacion` int(11) DEFAULT NULL,
  `id_servicio` int(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `hoteles`
--

CREATE TABLE `hoteles` (
  `id_hotel` int(11) NOT NULL,
  `nombre_hotel` varchar(50) NOT NULL,
  `categoria` int(11) DEFAULT NULL,
  `direccion` varchar(100) NOT NULL,
  `telefono` int(11) DEFAULT NULL,
  `correo` varchar(100) DEFAULT NULL,
  `año_inauguracion` decimal(10,0) DEFAULT NULL,
  `numero_total_habitantes` int(11) DEFAULT NULL,
  `servicios_disponibles` varchar(1000) DEFAULT NULL,
  `horarios_check_in` time DEFAULT NULL,
  `horarios_check_out` time DEFAULT NULL,
  `gerente_responsable` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `hoteles`
--

INSERT INTO `hoteles` (`id_hotel`, `nombre_hotel`, `categoria`, `direccion`, `telefono`, `correo`, `año_inauguracion`, `numero_total_habitantes`, `servicios_disponibles`, `horarios_check_in`, `horarios_check_out`, `gerente_responsable`) VALUES
(1, 'brisa marina', 5, 'calle 27 av 38 #44-33', 57537265, 'brisa_marina.14@gmail.com', 1990, 900, 'var, restaurante, psina, cancha', '14:00:00', '11:00:00', 'carlos londoño'),
(3, 'encanto total', 4, 'calle 44 av 63 #58-10', 76352, 'encanto_colonial.23@gmail.com', 2007, 700, 'restaurante, var, psina', '14:00:00', '11:00:00', 'andres camacho'),
(1, 'campo libre', 3, 'calle 27 av 38 #44-33', 57537265, 'brisa_marina.14@gmail.com', 1990, 900, 'var, restaurante, psina, cancha', '14:00:00', '11:00:00', 'carlos londoño');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `reservas`
--

CREATE TABLE `reservas` (
  `id_reserva` int(10) NOT NULL,
  `fecha_creacion` date DEFAULT NULL,
  `id_cliente` int(10) DEFAULT NULL,
  `fecha_llegada` date NOT NULL,
  `fecha_salida` date NOT NULL,
  `numero_noches` int(11) DEFAULT NULL,
  `numero_habitaciones` int(11) DEFAULT NULL,
  `id_tipo_habitacion` int(11) DEFAULT NULL,
  `numero_huespedes_adultos` int(11) DEFAULT NULL,
  `numero_huespedes_niños` int(11) DEFAULT NULL,
  `tarifa_aplicada` varchar(100) DEFAULT NULL,
  `deposito_resivido` varchar(100) DEFAULT NULL,
  `metodo_pago_deposito` varchar(20) DEFAULT NULL,
  `solicitudes_especiales` varchar(50) DEFAULT NULL,
  `estado_reserva` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `reservas`
--

INSERT INTO `reservas` (`id_reserva`, `fecha_creacion`, `id_cliente`, `fecha_llegada`, `fecha_salida`, `numero_noches`, `numero_habitaciones`, `id_tipo_habitacion`, `numero_huespedes_adultos`, `numero_huespedes_niños`, `tarifa_aplicada`, `deposito_resivido`, `metodo_pago_deposito`, `solicitudes_especiales`, `estado_reserva`) VALUES
(1, '2024-04-15', 1, '2024-04-20', '2024-04-22', 2, 1, 1, 2, 1, 'tarifa de paquete', 'deposito completo', 'tarjeta', 'vista a la ciudad', 'cancelada'),
(2, '2024-12-02', 2, '2024-12-10', '2024-12-15', 4, 1, 2, 1, 1, 'tarifa temporada', 'deposito confirmado', 'efectivo', 'vista a la montaña', 'confirmada'),
(3, '2024-06-11', 3, '2024-06-13', '2024-06-15', 1, 1, 3, 2, 0, 'tarifa estandar', 'deposito completo', 'tarjeta', 'vista al mar', 'pendiente'),
(4, '2024-04-15', 4, '2024-04-30', '2024-05-06', 6, 1, 4, 5, 3, 'tarifa de grupo', 'deposito parcial', 'tarjeta', 'vista a la montaña', 'cancelada');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `reserva_servicio`
--

CREATE TABLE `reserva_servicio` (
  `id_reserva_servicio` int(11) NOT NULL,
  `id_reserva` int(11) DEFAULT NULL,
  `id_servicio` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `salones`
--

CREATE TABLE `salones` (
  `id_salon` int(10) NOT NULL,
  `id_hotel` int(11) DEFAULT NULL,
  `nombre` varchar(100) NOT NULL,
  `ubicacion_en_hotel` varchar(50) DEFAULT NULL,
  `capacidad_maxima` varchar(50) DEFAULT NULL,
  `tamaño_en_m2` decimal(10,0) DEFAULT NULL,
  `configuraciones_posibles` varchar(50) DEFAULT NULL,
  `tarifas_segun_duracion` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `salones`
--

INSERT INTO `salones` (`id_salon`, `id_hotel`, `nombre`, `ubicacion_en_hotel`, `capacidad_maxima`, `tamaño_en_m2`, `configuraciones_posibles`, `tarifas_segun_duracion`) VALUES
(1, 1, 'salon 1', 'piso 5', '100 personas', 200, 'teatro', '50.00 hora'),
(2, 2, 'salon 2', 'piso 3', '50 personas', 100, 'reunion', '50.00 hora'),
(3, 3, 'salon 3', 'piso 5', '100 personas', 200, 'conferencia', '50.00 hora'),
(4, 4, 'salon 4', 'piso 12', '100 personas', 200, 'teatro', '50.00 hora');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `servicios`
--

CREATE TABLE `servicios` (
  `id_servicio` int(10) NOT NULL,
  `nombre_servicios_adicionales` varchar(200) NOT NULL,
  `descripcion` varchar(300) DEFAULT NULL,
  `horario_disponibilidad` varchar(50) DEFAULT NULL,
  `precio` decimal(10,0) DEFAULT NULL,
  `duracion_tipica` varchar(50) DEFAULT NULL,
  `capacidad_maxima` int(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `servicios`
--

INSERT INTO `servicios` (`id_servicio`, `nombre_servicios_adicionales`, `descripcion`, `horario_disponibilidad`, `precio`, `duracion_tipica`, `capacidad_maxima`) VALUES
(1, 'spa', 'nuestro hotel ofrece servicio de spa para hacer su estancia mas comoda', '24/7', 50, '30-60mn', 5),
(2, 'masaje', 'nuestro hotel ofrece servicios de masaje para hacer su estancia mas comoda', '24/7', 30, '30-40mn', 5),
(3, 'baño turco', 'nuestro hotel ofrece servicios baño turco para hacer su estancia mas comoda', '24/7', 100, '60mn', 2),
(4, 'tratamiento facial', 'nuestro hotel ofrece servicios de tratamiento facial para hacer su estancia mas comoda', '24/7', 40, '30-50mn', 5);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tarifas`
--

CREATE TABLE `tarifas` (
  `id_tarifas` int(10) NOT NULL,
  `id_tipo_habitacion` int(11) DEFAULT NULL,
  `id_temporada` int(11) DEFAULT NULL,
  `tarifa_base` decimal(10,0) NOT NULL,
  `impuestos` decimal(10,0) DEFAULT NULL,
  `descuento_por_estadia` decimal(10,0) DEFAULT NULL,
  `condiciones_especiales` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `tarifas`
--

INSERT INTO `tarifas` (`id_tarifas`, `id_tipo_habitacion`, `id_temporada`, `tarifa_base`, `impuestos`, `descuento_por_estadia`, `condiciones_especiales`) VALUES
(1, 1, 1, 200, 10, 20, 'calcelacion'),
(2, 2, 2, 150, 8, 12, 'pago'),
(3, 3, 3, 100, 5, 5, 'pendiente'),
(4, 4, 4, 200, 10, 20, 'cancelacion');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `temporadas`
--

CREATE TABLE `temporadas` (
  `id_temporada` int(10) NOT NULL,
  `nombre_temporada` varchar(20) DEFAULT NULL,
  `fecha_inicio` date NOT NULL,
  `fecha_fin` date NOT NULL,
  `factor_multiplicador_tarifa` decimal(10,0) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `temporadas`
--

INSERT INTO `temporadas` (`id_temporada`, `nombre_temporada`, `fecha_inicio`, `fecha_fin`, `factor_multiplicador_tarifa`) VALUES
(1, 'temporada baja', '2024-04-01', '2024-05-01', 1),
(2, 'temporada alta', '2024-11-10', '2025-01-30', 2),
(3, 'temporada meidaa', '2024-05-10', '2024-08-01', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tipos_habitacion`
--

CREATE TABLE `tipos_habitacion` (
  `id_tipo_habitacion` int(11) NOT NULL,
  `descripcion` varchar(50) NOT NULL,
  `maximo_huespedes` int(11) DEFAULT NULL,
  `tamaño_m2` decimal(10,0) DEFAULT NULL,
  `numero_camas` int(11) DEFAULT NULL,
  `tipo_camas` varchar(50) DEFAULT NULL,
  `amenidades_incluidas` varchar(300) DEFAULT NULL,
  `id_temporada` int(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `tipos_habitacion`
--

INSERT INTO `tipos_habitacion` (`id_tipo_habitacion`, `descripcion`, `maximo_huespedes`, `tamaño_m2`, `numero_camas`, `tipo_camas`, `amenidades_incluidas`, `id_temporada`) VALUES
(1, 'suite', 5, 50, 4, 'camas queen size', 'baño privado, jacuzzi, articulos de aseo personal, wifi, aire acondicionado, televicion', 1),
(2, 'doble', 4, 40, 2, 'cama matrimonial', 'toallas, wifi, televicion, artuculos de aseo personal', 2),
(3, 'individual', 2, 30, 1, 'cama individual', 'toallas, televicion, telefono', 3),
(4, 'familiar', 10, 100, 5, 'camas individuales', 'baño pribado, toallas, televicion, wifi', 4);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;


#============= buscar todas las tablas =====================

DELIMITER //

CREATE PROCEDURE sp_getHotelById(IN p_id_hotel INT)
BEGIN
    SELECT 
        id_hotel,
        nombre_hotel,
        categoria,
        direccion,
        telefono,
        correo,
        año_inauguracion,
        numero_total_habitantes,
        servicios_disponibles,
        horarios_check_in,
        horarios_check_out,
        gerente_responsable
    FROM hoteles
    WHERE id_hotel = p_id_hotel;
END //

DELIMITER ;


DELIMITER //

CREATE PROCEDURE sp_buscar_cliente(
    IN p_id_cliente INT
)
BEGIN
    SELECT * FROM clientes WHERE id_cliente = p_id_cliente;
END //

DELIMITER ;



DELIMITER //
CREATE PROCEDURE sp_buscarEmpleado (IN p_id_empleado INT)
BEGIN
    SELECT id_empleado, nombres, apellidos, cargo, telefono, correo, id_hotel
    FROM empleados
    WHERE id_empleado = p_id_empleado;
END //
DELIMITER ;




DELIMITER //
CREATE PROCEDURE sp_buscar_temporada(IN p_id_temporada INT)
BEGIN
    SELECT id_temporada, nombre_temporada, fecha_inicio, fecha_fin, factor_multiplicador_tarifa
    FROM temporadas
    WHERE id_temporada = p_id_temporada;
END //
DELIMITER ;



#==================eliminar todas las tablas ====================
DELIMITER //

CREATE PROCEDURE sp_deleteHotelById(IN p_id_hotel INT)
BEGIN
    DELETE FROM hoteles WHERE id_hotel = p_id_hotel;
END //

DELIMITER ;



DELIMITER $$

CREATE PROCEDURE sp_eliminar_cliente (
    IN p_id_cliente INT
)
BEGIN
    DELETE FROM clientes WHERE id_cliente = p_id_cliente;
END $$

DELIMITER ;



DELIMITER $$

CREATE PROCEDURE sp_deleteEmpleadoById(IN p_id_empleado INT)
BEGIN
    DELETE FROM empleados WHERE id_empleado = p_id_empleado;
END $$

DELIMITER ;


DELIMITER //
CREATE PROCEDURE sp_deleteTemporada(IN p_id_temporada INT)
BEGIN
    DELETE FROM temporadas WHERE id_temporada = p_id_temporada;
END //
DELIMITER ;



#================== actualizar todas las tablas =================

DELIMITER //

CREATE PROCEDURE sp_updateHotel(
    IN p_id_hotel INT,
    IN p_nombre_hotel VARCHAR(50),
    IN p_categoria INT,
    IN p_direccion VARCHAR(100),
    IN p_telefono INT,
    IN p_correo VARCHAR(100),
    IN p_año_inauguracion DECIMAL(10,0),
    IN p_numero_total_habitantes INT,
    IN p_servicios_disponibles VARCHAR(1000),
    IN p_horarios_check_in TIME,
    IN p_horarios_check_out TIME,
    IN p_gerente_responsable VARCHAR(50)
)
BEGIN
    UPDATE hoteles
    SET
        nombre_hotel = p_nombre_hotel,
        categoria = p_categoria,
        direccion = p_direccion,
        telefono = p_telefono,
        correo = p_correo,
        año_inauguracion = p_año_inauguracion,
        numero_total_habitantes = p_numero_total_habitantes,
        servicios_disponibles = p_servicios_disponibles,
        horarios_check_in = p_horarios_check_in,
        horarios_check_out = p_horarios_check_out,
        gerente_responsable = p_gerente_responsable
    WHERE id_hotel = p_id_hotel;
END //

DELIMITER ;


DELIMITER //

CREATE PROCEDURE sp_actualizar_cliente(
    IN p_id_cliente INT,
    IN p_nombre VARCHAR(100),
    IN p_apellido VARCHAR(100),
    IN p_documento_identidad INT,
    IN p_nacionalidad VARCHAR(50),
    IN p_fecha_nacimiento DATE,
    IN p_direccion VARCHAR(100),
    IN p_telefono INT,
    IN p_correo VARCHAR(100),
    IN p_preferencias_especiales VARCHAR(100),
    IN p_nivel_programa_fidelizacion VARCHAR(100)
)
BEGIN
    UPDATE clientes
    SET 
        nombre = p_nombre,
        apellido = p_apellido,
        documento_identidad = p_documento_identidad,
        nacionalidad = p_nacionalidad,
        fecha_nacimiento = p_fecha_nacimiento,
        direccion = p_direccion,
        telefono = p_telefono,
        correo = p_correo,
        preferencias_especiales = p_preferencias_especiales,
        nivel_programa_fidelizacion = p_nivel_programa_fidelizacion
    WHERE id_cliente = p_id_cliente;
END //

DELIMITER ;


DELIMITER $$

CREATE PROCEDURE sp_updateEmpleado(
    IN p_id_empleado INT,
    IN p_nombres VARCHAR(100),
    IN p_apellidos VARCHAR(100),
    IN p_cargo VARCHAR(100),
    IN p_telefono VARCHAR(50),
    IN p_correo VARCHAR(100),
    IN p_id_hotel INT
)
BEGIN
    UPDATE empleados
    SET
        nombres = p_nombres,
        apellidos = p_apellidos,
        cargo = p_cargo,
        telefono = p_telefono,
        correo = p_correo,
        id_hotel = p_id_hotel
    WHERE id_empleado = p_id_empleado;
END $$

DELIMITER ;



DELIMITER //
CREATE PROCEDURE sp_updateTemporada(
    IN p_id_temporada INT,
    IN p_nombre_temporada VARCHAR(255),
    IN p_fecha_inicio DATE,
    IN p_fecha_fin DATE,
    IN p_factor_multiplicador_tarifa DECIMAL(10,2)
)
BEGIN
    UPDATE temporadas
    SET nombre_temporada = p_nombre_temporada,
        fecha_inicio = p_fecha_inicio,
        fecha_fin = p_fecha_fin,
        factor_multiplicador_tarifa = p_factor_multiplicador_tarifa
    WHERE id_temporada = p_id_temporada;
END //
DELIMITER ;






#===================== guardar todas las tablas ================

DELIMITER //

CREATE PROCEDURE sp_insertHotel(
    IN p_id_hotel INT,
    IN p_nombre_hotel VARCHAR(50),
    IN p_categoria INT,
    IN p_direccion VARCHAR(100),
    IN p_telefono INT,
    IN p_correo VARCHAR(100),
    IN p_año_inauguracion DECIMAL(10,0),
    IN p_numero_total_habitantes INT,
    IN p_servicios_disponibles VARCHAR(1000),
    IN p_horarios_check_in TIME,
    IN p_horarios_check_out TIME,
    IN p_gerente_responsable VARCHAR(50)
)
BEGIN
    INSERT INTO hoteles (
        id_hotel, nombre_hotel, categoria, direccion, telefono, correo,
        año_inauguracion, numero_total_habitantes, servicios_disponibles,
        horarios_check_in, horarios_check_out, gerente_responsable
    ) VALUES (
        p_id_hotel, p_nombre_hotel, p_categoria, p_direccion, p_telefono, p_correo,
        p_año_inauguracion, p_numero_total_habitantes, p_servicios_disponibles,
        p_horarios_check_in, p_horarios_check_out, p_gerente_responsable
    );
END //

DELIMITER ;


DELIMITER //

CREATE PROCEDURE sp_insertar_cliente(
    IN p_nombre VARCHAR(100),
    IN p_apellido VARCHAR(100),
    IN p_documento_identidad INT,
    IN p_nacionalidad VARCHAR(50),
    IN p_fecha_nacimiento DATE,
    IN p_direccion VARCHAR(100),
    IN p_telefono INT,
    IN p_correo VARCHAR(100),
    IN p_preferencias_especiales VARCHAR(100),
    IN p_nivel_programa_fidelizacion VARCHAR(100)
)
BEGIN
    INSERT INTO clientes (
        nombre,
        apellido,
        documento_identidad,
        nacionalidad,
        fecha_nacimiento,
        direccion,
        telefono,
        correo,
        preferencias_especiales,
        nivel_programa_fidelizacion
    ) VALUES (
        p_nombre,
        p_apellido,
        p_documento_identidad,
        p_nacionalidad,
        p_fecha_nacimiento,
        p_direccion,
        p_telefono,
        p_correo,
        p_preferencias_especiales,
        p_nivel_programa_fidelizacion
    );
END //

DELIMITER ;



DELIMITER //
CREATE PROCEDURE sp_guardarEmpleado (
    IN p_id_empleado INT,
    IN p_nombres VARCHAR(100),
    IN p_apellidos VARCHAR(100),
    IN p_cargo VARCHAR(100),
    IN p_telefono VARCHAR(50),
    IN p_correo VARCHAR(100),
    IN p_id_hotel INT
)
BEGIN
    INSERT INTO empleados (id_empleado, nombres, apellidos, cargo, telefono, correo, id_hotel)
    VALUES (p_id_empleado, p_nombres, p_apellidos, p_cargo, p_telefono, p_correo, p_id_hotel);
END //
DELIMITER ;



DELIMITER //
CREATE PROCEDURE sp_insertTemporada(
    IN p_nombre_temporada VARCHAR(255),
    IN p_fecha_inicio DATE,
    IN p_fecha_fin DATE,
    IN p_factor_multiplicador_tarifa DECIMAL(10,2)
)
BEGIN
    INSERT INTO temporadas(nombre_temporada, fecha_inicio, fecha_fin, factor_multiplicador_tarifa)
    VALUES (p_nombre_temporada, p_fecha_inicio, p_fecha_fin, p_factor_multiplicador_tarifa);
END //
DELIMITER ;