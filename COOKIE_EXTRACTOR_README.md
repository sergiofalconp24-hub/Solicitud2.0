# 🔐 Extractor de Cookie Xiaomi

Script Python para extraer automáticamente tu cookie de Xiaomi Community.

## ✨ Características

- ✓ Inicia sesión automáticamente con email/contraseña
- ✓ Extrae el token/cookie de Xiaomi
- ✓ Verifica que el token sea válido
- ✓ Guarda en `token.txt` en la línea especificada
- ✓ Interfaz interactiva y segura

## 🚀 Uso

```bash
python extract_cookie.py
```

### Pasos:
1. Ejecuta el script
2. Ingresa tu **email** de Xiaomi Community
3. Ingresa tu **contraseña**
4. Especifica en qué **línea** guardar (default: 1)
5. ¡Listo! Tu cookie se guardará en `token.txt`

## 📋 Requisitos

- Python 3.6+
- Librería `requests` (se instala automáticamente con main.py)

## ⚠️ Consideraciones de Seguridad

### ✓ SEGURO:
- Las credenciales NO se almacenan en el script
- Se piden interactivamente (no en plaintext en el código)
- Se borra de la memoria después del login
- La contraseña se hashea antes de enviar

### ⚠️ IMPORTANTE:
- **NUNCA** compartas este script si contiene tus credenciales
- La contraseña se envía a servidores de Xiaomi (usa HTTPS)
- El token se almacena en texto plano en `token.txt`
- Protege `token.txt` como si fuera una contraseña

## 🔄 Automatización

Si quieres que se ejecute automáticamente cada cierto tiempo:

```bash
# En Linux/Mac:
(crontab -l 2>/dev/null; echo "0 22 * * * cd /ruta/al/proyecto && python extract_cookie.py") | crontab -

# En Windows:
# Usa Tareas Programadas
```

## 🔧 Solución de Problemas

### "Error: Timeout en la conexión"
- Verifica tu conexión a internet
- Xiaomi podría tener problemas de servidor
- Intenta de nuevo en unos minutos

### "Token expirado o inválido"
- El token se puede expirar después de cierto tiempo
- Vuelve a ejecutar este script
- Los tokens de Xiaomi expiran típicamente cada 30 días

### "No se encontró el token en la respuesta"
- Tu email/contraseña podrían ser incorrectos
- Xiaomi cambió su API (contacta al autor)
- Podrías tener 2FA activado (deshabilítalo temporalmente)

## 📝 Salida Esperada

```
============================================================
EXTRACTOR DE COOKIE XIAOMI COMMUNITY
============================================================

[?] Ingresa tu email de Xiaomi: usuario@email.com
[?] Ingresa tu contraseña: ••••••••
[*] Iniciando sesión en Xiaomi...
[+] Login exitoso!
[+] Token extraído: abc123def456ghi789...
[*] Verificando token...
[+] Token válido!
[?] ¿En qué línea guardar? (default: 1): 1

[+] ¡ÉXITO!
[+] Tu cookie está guardada en token.txt
[+] Token (primeros 30 caracteres): abc123def456ghi789jkl012mno34...

============================================================
Ejecución completada exitosamente
============================================================
```

## 🛡️ Privacidad

- Este script NO almacena tus credenciales
- Tu email/contraseña solo se envían a **servidores oficiales de Xiaomi**
- No se registra ni se guarda en logs
- Desaparece de la memoria después de ejecutarse

## 📞 Soporte

Si tienes problemas:
1. Verifica que tu email/contraseña sean correctos
2. Asegúrate de tener conexión a internet
3. Comprueba que 2FA no esté activado
4. Verifica que Xiaomi Community siga usando el mismo endpoint

---

**Última actualización:** Mayo 2026
**Versión:** 1.0
