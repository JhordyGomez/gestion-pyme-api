# Documentación del servicio: Autenticación y estado

**Servicio:** registro de usuarios e inicio de sesión
**Módulo del proyecto:** `app.py` (secciones `_registrar_usuario`, `_iniciar_sesion`)

## Endpoint 1 — Registro de usuario

- **Método:** POST
- **Ruta:** `/api/register`
- **Cuerpo (JSON):** `{"usuario": "...", "contrasena": "...", "rol": "..."}` (el rol es opcional; por defecto: vendedor)
- **Respuesta exitosa:** `201 {"mensaje": "Usuario registrado satisfactoriamente", "usuario": "..."}`
- **Errores:** `400` datos incompletos o JSON inválido · `409` el usuario ya existe

**Ejemplo de petición y respuesta:**
```json
// Request
{ "usuario": "ana", "contrasena": "Clave2026*" }
// Response 201
{ "mensaje": "Usuario registrado satisfactoriamente", "usuario": "ana" }
```

## Endpoint 2 — Inicio de sesión

- **Método:** POST
- **Ruta:** `/api/login`
- **Cuerpo (JSON):** `{"usuario": "...", "contrasena": "..."}`
- **Respuesta exitosa:** `200 {"mensaje": "Autenticación satisfactoria", "usuario": "...", "rol": "..."}`
- **Errores:** `400` datos incompletos · `401` error en la autenticación

## Endpoint 3 — Estado del servicio

- **Método:** GET
- **Ruta:** `/api/health`
- **Respuesta exitosa:** `200 {"estado": "Servicio en línea", "servicios": 6, ...}`

**Notas de diseño:** las contraseñas se comparan de forma directa por simplicidad
didáctica; en un entorno productivo deben almacenarse con funciones de cifrado
(hash) y el acceso debe protegerse con tokens de autenticación.
