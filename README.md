# Sistema-de-control-de-acceso
Sistema de control de acceso de grupo5
Este es un sistema de control de acceso sencillo para la práctica de GRUPO5. Integra 2 simuladores y un servidor que se conectan e intercambian información a través de azure-iot.
Se divide en 3 partes:
Dos simuladores: uno para la puerta ("door") y otro para el cliente ("client"). Ambos están desplegados localmente. El cliente permite ingresar el nombre y el número de empleado. La puerta recibe información del servidor; cuando recibe una señal para abrir, muestra "OPEN" durante 5 segundos. De lo contrario, el estado permanece como "CLOSE". También muestra "CLOSE" cuando recibe un mensaje de error.

Un servidor ("server"), desplegado en azure-app.
El servidor tiene cuatro funciones: 1. Agregar información de empleados, 2. Mostrar toda la información de los empleados, 3. Escuchar la información del cliente y controlar el abrir y cerrar de la puerta, 4. Volver al menú principal desde el modo de escucha.

Lógica general: Cuando el servidor recibe la información del simulador del cliente, verifica que el nombre y el número de empleado correspondan exactamente con la información almacenada en "employees". Si coinciden, envía una orden de apertura a la puerta. Si la información no coincide, no envía la orden de apertura y la puerta indica un error en la información del empleado.

Antes de usar, por favor ejecute este comando: !pip install azure-iot-device.
