import subprocess

def start_gazebo(world_file=None):
    """
    Inicia Gazebo con un archivo de mundo específico si se proporciona.
    
    :param world_file: Ruta al archivo de mundo (.world) que quieres cargar en Gazebo.
                       Si no se proporciona, Gazebo se iniciará con el mundo por defecto.
    """
    try:
        # Comando base para iniciar Gazebo
        cmd = ["gazebo"]
        
        # Si se proporciona un archivo de mundo, añadirlo al comando
        if world_file:
            cmd.append(world_file)
        
        # Ejecutar el comando para iniciar Gazebo
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        print("Gazebo iniciado con éxito.")
        return process
    except Exception as e:
        print(f"Error al iniciar Gazebo: {e}")

# Ejemplo de uso
if __name__ == "__main__":
    # Ruta opcional a un archivo de mundo de Gazebo
    world_file_path = "/path/to/your/world_file.world"
    
    # Iniciar Gazebo
    process = start_gazebo(world_file_path)
    
    # Si quieres esperar a que el proceso termine (bloqueante)
    # process.wait()
    
    # Si solo quieres dejarlo correr en el fondo, puedes omitir la línea anterior.
