import subprocess

def open_file_explorer() -> str:
    try:
        # Ejecutar el comando zenity para abrir el explorador de archivos
        result = subprocess.run(['zenity','--file-selection'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Verificar si el comando se ejecutó correctamente
        if result.returncode == 0:
            # Obtener la ruta seleccionada del stdout
            file_path = result.stdout.decode('utf-8').strip()
            return file_path
        else:
            # Si se presiona "Cancelar" o hay un error
            print(f"Error: {result.stderr.decode('utf-8').strip()}")
            return ""
    except Exception as e:
        print(f"Exception: {e}")
        return ""

# Ejemplo de uso
selected_file_path = open_file_explorer()
print(f"Ruta seleccionada: {selected_file_path}")
