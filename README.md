# Solicitud de Desbloqueo
 Script python que automatiza el envió de la solicitud de Desbloqueo del Blotloader a Xiaomi

# Como funciona

Solo es desplegar el script en Github, con el archivo.yml que contiene la instrucción de ejecutar el script de python 30 minutos antes de que sean las 12 am hora Pekín China y termina su ejecución apenas reciba una respuesta. Se tiene que poner una cookie de sesión en el archivo new_bbs justo en la primera línea,ojo tienes que ponerlo o unas horas antes o justo antes de que sea ejecutado el script por github , se tienen que cambiar todos los días porque en script se ejecuta todos los días hasta que sea aceptada la solicitud

# Ayuda que proporciona

* Mejora la eficiencia en un 80%
* Solo es poner la cookies y esperar
* No tienes que preocuparte por todos  los días esperar a las 12 para ejecutar tu mismo el archivo
* No influyen factores como la velocidad de conexión

## Configuración en GitHub

1. Sube este repositorio a GitHub.
2. Ve a Settings > Secrets and variables > Actions y agrega cualquier secreto necesario (si usas email, configura EMAIL_SENDER y EMAIL_PASSWORD).
3. El workflow se ejecutará automáticamente todos los días a las 11:30 PM hora de Pekín.
4. Antes de cada ejecución, actualiza el archivo `new_bbs` con la cookie válida de Xiaomi Community.

### Archivo new_bbs

Coloca la cookie de sesión de Xiaomi en la primera línea del archivo `new_bbs`. Esta cookie debe ser válida y actualizada diariamente.

## Envío de notificaciones por correo

El script ahora puede enviar un correo electrónico con el resultado final de la solicitud a `sergiofalconp24@gmail.com`.

Configura estas variables de entorno:

- `EMAIL_SENDER`: dirección de correo remitente
- `EMAIL_PASSWORD`: contraseña o token de aplicación SMTP
- `EMAIL_RECIPIENT`: dirección de destino (predeterminado `sergiofalconp24@gmail.com`)
- `EMAIL_SMTP_SERVER`: servidor SMTP (predeterminado `smtp.gmail.com`)
- `EMAIL_SMTP_PORT`: puerto SMTP (predeterminado `587`)

Por ejemplo:

```bash
export EMAIL_SENDER="tu-email@gmail.com"
export EMAIL_PASSWORD="tu_contraseña_o_token"
export EMAIL_RECIPIENT="sergiofalconp24@gmail.com"
```
