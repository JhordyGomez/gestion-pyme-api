# Documentación del servicio: Clientes

**Servicio:** administración de los clientes de la PYME
**Módulo del proyecto:** `app.py` (secciones `_listar_clientes`, `_crear_cliente`, `_obtener_cliente`, `_actualizar_cliente`, `_eliminar_cliente`)

## Endpoints

| Método | Ruta | Función |
|--------|------|---------|
| GET | `/api/clientes` | Lista todos los clientes |
| POST | `/api/clientes` | Registra un cliente nuevo |
| GET | `/api/clientes/{id}` | Consulta un cliente por su identificador |
| PUT | `/api/clientes/{id}` | Actualiza los datos de un cliente |
| DELETE | `/api/clientes/{id}` | Elimina un cliente |

## Campos del cliente

| Campo | Tipo | Obligatorio | Restricción |
|-------|------|-------------|-------------|
| documento | texto | Sí | Único (no se admiten duplicados) |
| nombre | texto | Sí | — |
| telefono | texto | No | — |
| correo | texto | No | — |
| direccion | texto | No | — |

## Ejemplo: crear un cliente

```json
// Request POST /api/clientes
{ "documento": "CC 1.111.222", "nombre": "Ana Torres",
  "telefono": "315 000 1111", "correo": "ana@correo.com", "direccion": "Calle 5 # 3-20" }
// Response 201
{ "mensaje": "Cliente registrado satisfactoriamente", "id": 4 }
```

## Códigos de respuesta

| Código | Significado |
|--------|-------------|
| 200 / 201 | Operación exitosa |
| 400 | Datos incompletos o no válidos |
| 404 | Cliente no encontrado |
| 409 | Documento de identidad duplicado |
