import flet
import subprocess
import os

def ejecutar_comando_en_ruta(e):
    # Obtiene la ruta del usuario desde un control de entrada, por ejemplo un TextField
    ruta_usuario = ruta_input.value

    # Determina el comando basado en el sistema operativo
    comando = "ls" if os.name == "posix" else "dir"

    # Construye el comando completo con la ruta
    comando_completo = f"cd {ruta_usuario} && {comando}"

    try:
        # Ejecuta el comando
        resultado = subprocess.run(comando_completo, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Muestra el resultado en la aplicación
        salida.value = resultado.stdout
    except subprocess.CalledProcessError as e:
        # Maneja errores en la ejecución, mostrando el error en la aplicación
        salida.value = f"Error al ejecutar el comando: {e.stderr}"

# Crea la aplicación y los controles
app = flet.app()
ruta_input = flet.TextField(label="Ingresa la ruta", width=300)
boton_ejecutar = flet.Button(text="Ejecutar Comando", on_click=ejecutar_comando_en_ruta)
salida = flet.TextField(label="Salida del comando", multiline=True, enabled=False, width=300, height=200)

# Añade los controles a la aplicación
app.add(ruta_input, boton_ejecutar, salida)

# Ejecuta la aplicación
app.run()
