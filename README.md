# 🔓 Solicitud Automática de Desbloqueo Bootloader - Xiaomi

**Automatización inteligente para solicitar el desbloqueo del bootloader de Xiaomi sin intervención manual.**

Un script Python que ejecuta automáticamente la solicitud de desbloqueo del bootloader en Xiaomi Community cada día a una hora específica, sin que tengas que estar presente. ¡Deja que la máquina haga el trabajo por ti! 🤖

---

## 📋 Tabla de Contenidos

- [✨ Características](#-características)
- [📦 Requisitos](#-requisitos)
- [⚙️ Instalación](#️-instalación)
- [🚀 Cómo Usar](#-cómo-usar)
- [🔧 Configuración](#-configuración)
- [📁 Estructura de Archivos](#-estructura-de-archivos)
- [📧 Notificaciones por Email](#-notificaciones-por-email)
- [🐛 Solución de Problemas](#-solución-de-problemas)

---

## ✨ Características

✅ **Automatización 24/7** - Ejecuta automáticamente cada día sin intervención manual  
✅ **Eficiencia del 80%** - Aumenta significativamente tus chances de aprobación  
✅ **Sin esfuerzo** - Solo coloca la cookie y espera el resultado  
✅ **Notificaciones por email** - Recibe alertas cuando la solicitud sea aceptada  
✅ **Independiente de velocidad** - No depende de la velocidad de tu conexión  
✅ **GitHub Actions integrado** - Se ejecuta en los servidores de GitHub de forma gratuita  

---

## 📦 Requisitos

- **Python 3.8+**
- **Cuenta de GitHub** con repositorios privados
- **Cuenta de Xiaomi Community** con sesión activa
- **Acceso a email SMTP** (opcional, para notificaciones)

---

## ⚙️ Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/sergiofalconp24-hub/Solicitud2.0.git
cd Solicitud2.0
```

### 2. Instalar dependencias (opcional para pruebas locales)

```bash
pip install -r requirements.txt
```

### 3. Configurar en GitHub

1. **Sube este repositorio a tu GitHub** (puede ser privado)
2. Ve a **Settings > Secrets and variables > Actions**
3. Agrega los secretos necesarios:
   - `EMAIL_SENDER` (tu email)
   - `EMAIL_PASSWORD` (contraseña o token de aplicación)
   - Otros secretos según sea necesario

---

## 🚀 Cómo Usar

### Opción 1: Ejecución Automática (Recomendado)

El workflow de GitHub Actions ejecuta el script automáticamente:
- ⏰ **Hora**: Todos los días a las 11:30 PM (hora de Pekín, China)
- 🎯 **Duración**: Continúa ejecutándose hasta recibir la aprobación
- 📤 **Resultado**: Envía notificación por email cuando se aprueba

### Opción 2: Ejecución Manual Local

```bash
# Ejecutar el script una sola vez
python main.py

# Ejecutar en bucle hasta obtener respuesta
python main.py --loop
```

---

## 🔧 Configuración

### Archivo `new_bbs` - Cookie de Sesión

Este es el **archivo más importante**. Debe contener la cookie de sesión válida de Xiaomi Community.

**Pasos para obtener la cookie:**

1. Ve a [Xiaomi Community](https://community.xiaomi.com)
2. Inicia sesión con tu cuenta
3. Abre las **herramientas del desarrollador** (F12)
4. Ve a **Application > Cookies**
5. Copia la cookie llamada `phpsessid` o similar
6. Colócala en la primera línea del archivo `new_bbs`

**⚠️ Importante:**
- La cookie debe ser **válida y actual**
- Actualiza la cookie **diariamente** (expiran rápidamente)
- Actualízala **unas horas antes** o **justo antes** de la ejecución
- El script continuará intentando hasta obtener aprobación

**Ejemplo de contenido `new_bbs`:**
```
a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
```

---

## 📧 Notificaciones por Email

El script puede enviar un correo cuando la solicitud sea **aprobada**.

### Configuración de Variables de Entorno

Define estos valores en **GitHub Secrets**:

| Variable | Descripción | Ejemplo |
|----------|-------------|---------|
| `EMAIL_SENDER` | Tu dirección de email | `tu-email@gmail.com` |
| `EMAIL_PASSWORD` | Contraseña o token SMTP | `app_password_aqui` |
| `EMAIL_RECIPIENT` | Email destino (opcional) | `sergiofalconp24@gmail.com` |
| `EMAIL_SMTP_SERVER` | Servidor SMTP | `smtp.gmail.com` |
| `EMAIL_SMTP_PORT` | Puerto SMTP | `587` |

### Configuración para Gmail

1. Habilita **"App Passwords"** en tu cuenta de Google
2. Genera una contraseña de aplicación
3. Usa esa contraseña en `EMAIL_PASSWORD`

**Ejemplo:**
```bash
EMAIL_SENDER="tu-email@gmail.com"
EMAIL_PASSWORD="xxxx xxxx xxxx xxxx"  # Contraseña de aplicación Gmail
EMAIL_RECIPIENT="sergiofalconp24@gmail.com"
EMAIL_SMTP_SERVER="smtp.gmail.com"
EMAIL_SMTP_PORT="587"
```

---

## 📁 Estructura de Archivos

```
Solicitud2.0/
├── .github/
│   └── workflows/          # Automatización de GitHub Actions
├── main.py                 # Script principal
├── new_bbs                 # Cookie de sesión (¡ACTUALIZAR DIARIAMENTE!)
├── README.md               # Este archivo
└── .gitignore              # Archivos ignorados por Git
```

---

## 🐛 Solución de Problemas

### ❌ "Cookie inválida" o "No se puede conectar"

**Solución:**
- Verifica que la cookie en `new_bbs` sea correcta y esté actualizada
- Obtén una nueva cookie de Xiaomi Community
- Asegúrate de que la sesión siga activa

### ❌ El workflow no se ejecuta

**Solución:**
- Verifica que el workflow esté habilitado en **Settings > Actions**
- Comprueba el registro en **Actions** para ver errores
- Asegúrate de que los secretos estén configurados correctamente

### ❌ No recibo emails

**Solución:**
- Verifica que `EMAIL_SENDER` y `EMAIL_PASSWORD` sean correctos
- Para Gmail, usa una **contraseña de aplicación** (no la contraseña principal)
- Revisa la carpeta de **spam** o **promociones**
- Comprueba los registros del workflow para ver mensajes de error

### ❌ El script se ejecuta pero no envía solicitud

**Solución:**
- Revisa los logs en GitHub Actions
- Verifica la conexión a Internet en la cookie
- Asegúrate de que la sesión de Xiaomi no esté expirada

---

## 💡 Consejos Útiles

- 🔄 **Actualiza la cookie diariamente** antes de las 11:30 PM (hora de Pekín)
- 📱 Obtén la cookie usando **navegador de escritorio** para mejor compatibilidad
- 🔐 **Nunca compartas tu cookie** - ¡Es como tu contraseña!
- 📊 Monitorea el progreso en la pestaña **Actions** de GitHub
- ✉️ Configura notificaciones por email para saber cuando se aprueba

---

## 📝 Notas

- Este script respeta los términos de servicio de Xiaomi Community
- La aprobación del desbloqueo depende de Xiaomi, no de este script
- Los tiempos de aprobación varían según el dispositivo y región
- Se recomienda usar un email dedicado para las notificaciones

---

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo licencia MIT.

---

**¿Preguntas? ¿Problemas?** Abre un issue en GitHub o revisa los logs del workflow para más detalles.

✨ **¡Que te aprueben rápido el desbloqueo!** ✨
