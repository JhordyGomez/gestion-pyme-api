# API del Sistema de Gestión para PYMEs

**Evidencia:** GA7-220501096-AA5-EV03 — Diseño y desarrollo de servicios web (proyecto)
**Componente formativo:** Construcción de API
**Aprendiz:** Jhordy Dayan Gómez Olaya — Ficha 3186690

## 1. Descripción del proyecto

Servicios web (API REST) que implementan las funcionalidades del sistema web de
gestión para PYMEs del sur del Cesar: autenticación de usuarios, administración de
clientes, productos y proveedores, registro de ventas con descuentos y reportes
de gestión. Todos los servicios intercambian datos en formato JSON.

**Arquitectura (cliente–servidor en capas):**

```
Cliente (Postman / navegador / aplicación web)
        |  peticiones HTTP + JSON
        v
Servicios web (app.py)  ->  Lógica de cada servicio
        |
        v
Almacén de datos (datos.py) -> modelo relacional gestion_pyme
```

## 2. Resumen de servicios (endpoints)

| Servicio | Endpoints | Documentación |
|----------|-----------|---------------|
| Autenticación | `POST /api/register`, `POST /api/login` | docs/01_autenticacion.md |
| Clientes | `GET/POST /api/clientes`, `GET/PUT/DELETE /api/clientes/{id}` | docs/02_clientes.md |
| Productos y proveedores | `GET/POST /api/productos`, `PUT/DELETE /api/productos/{id}`, `GET/POST /api/proveedores` | docs/03_productos_proveedores.md |
| Ventas y reportes | `GET/POST /api/ventas`, `GET /api/ventas/{id}`, `GET /api/reportes/resumen` | docs/04_ventas_reportes.md |
| Estado | `GET /api/health` | docs/01_autenticacion.md |

## 3. Reglas de negocio del sistema

1. El documento de identidad de un cliente es único.
2. El precio y el stock de los productos no pueden ser negativos.
3. Una venta aplica **descuento del 20%** cuando el total supera $50.000.
4. El stock de los productos se relaciona con la venta mediante el detalle.
5. Toda respuesta es JSON con el campo `mensaje` (éxito) o `error` (falla).

## 4. Ejecución del proyecto

```bash
python app.py
# API del sistema de gestión iniciada en http://localhost:8000
```

## 5. Tecnologías y versionamiento

- Lenguaje: Python 3 (biblioteca estándar: `http.server`, `json`, `re`)
- Modelo de datos: módulo `datos.py` (replica el modelo relacional `gestion_pyme`)
- Control de versiones: Git (historial de commits) + repositorio remoto en GitHub
