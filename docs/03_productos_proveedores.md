# Documentación del servicio: Productos y Proveedores

**Servicio:** administración del inventario y de los proveedores
**Módulo del proyecto:** `app.py` (secciones de productos y proveedores)

## Endpoints de productos

| Método | Ruta | Función |
|--------|------|---------|
| GET | `/api/productos` | Lista todos los productos |
| POST | `/api/productos` | Registra un producto nuevo |
| PUT | `/api/productos/{id}` | Actualiza precio, stock o categoría |
| DELETE | `/api/productos/{id}` | Elimina un producto |

**Campos:** `nombre` (obligatorio), `categoria` (obligatoria), `precio` (obligatorio,
numérico ≥ 0), `stock` (numérico ≥ 0), `id_proveedor` (opcional).

**Ejemplo: crear un producto**
```json
// Request POST /api/productos
{ "nombre": "Arroz premium 1 kg", "categoria": "Granos", "precio": 4500,
  "stock": 120, "id_proveedor": 1 }
// Response 201
{ "mensaje": "Producto registrado satisfactoriamente", "id": 5 }
```

## Endpoints de proveedores

| Método | Ruta | Función |
|--------|------|---------|
| GET | `/api/proveedores` | Lista todos los proveedores |
| POST | `/api/proveedores` | Registra un proveedor nuevo |

**Campos:** `nombre` (obligatorio), `contacto`, `telefono`, `direccion` (opcionales).

## Códigos de respuesta

| Código | Significado |
|--------|-------------|
| 200 / 201 | Operación exitosa |
| 400 | Datos incompletos o valores numéricos no válidos (precio o stock negativos) |
| 404 | Producto no encontrado |

**Notas de diseño:** las validaciones numéricas garantizan la integridad del
inventario (regla de negocio: precio y stock ≥ 0), coherentes con las
restricciones CHECK del modelo de base de datos del proyecto.
