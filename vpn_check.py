#!/usr/bin/python3

import json
import subprocess
import time

# Глобальная переменная для хранения имени последнего запущенного приложения
last_app = None
WIREGUARD = "WireGuard"
VISCOSITY = "Viscosity"


def is_process_running(process_name):
    """Проверка, запущен ли процесс"""
    try:
        output = subprocess.check_output(['pgrep', process_name], text=True)
        if output:
            return True
    except subprocess.CalledProcessError:
        return False
    return False


def kill_process(process_name):
    """Завершение процесса по его имени с использованием sudo без запроса пароля"""
    try:
        subprocess.call(['sudo', 'pkill', '-9', '-f', process_name])
    except subprocess.SubprocessError as e:
        print(f"Ошибка при попытке завершить процесс {process_name}: {e}")


def launch_application(app_name):
    """Запуск приложения"""
    subprocess.call(['open', '-a', app_name])


def get_external_ip_country():
    """Получение страны внешнего IP-адреса"""
    try:
        output = subprocess.check_output(['curl', '-s', 'https://api.myip.com/'], text=True)
        ip_info = json.loads(output)
        return ip_info.get('cc')
    except Exception as e:
        print(f"Ошибка при получении информации об IP: {e}")
        return None


def check_and_manage_vpn():
    """Проверка и управление VPN-клиентами с учётом страны и переключением между приложениями"""
    global last_app
    country = get_external_ip_country()

    if country != 'RU':
        if is_process_running(VISCOSITY):
            kill_process(VISCOSITY)
            print(f"{VISCOSITY} был остановлен, так как внешний IP не из РФ.")
    else:
        if last_app == VISCOSITY and is_process_running(WIREGUARD):
            kill_process(VISCOSITY)
            last_app = WIREGUARD
            print(f"{VISCOSITY} был остановлен, переключаемся на {WIREGUARD}.")
        elif last_app == WIREGUARD and is_process_running(VISCOSITY):
            kill_process(WIREGUARD)
            last_app = VISCOSITY
            print(f"{WIREGUARD} был остановлен, переключаемся на {VISCOSITY}.")
        elif last_app is None or not is_process_running(last_app):
            # Если последнее приложение не определено или не запущено, запускаем WireGuard как приложение по умолчанию
            last_app = WIREGUARD
            launch_application(WIREGUARD)
            print(f"Устанавливаем {WIREGUARD} как приложение по умолчанию.")


if __name__ == "__main__":
    while True:
        check_and_manage_vpn()
        # Задержка перед следующей проверкой, например, 1 секунда
        time.sleep(1)
