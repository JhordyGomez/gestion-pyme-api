# -*- coding: utf-8 -*-
"""
=============================================================================
SERVICIOS WEB (API REST) DEL SISTEMA DE GESTIÓN PARA PYMES
=============================================================================
Evidencia:   GA7-220501096-AA5-EV03 - Diseño y desarrollo de servicios web (proyecto)
Componente:  Construcción de API
Aprendiz:    Jhordy Dayan Gómez Olaya - Ficha 3186690

Descripción:
    API web que implementa los servicios necesarios para el sistema de
    gestión de una PYME del sur del Cesar: autenticación de usuarios,
    administración de clientes, productos y proveedores, registro de ventas
    y reportes de gestión. Todos los servicios intercambian datos en formato
    JSON y se documentan en la carpeta docs/ del proyecto.

Servicios (endpoints):
    Autenticación ...... POST /api/register | POST /api/login
    Clientes ........... GET/POST /api/clientes | GET/PUT/DELETE /api/clientes/{id}
    Productos .......... GET/POST /api/productos | PUT/DELETE /api/productos/{id}
    Proveedores ........ GET/POST /api/proveedores
    Ventas ............. GET/POST /api/ventas | GET /api/ventas/{id}
    Reportes ........... GET /api/reportes/resumen
    Estado ............. GET /api/health

Tecnología: Python 3 (biblioteca estándar: http.server, json, re).
Ejecución:  python app.py  (servicio en http://localhost:8000)
=============================================================================
"""

# Importación de las librerías necesarias (biblioteca estándar de Python)
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import re

# Importación del almacén de datos del proyecto (módulo datos.py)
from datos import (usuarios, clientes, proveedores, productos,
                   ventas, detalle_venta, nuevo_id)

# Puerto en el que escucha el servicio web
PUERTO = 8000


class ManejadorServicios(BaseHTTPRequestHandler):
    """Manejador central de las peticiones HTTP de todos los servicios."""

    # ------------------------------------------------------------------
    # UTILIDADES GENERALES
    # ------------------------------------------------------------------
    def _responder(self, codigo, datos):
        """Envía una respuesta JSON con el código de estado indicado."""
        cuerpo = json.dumps(datos, ensure_ascii=False).encode("utf-8")
        self.send_response(codigo)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(cuerpo)))
        self.end_headers()
        self.wfile.write(cuerpo)

    def _leer_json(self):
        """Lee y convierte el cuerpo JSON de la petición; devuelve None si no es válido."""
        longitud = int(self.headers.get("Content-Length", 0))
        crudo = self.rfile.read(longitud) if longitud else b"{}"
        try:
            return json.loads(crudo.decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            return None

    def _exigir_campos(self, datos, campos):
        """Valida que el cuerpo contenga todos los campos obligatorios."""
        if datos is None:
            return "El cuerpo de la petición debe ser JSON válido"
        faltantes = [c for c in campos if not str(datos.get(c, "")).strip()]
        if faltantes:
            return "Datos incompletos: campos requeridos -> " + ", ".join(faltantes)
        return None

    # ------------------------------------------------------------------
    # SERVICIO 1: AUTENTICACIÓN (POST /api/register | POST /api/login)
    # ------------------------------------------------------------------
    def _registrar_usuario(self):
        datos = self._leer_json()
        error = self._exigir_campos(datos, ["usuario", "contrasena"])
        if error:
            self._responder(400, {"error": error})
            return
        usuario = str(datos["usuario"]).strip()
        if usuario in usuarios:
            self._responder(409, {"error": "El usuario ya existe"})
            return
        usuarios[usuario] = {"contrasena": str(datos["contrasena"]).strip(),
                             "rol": str(datos.get("rol", "vendedor")).strip()}
        self._responder(201, {"mensaje": "Usuario registrado satisfactoriamente",
                              "usuario": usuario})

    def _iniciar_sesion(self):
        datos = self._leer_json()
        error = self._exigir_campos(datos, ["usuario", "contrasena"])
        if error:
            self._responder(400, {"error": error})
            return
        usuario = str(datos["usuario"]).strip()
        clave = str(datos["contrasena"]).strip()
        if usuario in usuarios and usuarios[usuario]["contrasena"] == clave:
            self._responder(200, {"mensaje": "Autenticación satisfactoria",
                                  "usuario": usuario, "rol": usuarios[usuario]["rol"]})
        else:
            self._responder(401, {"error": "Error en la autenticación"})

    # ------------------------------------------------------------------
    # SERVICIO 2: CLIENTES (GET/POST /api/clientes | GET/PUT/DELETE /api/clientes/{id})
    # ------------------------------------------------------------------
    def _listar_clientes(self):
        lista = [{"id": i, **c} for i, c in clientes.items()]
        self._responder(200, {"clientes": lista, "total": len(lista)})

    def _crear_cliente(self):
        datos = self._leer_json()
        error = self._exigir_campos(datos, ["documento", "nombre"])
        if error:
            self._responder(400, {"error": error})
            return
        # El documento de identidad debe ser único (regla de integridad)
        if any(c["documento"] == datos["documento"] for c in clientes.values()):
            self._responder(409, {"error": "Ya existe un cliente con ese documento"})
            return
        identificador = nuevo_id("clientes")
        clientes[identificador] = {
            "documento": str(datos["documento"]).strip(),
            "nombre": str(datos["nombre"]).strip(),
            "telefono": str(datos.get("telefono", "")).strip(),
            "correo": str(datos.get("correo", "")).strip(),
            "direccion": str(datos.get("direccion", "")).strip(),
        }
        self._responder(201, {"mensaje": "Cliente registrado satisfactoriamente",
                              "id": identificador})

    def _obtener_cliente(self, identificador):
        if identificador not in clientes:
            self._responder(404, {"error": "Cliente no encontrado"})
            return
        self._responder(200, {"id": identificador, **clientes[identificador]})

    def _actualizar_cliente(self, identificador):
        if identificador not in clientes:
            self._responder(404, {"error": "Cliente no encontrado"})
            return
        datos = self._leer_json()
        if datos is None:
            self._responder(400, {"error": "El cuerpo de la petición debe ser JSON válido"})
            return
        for campo in ("documento", "nombre", "telefono", "correo", "direccion"):
            if campo in datos:
                clientes[identificador][campo] = str(datos[campo]).strip()
        self._responder(200, {"mensaje": "Cliente actualizado satisfactoriamente",
                              "id": identificador})

    def _eliminar_cliente(self, identificador):
        if identificador not in clientes:
            self._responder(404, {"error": "Cliente no encontrado"})
            return
        del clientes[identificador]
        self._responder(200, {"mensaje": "Cliente eliminado satisfactoriamente"})

    # ------------------------------------------------------------------
    # SERVICIO 3: PRODUCTOS (GET/POST /api/productos | PUT/DELETE /api/productos/{id})
    # ------------------------------------------------------------------
    def _listar_productos(self):
        lista = [{"id": i, **p} for i, p in productos.items()]
        self._responder(200, {"productos": lista, "total": len(lista)})

    def _crear_producto(self):
        datos = self._leer_json()
        error = self._exigir_campos(datos, ["nombre", "categoria", "precio"])
        if error:
            self._responder(400, {"error": error})
            return
        try:
            precio = float(datos["precio"])
            stock = int(datos.get("stock", 0))
        except (TypeError, ValueError):
            self._responder(400, {"error": "El precio y el stock deben ser valores numéricos"})
            return
        if precio < 0 or stock < 0:
            self._responder(400, {"error": "El precio y el stock no pueden ser negativos"})
            return
        identificador = nuevo_id("productos")
        productos[identificador] = {
            "nombre": str(datos["nombre"]).strip(),
            "categoria": str(datos["categoria"]).strip(),
            "precio": precio,
            "stock": stock,
            "id_proveedor": datos.get("id_proveedor"),
        }
        self._responder(201, {"mensaje": "Producto registrado satisfactoriamente",
                              "id": identificador})

    def _actualizar_producto(self, identificador):
        if identificador not in productos:
            self._responder(404, {"error": "Producto no encontrado"})
            return
        datos = self._leer_json()
        if datos is None:
            self._responder(400, {"error": "El cuerpo de la petición debe ser JSON válido"})
            return
        for campo in ("nombre", "categoria", "id_proveedor"):
            if campo in datos:
                productos[identificador][campo] = datos[campo]
        for campo in ("precio", "stock"):
            if campo in datos:
                try:
                    productos[identificador][campo] = float(datos[campo])
                except (TypeError, ValueError):
                    self._responder(400, {"error": f"El campo {campo} debe ser numérico"})
                    return
        self._responder(200, {"mensaje": "Producto actualizado satisfactoriamente",
                              "id": identificador})

    def _eliminar_producto(self, identificador):
        if identificador not in productos:
            self._responder(404, {"error": "Producto no encontrado"})
            return
        del productos[identificador]
        self._responder(200, {"mensaje": "Producto eliminado satisfactoriamente"})

    # ------------------------------------------------------------------
    # SERVICIO 4: PROVEEDORES (GET/POST /api/proveedores)
    # ------------------------------------------------------------------
    def _listar_proveedores(self):
        lista = [{"id": i, **p} for i, p in proveedores.items()]
        self._responder(200, {"proveedores": lista, "total": len(lista)})

    def _crear_proveedor(self):
        datos = self._leer_json()
        error = self._exigir_campos(datos, ["nombre"])
        if error:
            self._responder(400, {"error": error})
            return
        identificador = nuevo_id("proveedores")
        proveedores[identificador] = {
            "nombre": str(datos["nombre"]).strip(),
            "contacto": str(datos.get("contacto", "")).strip(),
            "telefono": str(datos.get("telefono", "")).strip(),
            "direccion": str(datos.get("direccion", "")).strip(),
        }
        self._responder(201, {"mensaje": "Proveedor registrado satisfactoriamente",
                              "id": identificador})

    # ------------------------------------------------------------------
    # SERVICIO 5: VENTAS (GET/POST /api/ventas | GET /api/ventas/{id})
    # ------------------------------------------------------------------
    def _listar_ventas(self):
        lista = [{"id": i, **v} for i, v in ventas.items()]
        self._responder(200, {"ventas": lista, "total": len(lista)})

    def _crear_venta(self):
        datos = self._leer_json()
        error = self._exigir_campos(datos, ["id_cliente", "productos"])
        if error:
            self._responder(400, {"error": error})
            return
        # Validación: el cliente debe existir
        try:
            id_cliente = int(datos["id_cliente"])
        except (TypeError, ValueError):
            self._responder(400, {"error": "El id_cliente debe ser un número entero"})
            return
        if id_cliente not in clientes:
            self._responder(404, {"error": "Cliente no encontrado"})
            return
        items = datos["productos"]
        if not isinstance(items, list) or not items:
            self._responder(400, {"error": "Debe enviar al menos un producto en la venta"})
            return
        # Cálculo del total y descuento automático del 20% si supera 50000
        total = 0.0
        detalles = []
        for item in items:
            try:
                id_producto = int(item["id_producto"])
                cantidad = int(item["cantidad"])
            except (TypeError, ValueError, KeyError):
                self._responder(400, {"error": "Cada producto requiere id_producto y cantidad numéricos"})
                return
            if id_producto not in productos:
                self._responder(404, {"error": f"El producto {id_producto} no existe"})
                return
            if cantidad <= 0:
                self._responder(400, {"error": "La cantidad debe ser mayor que cero"})
                return
            subtotal = productos[id_producto]["precio"] * cantidad
            total += subtotal
            detalles.append({"id_producto": id_producto, "cantidad": cantidad,
                             "subtotal": subtotal})
        # Regla de negocio: descuento del 20% en compras mayores a 50000
        descuento = total * 0.20 if total > 50000 else 0.0
        pago = total - descuento
        id_venta = nuevo_id("ventas")
        ventas[id_venta] = {"fecha": "2026-11-23", "id_cliente": id_cliente,
                            "usuario": str(datos.get("usuario", "admin")).strip(),
                            "total": pago}
        for det in detalles:
            clave = nuevo_id("detalle_venta")
            detalle_venta[clave] = {"id_venta": id_venta, **det}
        self._responder(201, {
            "mensaje": "Venta registrada satisfactoriamente",
            "id_venta": id_venta,
            "subtotal": total,
            "descuento": descuento,
            "total_a_pagar": pago,
        })

    def _obtener_venta(self, identificador):
        if identificador not in ventas:
            self._responder(404, {"error": "Venta no encontrada"})
            return
        items = [{"id": i, **d} for i, d in detalle_venta.items()
                 if d["id_venta"] == identificador]
        self._responder(200, {"id": identificador, **ventas[identificador],
                              "productos": items})

    # ------------------------------------------------------------------
    # SERVICIO 6: REPORTES (GET /api/reportes/resumen)
    # ------------------------------------------------------------------
    def _reporte_resumen(self):
        total_ventas = len(ventas)
        ingresos = sum(v["total"] for v in ventas.values())
        unidades = sum(d["cantidad"] for d in detalle_venta.values())
        self._responder(200, {
            "mensaje": "Resumen del periodo",
            "ventas_registradas": total_ventas,
            "ingresos_totales": ingresos,
            "clientes_registrados": len(clientes),
            "productos_en_inventario": len(productos),
            "unidades_vendidas": unidades,
        })

    # ------------------------------------------------------------------
    # ENRUTADOR DE PETICIONES POST
    # ------------------------------------------------------------------
    def do_POST(self):
        if self.path == "/api/register":
            self._registrar_usuario()
        elif self.path == "/api/login":
            self._iniciar_sesion()
        elif self.path == "/api/clientes":
            self._crear_cliente()
        elif self.path == "/api/productos":
            self._crear_producto()
        elif self.path == "/api/proveedores":
            self._crear_proveedor()
        elif self.path == "/api/ventas":
            self._crear_venta()
        else:
            self._responder(404, {"error": "Ruta no encontrada"})

    # ------------------------------------------------------------------
    # ENRUTADOR DE PETICIONES GET
    # ------------------------------------------------------------------
    def do_GET(self):
        # Rutas con identificador numérico al final
        coincidencia = re.match(r"^/api/(clientes|productos|ventas)/(\d+)$", self.path)
        if coincidencia:
            recurso, identificador = coincidencia.group(1), int(coincidencia.group(2))
            if recurso == "clientes":
                self._obtener_cliente(identificador)
            elif recurso == "productos":
                if identificador in productos:
                    self._responder(200, {"id": identificador, **productos[identificador]})
                else:
                    self._responder(404, {"error": "Producto no encontrado"})
            else:
                self._obtener_venta(identificador)
        elif self.path == "/api/health":
            self._responder(200, {"estado": "Servicio en línea",
                                  "servicios": 6, "clientes": len(clientes),
                                  "productos": len(productos), "ventas": len(ventas)})
        elif self.path == "/api/clientes":
            self._listar_clientes()
        elif self.path == "/api/productos":
            self._listar_productos()
        elif self.path == "/api/proveedores":
            self._listar_proveedores()
        elif self.path == "/api/ventas":
            self._listar_ventas()
        elif self.path == "/api/reportes/resumen":
            self._reporte_resumen()
        else:
            self._responder(404, {"error": "Ruta no encontrada"})

    # ------------------------------------------------------------------
    # ENRUTADOR DE PETICIONES PUT
    # ------------------------------------------------------------------
    def do_PUT(self):
        coincidencia = re.match(r"^/api/(clientes|productos)/(\d+)$", self.path)
        if not coincidencia:
            self._responder(404, {"error": "Ruta no encontrada"})
            return
        recurso, identificador = coincidencia.group(1), int(coincidencia.group(2))
        if recurso == "clientes":
            self._actualizar_cliente(identificador)
        else:
            self._actualizar_producto(identificador)

    # ------------------------------------------------------------------
    # ENRUTADOR DE PETICIONES DELETE
    # ------------------------------------------------------------------
    def do_DELETE(self):
        coincidencia = re.match(r"^/api/(clientes|productos)/(\d+)$", self.path)
        if not coincidencia:
            self._responder(404, {"error": "Ruta no encontrada"})
            return
        recurso, identificador = coincidencia.group(1), int(coincidencia.group(2))
        if recurso == "clientes":
            self._eliminar_cliente(identificador)
        else:
            self._eliminar_producto(identificador)

    # Silenciar los mensajes de log para mayor claridad en la consola
    def log_message(self, formato, *args):
        pass


def iniciar_servicio():
    """Inicia el servidor web y queda a la espera de peticiones."""
    servidor = ThreadingHTTPServer(("localhost", PUERTO), ManejadorServicios)
    print(f"API del sistema de gestión iniciada en http://localhost:{PUERTO}")
    print("Servicios: autenticación, clientes, productos, proveedores, ventas, reportes")
    servidor.serve_forever()


# Punto de entrada del programa
if __name__ == "__main__":
    iniciar_servicio()
