import subprocess
import sys
import os
import platform

# Server lists
ntp_servers = [
    "ntp0.ntp-servers.net", "ntp1.ntp-servers.net", "ntp2.ntp-servers.net",
    "ntp3.ntp-servers.net", "ntp4.ntp-servers.net", "ntp5.ntp-servers.net",
    "ntp6.ntp-servers.net"
]

MI_SERVERS = ['161.117.96.161', '20.157.18.26']

# Installation of dependencies
def install_package(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

required_packages = ["requests", "ntplib", "pytz", "urllib3", "icmplib", "colorama", "linecache"]
for package in required_packages:
    try:
        __import__(package)
    except ImportError:
        print(f"Instalando paquete {package}...")
        install_package(package)

os.system('cls' if os.name == 'nt' else 'clear')

import hashlib
import linecache
import random
import time
from datetime import datetime, timezone, timedelta
import ntplib
import pytz
import urllib3
import json
import statistics
import smtplib
from email.message import EmailMessage
from icmplib import ping
from colorama import init, Fore, Style

# Color settings
init(autoreset=True)
col_g = Fore.GREEN #green
col_gb = Style.BRIGHT + Fore.GREEN #bright green
col_b = Fore.BLUE #blue
col_bb = Style.BRIGHT + Fore.BLUE #bright blue
col_y = Fore.YELLOW #yellow
col_yb = Style.BRIGHT + Fore.YELLOW #bright yellow
col_r = Fore.RED #red
col_rb = Style.BRIGHT + Fore.RED #bright red

# Version and token number
#token_number = int(input(col_g + f"[Número de línea del token]: " + Fore.RESET))
os.system('cls' if os.name == 'nt' else 'clear')
token_number = 1
scriptversion = "ARU_FHL_v070425"

# Variables globales
print(col_yb + f"{scriptversion}_токен_#{token_number}:")
print (col_y + f"Verificando estado de la cuenta" + Fore.RESET)

# Validar existencia de archivos
try:
    token = linecache.getline("new_bbs", token_number).strip()
    if not token:
        print(col_r + f"[ERROR] Token vacío en línea {token_number}" + Fore.RESET)
        exit(1)
    cookie_value = token
    
    timeshift_line = linecache.getline("timeshift.txt", token_number).strip()
    if not timeshift_line:
        print(col_r + f"[ERROR] Timeshift vacío en línea {token_number}" + Fore.RESET)
        exit(1)
    feedtime = float(timeshift_line)
    feed_time_shift = feedtime
    feed_time_shift_1 = feed_time_shift / 1000
except FileNotFoundError as e:
    print(col_r + f"[ERROR] Archivo no encontrado: {e}" + Fore.RESET)
    exit(1)
except ValueError as e:
    print(col_r + f"[ERROR] Valor inválido en timeshift.txt: {e}" + Fore.RESET)
    exit(1)

# Generates a unique device identifier
def generate_device_id():
    random_data = f"{random.random()}-{time.time()}"
    device_id = hashlib.sha1(random_data.encode('utf-8')).hexdigest().upper()
    return device_id

# Get the current Beijing time from NTP
def get_initial_beijing_time():
    client = ntplib.NTPClient()
    beijing_tz = pytz.timezone("Asia/Shanghai")
    for server in ntp_servers:
        try:
            print(col_y + f"\nObteniendo hora actual en Pekín" + Fore.RESET)
            response = client.request(server, version=3)
            ntp_time = datetime.fromtimestamp(response.tx_time, timezone.utc)
            beijing_time = ntp_time.astimezone(beijing_tz)
            print(col_g + f"[Hora en Pekín]: " + Fore.RESET +  f"{beijing_time.strftime('%Y-%m-%d %H:%M:%S.%f')}")
            return beijing_time
        except Exception as e:
            print(f"Error al conectar con {server}: {e}")
    print(f"No se pudo conectar a ningún servidor NTP.")
    return None

# Synchronize Beijing time
def get_synchronized_beijing_time(start_beijing_time, start_timestamp):
    elapsed = time.time() - start_timestamp
    current_time = start_beijing_time + timedelta(seconds=elapsed)
    return current_time

# Wait until the target time taking into account the ping
def wait_until_target_time(start_beijing_time, start_timestamp):
    next_day = start_beijing_time + timedelta(days=1)
    print(col_y + f"\nSolicitud para desbloqueo del bootloader" + Fore.RESET)
    print (col_g + f"[Desfase establecido]: " + Fore.RESET + f"{feed_time_shift:.2f} мс.")
    target_time = next_day.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(seconds=feed_time_shift_1)
    print(col_g + f"[Esperando hasta]: " + Fore.RESET + f"{target_time.strftime('%Y-%m-%d %H:%M:%S.%f')}")
    print(f"No cierre esta ventana...")
    
    while True:
        current_time = get_synchronized_beijing_time(start_beijing_time, start_timestamp)
        time_diff = target_time - current_time
        
        if time_diff.total_seconds() > 1:
            time.sleep(min(1.0, time_diff.total_seconds() - 1))
        elif current_time >= target_time:
            print(f"Время достигнуто: {current_time.strftime('%Y-%m-%d %H:%M:%S.%f')}. Начинаем отправку запросов...")
            break
        else:
            time.sleep(0.0001)

# Check if account unlocking is possible via API
def check_unlock_status(session, cookie_value, device_id, is_automated=False):
    try:
        url = "https://sgp-api.buy.mi.com/bbs/api/global/user/bl-switch/state"
        headers = {
            "Cookie": f"new_bbs_serviceToken={cookie_value};versionCode=500411;versionName=5.4.11;deviceId={device_id};"
        }
        
        response = session.make_request('GET', url, headers=headers)
        if response is None:
            print(f"[Error] No se pudo obtener el estado de desbloqueo.")
            return False

        response_data = json.loads(response.data.decode('utf-8'))
        response.release_conn()

        if response_data.get("code") == 100004:
            print(col_r + f"[Error] La cookie ha expirado, necesita actualizarse." + Fore.RESET)
            return False

        data = response_data.get("data", {})
        is_pass = data.get("is_pass")
        button_state = data.get("button_state")
        deadline_format = data.get("deadline_format", "")

        if is_pass == 4:
            if button_state == 1:
                    print(col_g + f"[Estado de la cuenta]: " + Fore.RESET + f"es posible enviar la solicitud..")
                    return True

            elif button_state == 2:
                print(col_g + f"[Estado de la cuenta]: " + Fore.RESET + f"bloqueo para enviar solicitudes hasta {deadline_format} (Месяц/День).")
                if is_automated:
                    print(col_y + f"[Automático] Continuando..." + Fore.RESET)
                    return True
                status_2 = (input(f"Продолжить (" + col_b + f"Yes/No" +Fore.RESET + f")?: ") )
                if (status_2 == 'y' or status_2 == 'Y' or status_2 == 'yes' or status_2 == 'Yes' or status_2 == 'YES'):
                    return True
                else:
                    return False
            elif button_state == 3:
                print(col_g + f"[Estado de la cuenta]: " + Fore.RESET + f"la cuenta fue creada hace menos de 30 días..")
                if is_automated:
                    print(col_y + f"[Automático] Continuando..." + Fore.RESET)
                    return True
                status_3 = (input(f"Продолжить (" + col_b + f"Yes/No" +Fore.RESET + f")?: ") )
                if (status_3 == 'y' or status_3 == 'Y' or status_3 == 'yes' or status_3 == 'Yes' or status_3 == 'YES'):
                    return True
                else:
                    return False
        elif is_pass == 1:
            print(col_g + f"[Estado de la cuenta]: " + Fore.RESET + f"la solicitud fue aprobada, el desbloqueo es posible hasta {deadline_format}.")
            return False
        else:
            print(col_g + f"[Estado de la cuenta]: " + Fore.RESET + f"estado desconocido.")
            return False
    except Exception as e:
        print(f"[Error проверки статуса] {e}")
        return False

DEFAULT_EMAIL_RECIPIENT = "sergiofalconp24@gmail.com"

# Función para cargar configuración de correo desde variables de entorno
def load_email_settings():
    sender = os.getenv('EMAIL_SENDER')
    password = os.getenv('EMAIL_PASSWORD')
    recipient = os.getenv('EMAIL_RECIPIENT', DEFAULT_EMAIL_RECIPIENT)
    smtp_server = os.getenv('EMAIL_SMTP_SERVER', 'smtp.gmail.com')
    smtp_port = int(os.getenv('EMAIL_SMTP_PORT', '587'))

    if not sender or not password:
        return None

    return {
        'sender': sender,
        'password': password,
        'recipient': recipient,
        'smtp_server': smtp_server,
        'smtp_port': smtp_port,
    }

# Función para enviar correo electrónico con el resultado de la solicitud
def send_email_report(subject, body, email_settings):
    try:
        msg = EmailMessage()
        msg['From'] = email_settings['sender']
        msg['To'] = email_settings['recipient']
        msg['Subject'] = subject
        msg.set_content(body)

        with smtplib.SMTP(email_settings['smtp_server'], email_settings['smtp_port']) as server:
            server.starttls()
            server.login(email_settings['sender'], email_settings['password'])
            server.send_message(msg)

        print(col_g + f"[Correo enviado]: " + Fore.RESET + f"{email_settings['recipient']}")
        return True
    except Exception as e:
        print(col_r + f"[Error al enviar correo]: {e}" + Fore.RESET)
        return False

# Función para registrar resultados en archivo
def save_response_log(start_time, end_time, status, response_data, send_email=False):
    try:
        with open('respuesta.txt', 'w', encoding='utf-8') as f:
            f.write(f"=== REPORTE DE SOLICITUD DE DESBLOQUEO ===\n\n")
            f.write(f"[Hora de Inicio]: {start_time.strftime('%Y-%m-%d %H:%M:%S.%f')} (UTC+8)\n")
            f.write(f"[Hora de Finalización]: {end_time.strftime('%Y-%m-%d %H:%M:%S.%f')} (UTC+8)\n")
            f.write(f"[Estado]: {status}\n")
            f.write(f"[Respuesta]: {response_data}\n")
        print(col_g + f"[Registro guardado]: " + Fore.RESET + f"respuesta.txt")

        if send_email:
            email_settings = load_email_settings()
            if email_settings is None:
                print(col_y + "[Aviso]: Las variables de entorno EMAIL_SENDER y EMAIL_PASSWORD no están configuradas. No se envió correo." + Fore.RESET)
            else:
                subject = f"Solicitud de desbloqueo Xiaomi - {status}"
                body = (
                    f"Solicitud de desbloqueo Xiaomi\n\n"
                    f"Estado: {status}\n"
                    f"Inicio: {start_time.strftime('%Y-%m-%d %H:%M:%S.%f')} (UTC+8)\n"
                    f"Fin: {end_time.strftime('%Y-%m-%d %H:%M:%S.%f')} (UTC+8)\n\n"
                    f"Respuesta:\n{response_data}\n"
                )
                send_email_report(subject, body, email_settings)
    except Exception as e:
        print(f"[Error al guardar]: {e}")

# Container for working with HTTP requests
class HTTP11Session:
    def __init__(self):
        self.http = urllib3.PoolManager(
            maxsize=10,
            retries=True,
            timeout=urllib3.Timeout(connect=2.0, read=15.0),
            headers={}
        )

    def make_request(self, method, url, headers=None, body=None):
        try:
            request_headers = {}
            if headers:
                request_headers.update(headers)
                request_headers['Content-Type'] = 'application/json; charset=utf-8'
            
            if method == 'POST':
                if body is None:
                    body = '{"is_retry":true}'.encode('utf-8')
                request_headers['Content-Length'] = str(len(body))
                request_headers['Accept-Encoding'] = 'gzip, deflate, br'
                request_headers['User-Agent'] = 'okhttp/4.12.0'
                request_headers['Connection'] = 'keep-alive'
            
            response = self.http.request(
                method,
                url,
                headers=request_headers,
                body=body,
                preload_content=False
            )
            
            return response
        except Exception as e:
            print(f"[Error сети] {e}")
            return None
 
def main():
        
    device_id = generate_device_id()
    session = HTTP11Session()
    execution_start_time = datetime.now(pytz.timezone("Asia/Shanghai"))  # Hora de inicio
    is_automated = not sys.stdin.isatty()  # Detectar si es modo automático

    try:
        if not check_unlock_status(session, cookie_value, device_id, is_automated):
            execution_end_time = datetime.now(pytz.timezone("Asia/Shanghai"))
            save_response_log(execution_start_time, execution_end_time, "FALLO - VERIFICACIÓN INICIAL", "No se pudo verificar el estado de la cuenta", send_email=True)
            exit(1)
            
        start_beijing_time = get_initial_beijing_time()
        if start_beijing_time is None:
            execution_end_time = datetime.now(pytz.timezone("Asia/Shanghai"))
            save_response_log(execution_start_time, execution_end_time, "ERROR - HORA NTP", "No se pudo establecer la hora inicial desde NTP", send_email=True)
            exit(1)

        start_timestamp = time.time()
        
        wait_until_target_time(start_beijing_time, start_timestamp)

        url = "https://sgp-api.buy.mi.com/bbs/api/global/apply/bl-auth"
        headers = {
            "Cookie": f"new_bbs_serviceToken={cookie_value};versionCode=500411;versionName=5.4.11;deviceId={device_id};"
        }

        max_retries = 5  # Máximo de intentos para evitar loop infinito
        retry_count = 0
        success = False

        while retry_count < max_retries and not success:
            try:
                request_time = get_synchronized_beijing_time(start_beijing_time, start_timestamp)
                print(col_g + f"[Solicitud]: " + Fore.RESET + f"Enviando solicitud a las {request_time.strftime('%Y-%m-%d %H:%M:%S.%f')} (UTC+8)")
                
                response = session.make_request('POST', url, headers=headers)
                if response is None:
                    retry_count += 1
                    time.sleep(2)
                    continue

                response_time = get_synchronized_beijing_time(start_beijing_time, start_timestamp)
                print(col_g + f"[Respuesta]: " + Fore.RESET + f"Respuesta получен в {response_time.strftime('%Y-%m-%d %H:%M:%S.%f')} (UTC+8)")

                try:
                    response_data = response.data
                    response.release_conn()
                    json_response = json.loads(response_data.decode('utf-8'))
                    code = json_response.get("code")
                    data = json_response.get("data", {})

                    if code == 0:
                        apply_result = data.get("apply_result")
                        execution_end_time = datetime.now(pytz.timezone("Asia/Shanghai"))
                        if apply_result == 1:
                            print(col_g + f"[Статус]: " + Fore.RESET + f"La solicitud fue aprobada, verificando estado...")
                            save_response_log(execution_start_time, execution_end_time, "APROBADA", json.dumps(json_response, indent=2), send_email=True)
                            success = True
                            break
                        elif apply_result == 3:
                            deadline_format = data.get("deadline_format", "Не указано")
                            print(col_g + f"[Статус]: " + Fore.RESET + f"La solicitud no fue enviada, se alcanzó el límite. Intente de nuevo el {deadline_format} (Месяц/День).")
                            save_response_log(execution_start_time, execution_end_time, "RECHAZADA - LÍMITE ALCANZADO", json.dumps(json_response, indent=2), send_email=True)
                            success = True
                            break
                        elif apply_result == 4:
                            deadline_format = data.get("deadline_format", "Не указано")
                            print(col_g + f"[Статус]: " + Fore.RESET + f"La solicitud no fue enviada, se impuso un bloqueo hasta {deadline_format} (Месяц/День).")
                            save_response_log(execution_start_time, execution_end_time, "BLOQUEADA", json.dumps(json_response, indent=2), send_email=True)
                            success = True
                            break
                    elif code == 100001:
                        execution_end_time = datetime.now(pytz.timezone("Asia/Shanghai"))
                        print(col_g + f"[Статус]: " + Fore.RESET + f"La solicitud fue rechazada, error en la petición..")
                        print(col_g + f"[ПОЛНЫЙ ОТВЕТ]: " + Fore.RESET + f"{json_response}")
                        save_response_log(execution_start_time, execution_end_time, "RECHAZADA - ERROR EN PETICIÓN", json.dumps(json_response, indent=2), send_email=True)
                        success = True
                        break
                    elif code == 100003:
                        execution_end_time = datetime.now(pytz.timezone("Asia/Shanghai"))
                        print(col_g + f"[Статус]: " + Fore.RESET + f"La solicitud puede haber sido aprobada, verificando estado...")
                        print(col_g + f"[Полный ответ]: " + Fore.RESET + f"{json_response}")
                        save_response_log(execution_start_time, execution_end_time, "POSIBLEMENTE APROBADA", json.dumps(json_response, indent=2), send_email=True)
                        success = True
                        break
                    elif code is not None:
                        execution_end_time = datetime.now(pytz.timezone("Asia/Shanghai"))
                        print(col_g + f"[Статус]: " + Fore.RESET + f"Estado desconocido de la solicitud: {code}")
                        print(col_g + f"[Полный ответ]: " + Fore.RESET + f"{json_response}")
                        save_response_log(execution_start_time, execution_end_time, f"ESTADO DESCONOCIDO (Código: {code})", json.dumps(json_response, indent=2), send_email=True)
                        success = True
                        break
                    else:
                        execution_end_time = datetime.now(pytz.timezone("Asia/Shanghai"))
                        print(col_g + f"[Error]: " + Fore.RESET + f"Respuesta не содержит необходимого кода.")
                        print(col_g + f"[Полный ответ]: " + Fore.RESET + f"{json_response}")
                        save_response_log(execution_start_time, execution_end_time, "ERROR - SIN CÓDIGO EN RESPUESTA", json.dumps(json_response, indent=2))
                        retry_count += 1
                        if retry_count < max_retries:
                            time.sleep(2)

                except json.JSONDecodeError:
                    execution_end_time = datetime.now(pytz.timezone("Asia/Shanghai"))
                    print(col_g + f"[Error]: " + Fore.RESET + f"No se pudo decodificar el JSON de la respuesta..")
                    print(col_g + f"[Respuesta сервера]: " + Fore.RESET + f"{response_data}")
                    save_response_log(execution_start_time, execution_end_time, "ERROR - JSON INVÁLIDO", str(response_data))
                    retry_count += 1
                    if retry_count < max_retries:
                        time.sleep(2)
                except Exception as e:
                    print(col_g + f"[Error обработки ответа]: " + Fore.RESET + f"{e}")
                    retry_count += 1
                    if retry_count < max_retries:
                        time.sleep(2)

            except Exception as e:
                execution_end_time = datetime.now(pytz.timezone("Asia/Shanghai"))
                print(col_g + f"[Error запроса]: " + Fore.RESET + f"{e}")
                save_response_log(execution_start_time, execution_end_time, "ERROR EN LA SOLICITUD", str(e), send_email=True)

        if not success:
            execution_end_time = datetime.now(pytz.timezone("Asia/Shanghai"))
            save_response_log(execution_start_time, execution_end_time, "ERROR - MÁXIMO DE REINTENTOS ALCANZADO", f"No se pudo completar después de {max_retries} intentos", send_email=True)
            exit(1)

    except Exception as e:
        execution_end_time = datetime.now(pytz.timezone("Asia/Shanghai"))
        print(col_r + f"[Error global]: {e}" + Fore.RESET)
        save_response_log(execution_start_time, execution_end_time, "ERROR GLOBAL", str(e), send_email=True)
        exit(1)

if __name__ == "__main__":
    main()