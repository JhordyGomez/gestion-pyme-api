# Documentación del servicio: Ventas y Reportes

**Servicio:** registro de ventas y reportes de gestión
**Módulo del proyecto:** `app.py` (secciones `_listar_ventas`, `_crear_venta`, `_obtener_venta`, `_reporte_resumen`)

## Endpoints de ventas

| Método | Ruta | Función |
|--------|------|---------|
| GET | `/api/ventas` | Lista todas las ventas |
| POST | `/api/ventas` | Registra una venta con su detalle |
| GET | `/api/ventas/{id}` | Consulta una venta con sus productos |

## Reglas de negocio de la venta

1. El cliente debe estar registrado (validación de existencia).
2. La venta debe incluir al menos un producto con cantidad mayor que cero.
3. El subtotal de cada producto es `precio × cantidad`.
4. **Descuento del 20%** cuando el total supera $50.000.
5. El detalle de la venta se registra producto por producto.

## Ejemplo: registrar una venta

```json
// Request POST /api/ventas
{ "id_cliente": 1,
  "usuario": "admin",
  "productos": [
    { "id_producto": 1, "cantidad": 5 },
    { "id_producto": 4, "cantidad": 4 }
  ] }
// Response 201
{ "mensaje": "Venta registrada satisfactoriamente", "id_venta": 3,
  "subtotal": 85300, "descuento": 17060, "total_a_pagar": 68240 }
```

## Endpoint de reportes

| Método | Ruta | Función |
|--------|------|---------|
| GET | `/api/reportes/resumen` | Resumen del periodo de gestión |

**Respuesta:**
```json
{ "mensaje": "Resumen del periodo", "ventas_registradas": 3,
  "ingresos_totales": 153500, "clientes_registrados": 3,
  "productos_en_inventario": 4, "unidades_vendidas": 12 }
```

## Códigos de respuesta

| Código | Significado |
|--------|-------------|
| 200 / 201 | Operación exitosa |
| 400 | Datos incompletos o cantidades no válidas |
| 404 | Cliente, producto o venta no encontrados |
