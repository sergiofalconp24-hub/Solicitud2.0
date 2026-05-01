#!/usr/bin/env python3
"""
Script para extraer la cookie de Xiaomi Community
Requiere: email, contraseña
Genera: token.txt con la cookie
"""

import requests
import json
import hashlib
import time
import urllib3
from datetime import datetime

# Desactivar advertencias de SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class XiaomiCookieExtractor:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'okhttp/4.12.0',
            'Content-Type': 'application/x-www-form-urlencoded'
        })
        self.base_url = "https://sgp-api.buy.mi.com/bbs/api/global"
        self.token = None
        
    def login(self, email, password):
        """
        Inicia sesión en Xiaomi y extrae el token
        """
        try:
            print("[*] Iniciando sesión en Xiaomi...")
            
            # Endpoint de login
            login_url = "https://sgp-api.buy.mi.com/bbs/api/global/user/login"
            
            login_data = {
                "email": email,
                "password": hashlib.md5(password.encode()).hexdigest(),
                "lng": "es",
                "countryCode": "ES"
            }
            
            response = self.session.post(
                login_url,
                data=login_data,
                verify=False,
                timeout=10
            )
            
            if response.status_code != 200:
                print(f"[!] Error en la solicitud: {response.status_code}")
                return False
                
            response_data = response.json()
            
            if response_data.get("code") != 0:
                error_msg = response_data.get("message", "Error desconocido")
                print(f"[!] Error de login: {error_msg}")
                print(f"[!] Código de error: {response_data.get('code')}")
                return False
            
            # Extraer token de la respuesta
            data = response_data.get("data", {})
            self.token = data.get("new_bbs_serviceToken") or data.get("token")
            
            if not self.token:
                print("[!] No se encontró el token en la respuesta")
                print(f"[!] Respuesta completa: {json.dumps(response_data, indent=2)}")
                return False
            
            print(f"[+] Login exitoso!")
            print(f"[+] Token extraído: {self.token[:20]}...")
            return True
            
        except requests.exceptions.Timeout:
            print("[!] Error: Timeout en la conexión")
            return False
        except requests.exceptions.ConnectionError:
            print("[!] Error: No se pudo conectar al servidor de Xiaomi")
            return False
        except json.JSONDecodeError:
            print("[!] Error: Respuesta inválida del servidor")
            return False
        except Exception as e:
            print(f"[!] Error inesperado: {e}")
            return False
    
    def verify_token(self):
        """
        Verifica que el token sea válido
        """
        try:
            print("[*] Verificando token...")
            
            verify_url = f"{self.base_url}/user/bl-switch/state"
            headers = {
                "Cookie": f"new_bbs_serviceToken={self.token};versionCode=500411;versionName=5.4.11;"
            }
            
            response = self.session.get(
                verify_url,
                headers=headers,
                verify=False,
                timeout=10
            )
            
            response_data = response.json()
            
            if response_data.get("code") == 0:
                print("[+] Token válido!")
                return True
            elif response_data.get("code") == 100004:
                print("[!] Token expirado o inválido")
                return False
            else:
                print(f"[!] Error en verificación: {response_data.get('message')}")
                return False
                
        except Exception as e:
            print(f"[!] Error en verificación: {e}")
            return False
    
    def save_token(self, filename="token.txt", line_number=1):
        """
        Guarda el token en el archivo token.txt
        """
        try:
            print(f"[*] Guardando token en {filename}...")
            
            # Leer líneas existentes
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
            except FileNotFoundError:
                lines = []
            
            # Asegurar que hay suficientes líneas
            while len(lines) < line_number:
                lines.append("\n")
            
            # Reemplazar o agregar la línea
            lines[line_number - 1] = self.token + "\n"
            
            # Guardar
            with open(filename, 'w', encoding='utf-8') as f:
                f.writelines(lines)
            
            print(f"[+] Token guardado en línea {line_number} de {filename}")
            return True
            
        except Exception as e:
            print(f"[!] Error al guardar token: {e}")
            return False

def main():
    print("=" * 60)
    print("EXTRACTOR DE COOKIE XIAOMI COMMUNITY")
    print("=" * 60)
    print()
    
    # Solicitar credenciales
    email = input("[?] Ingresa tu email de Xiaomi: ").strip()
    password = input("[?] Ingresa tu contraseña: ").strip()
    
    if not email or not password:
        print("[!] Email y contraseña son requeridos")
        return False
    
    # Crear extractor
    extractor = XiaomiCookieExtractor()
    
    # Intentar login
    if not extractor.login(email, password):
        print("[!] Fallo en el login")
        return False
    
    # Verificar token
    if not extractor.verify_token():
        print("[!] Token no válido")
        return False
    
    # Preguntar línea de guardado
    line_input = input("[?] ¿En qué línea guardar? (default: 1): ").strip()
    try:
        line_number = int(line_input) if line_input else 1
    except ValueError:
        line_number = 1
    
    # Guardar token
    if extractor.save_token(line_number=line_number):
        print()
        print("[+] ¡ÉXITO!")
        print(f"[+] Tu cookie está guardada en token.txt")
        print(f"[+] Token (primeros 30 caracteres): {extractor.token[:30]}...")
        return True
    else:
        print("[!] Error al guardar token")
        return False

if __name__ == "__main__":
    try:
        success = main()
        print()
        print("=" * 60)
        if success:
            print("Ejecución completada exitosamente")
        else:
            print("Ejecución finalizada con errores")
        print("=" * 60)
    except KeyboardInterrupt:
        print("\n[!] Operación cancelada por el usuario")
    except Exception as e:
        print(f"\n[!] Error global: {e}")
