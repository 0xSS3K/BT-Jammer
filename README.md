## Bluetooth DoS Script v2.0
Un script de Python para realizar ataques de Denegación de Servicio (DoS) a dispositivos Bluetooth Clásico mediante una inundación de pings L2CAP. Este script es una versión mejorada, más robusta y fácil de usar.

---

## ⚠️ Descargo de Responsabilidad

Este script ha sido creado con fines estrictamente educativos y de investigación en seguridad. El autor no se hace responsable del mal uso que se le pueda dar a esta herramienta. Utilizar este script contra redes o dispositivos sin consentimiento explícito previo es ilegal. Eres el único responsable de tus acciones.

---

## 🚀 Características

* Detección automática de adaptadores.
* Escaneo de dispositivos.
* Ataque multihilo.
* Interfaz de usuario mejorada.
* Robusto y seguro.
* Manejo de errores.

---

## 🔧 Requisitos Previos

* Un sistema operativo Linux (probado en Debian, Ubuntu, Kali Linux).
* Python 3.x.
* El paquete bluez-utils, que contiene las herramientas l2ping y hcitool.

---

## ⚙️ Instalación

1. Clona el repositorio
```Bash
git clone https://github.com/0xSS3K/BT-Jammer.git
cd BT-Jammer
```

2. Instala las dependencias
En sistemas basados en Debian/Ubuntu:
```Bash
sudo apt-get update
sudo apt-get install python3 bluez-utils
```

---

## 🤔 ¿Cómo Funciona?

El script automatiza un ataque de inundación de pings (ping flood) sobre el protocolo L2CAP de Bluetooth Clásico.

* Usa hcitool para escanear y descubrir dispositivos cercanos.
* Una vez seleccionado un objetivo, utiliza l2ping para enviar un flujo masivo y continuo de paquetes "echo request".
* El uso de threading permite enviar múltiples flujos de pings en paralelo, aumentando la carga sobre el dispositivo objetivo.
* El objetivo es saturar la pila de protocolos Bluetooth del dispositivo receptor, provocando que se ralentice, pierda conexiones o deje de responder por completo.

---

Este proyecto se distribuye bajo la Licencia MIT. Consulta el archivo ```LICENSE``` para más detalles.
