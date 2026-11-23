# -*- coding: utf-8 -*-
"""
=============================================================================
ALMACÉN DE DATOS EN MEMORIA DEL SISTEMA DE GESTIÓN PARA PYMES
=============================================================================
Evidencia:  GA7-220501096-AA5-EV03 - Diseño y desarrollo de servicios web (proyecto)
Aprendiz:   Jhordy Dayan Gómez Olaya - Ficha 3186690

Descripción:
    Módulo que contiene las estructuras de datos del proyecto y los datos
    de prueba (semillas). La estructura replica el modelo relacional
    diseñado para la base de datos gestion_pyme:
        usuarios -> ventas <- clientes
        productos -> detalle_venta -> ventas
        proveedores -> productos

Nota:
    Este almacén es temporal (memoria del servicio). En un entorno productivo
    estos datos se almacenarían en una base de datos MySQL.
=============================================================================
"""

# ---------------------------------------------------------------------------
# TABLA USUARIOS: personal que opera el sistema (administrador, vendedor...).
# Estructura: { "usuario": {"contrasena": "...", "rol": "..."} }
# ---------------------------------------------------------------------------
usuarios = {
    "admin": {"contrasena": "Admin123*", "rol": "administrador"},
}

# ---------------------------------------------------------------------------
# TABLA CLIENTES: personas o empresas que compran en la PYME.
# ---------------------------------------------------------------------------
clientes = {
    1: {"documento": "CC 1.023.445", "nombre": "María López", "telefono": "300 456 7890",
        "correo": "maria@correo.com", "direccion": "Calle 10 # 5-20"},
    2: {"documento": "CC 1.067.221", "nombre": "Carlos Ruiz", "telefono": "310 123 4567",
        "correo": "carlos@correo.com", "direccion": "Carrera 8 # 12-34"},
    3: {"documento": "NIT 901.456", "nombre": "Distribuidora El Sol", "telefono": "601 555 1212",
        "correo": "ventas@elsol.co", "direccion": "Av. Principal # 45-67"},
}

# ---------------------------------------------------------------------------
# TABLA PROVEEDORES: empresas que suministran los productos.
# ---------------------------------------------------------------------------
proveedores = {
    1: {"nombre": "Agroindustrias del Sur", "contacto": "Laura Mendoza",
        "telefono": "320 555 0101", "direccion": "Zona Industrial, San Alberto"},
    2: {"nombre": "Distribuciones Nacionales", "contacto": "Pedro Ramírez",
        "telefono": "315 555 0202", "direccion": "Bodega 7, Cúcuta"},
}

# ---------------------------------------------------------------------------
# TABLA PRODUCTOS: inventario de la PYME.
# ---------------------------------------------------------------------------
productos = {
    1: {"nombre": "Arroz premium 1 kg", "categoria": "Granos", "precio": 4500,
        "stock": 120, "id_proveedor": 1},
    2: {"nombre": "Aceite de oliva 500 ml", "categoria": "Abarrotes", "precio": 18900,
        "stock": 45, "id_proveedor": 2},
    3: {"nombre": "Detergente líquido", "categoria": "Aseo", "precio": 12300,
        "stock": 80, "id_proveedor": 2},
    4: {"nombre": "Café molido 250 g", "categoria": "Bebidas", "precio": 15700,
        "stock": 60, "id_proveedor": 1},
}

# ---------------------------------------------------------------------------
# TABLA VENTAS: cabecera de cada venta realizada.
# ---------------------------------------------------------------------------
ventas = {
    1: {"fecha": "2026-11-22", "id_cliente": 1, "usuario": "admin", "total": 85000},
    2: {"fecha": "2026-11-22", "id_cliente": 2, "usuario": "admin", "total": 120500},
}

# ---------------------------------------------------------------------------
# TABLA DETALLE_VENTA: productos y cantidades de cada venta.
# ---------------------------------------------------------------------------
detalle_venta = {
    1: {"id_venta": 1, "id_producto": 1, "cantidad": 5, "subtotal": 22500},
    2: {"id_venta": 1, "id_producto": 4, "cantidad": 4, "subtotal": 62800},
    3: {"id_venta": 2, "id_producto": 2, "cantidad": 3, "subtotal": 56700},
}

# ---------------------------------------------------------------------------
# CONTADORES DE IDENTIFICADORES: simulan el AUTO_INCREMENT de la base de datos.
# ---------------------------------------------------------------------------
contadores = {
    "clientes": max(clientes.keys(), default=0) + 1,
    "proveedores": max(proveedores.keys(), default=0) + 1,
    "productos": max(productos.keys(), default=0) + 1,
    "ventas": max(ventas.keys(), default=0) + 1,
    "detalle_venta": max(detalle_venta.keys(), default=0) + 1,
}


def nuevo_id(tabla):
    """Genera un identificador único para la tabla indicada (AUTO_INCREMENT)."""
    identificador = contadores[tabla]
    contadores[tabla] = identificador + 1
    return identificador
