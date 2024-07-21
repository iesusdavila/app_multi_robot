import yaml
import os
import subprocess
import threading
from ament_index_python import get_package_share_path
from user_controls.modelo import Modelo
from user_controls.robot import Robot
from user_controls.world import World

home_dir = os.path.expanduser('~')
robots_path = os.path.join(home_dir,'robotmap-data', "data",'robots_register.yaml')
models_path = os.path.join(home_dir,'robotmap-data', "data",'models_register.yaml')
worlds_path = os.path.join(home_dir,'robotmap-data', "data",'worlds_register.yaml')
gazebo_dir = os.path.join(home_dir,'robotmap-data','gazebo')
rutina_dir = os.path.join(home_dir,'robotmap-data','rutinas')

def configure_package():
    try:
        package_share_path = get_package_share_path('multi_robot_bringup')
        config_path = package_share_path / 'config'
        return str(config_path)
    except ValueError as e:
        print(f"Error al obtener la ruta del paquete: {e}")
        return None

def configure_rutina_path():
    try:
        package_share_path = get_package_share_path('multi_robot_master_slave')
        config_path = package_share_path / 'config'
        return str(config_path)
    except ValueError as e:
        print(f"Error al obtener la ruta del paquete: {e}")
        return None

def obtain_model_list() -> list:
    model_list = list()
    path = models_path
    # Verificar si el archivo existe
    if not os.path.exists(path):
        # Crear el archivo vacío
        with open(path, 'w') as file:
            data = {'models': list()}
            yaml.dump(data, file)
            return model_list
    with open(path, 'r') as file:
        try:
            data = yaml.safe_load(file)
            if data is None or "models" not in data.keys():
                return []
            else:
                if data["models"]:
                    for modelo in data["models"]:
                        model_list.append(Modelo(modelo["name"], modelo["rutaURDF"], modelo["rutaSDF"], modelo['nav_path']))
                    return model_list
                else:
                    return model_list
        except yaml.YAMLError as e:
            print(f"Error en la lectura: {e}")
            return []
        
def model_to_yaml(modelo: Modelo) -> dict:
    return {
        'name': modelo.nombre,
        'rutaURDF': modelo.rutaURDF,
        'rutaSDF': modelo.rutaSDF,
        'nav_path': modelo.nav_path
    }

def add_model(modelo: Modelo):
    path = models_path
    modelos_old = list()
    with open(path, 'r') as file:
        try:
            data = yaml.safe_load(file)
            modelos_old = data['models']
        except yaml.YAMLError as e:
            print(f"Error en la actualizacion: {e}")
    modelos_old.append(model_to_yaml(modelo))
    with open(path, 'w') as file:
            datos = {'models': modelos_old}
            yaml.dump(datos, file)

def obtain_robot_list() -> list:
    robot_list = list()
    path = robots_path
    # Verificar si el archivo existe
    if not os.path.exists(path):
        # Crear el archivo vacío
        with open(path, 'w') as file:
            data = {'robots': list()}
            yaml.dump(data, file)
            return robot_list
    with open(path, 'r') as file:
        try:
            data = yaml.safe_load(file)
            if data is None or "robots" not in data.keys():
                return []
            else:
                if data["robots"]:
                    for robot in data["robots"]:
                        modelo_robot = Modelo(robot["model_name"], robot["model_urdf_path"], robot["model_sdf_path"], robot['model_nav_path'])
                        robot_list.append(Robot(robot["name"], modelo_robot, robot["control_type"], robot["has_camera"]))
                    return robot_list
                else:
                    return robot_list
        except yaml.YAMLError as e:
            print(f"Error en la lectura: {e}")
            return []

def robot_to_yaml(robot: Robot) -> dict:
    return {
        'name': robot.name,
        'control_type': robot.control_type,
        'has_camera': robot.has_camera,
        'model_name': robot.modelo.nombre,
        'model_urdf_path': robot.modelo.rutaURDF,
        'model_sdf_path': robot.modelo.rutaSDF,
        'model_nav_path': robot.modelo.nav_path
    }

def add_robot(robot: Robot):
    path = robots_path
    robots_old = list()
    with open(path, 'r') as file:
        try:
            data = yaml.safe_load(file)
            robots_old = data['robots']
        except yaml.YAMLError as e:
            print(f"Error en la actualizacion: {e}")
    robots_old.append(robot_to_yaml(robot))
    with open(path, 'w') as file:
            datos = {'robots': robots_old}
            yaml.dump(datos, file)

def obtain_world_list() -> list:
    world_list = list()
    path = worlds_path
    if not os.path.exists(path):
        with open(path, 'w') as file:
            data = {'worlds': world_list}
            yaml.dump(data, file)
            return world_list
    with open(path, 'r') as file:
        try:
            data = yaml.safe_load(file)
            if data is None or "worlds" not in data.keys():
                return []
            else:
                if data['worlds']:
                    for world in data['worlds']:
                        world_item = World(world['name'], world['world_path'], world['map_path'])
                        world_list.append(world_item)
                    return world_list
                else:
                    return world_list
        except yaml.YAMLError as e:
            print(f"Error en la lectura: {e}")
            return []

def add_world(world: World):
    path = worlds_path
    worlds_old = list()
    with open(path, 'r') as file:
        try:
            data = yaml.safe_load(file)
            worlds_old = data['worlds']
        except yaml.YAMLError as e:
            print(f"Error en la actualizacion: {e}")
    worlds_old.append(world.to_yaml())
    with open(path, 'w') as file:
            datos = {'worlds': worlds_old}
            yaml.dump(datos, file)

def list_files_in_directory(directory_path: str) -> list:
    """
    List all .yaml or .yml files in the given directory.

    :param directory_path: Path to the directory.
    :return: List of .yaml or .yml file names in the directory.
    """
    try:
        # Verificar si el path proporcionado es un directorio
        response = list()
        if not os.path.isdir(directory_path):
            raise NotADirectoryError(f"El path proporcionado no es un directorio: {directory_path}")
        
        # Obtener la lista de archivos .yaml en el directorio
        yaml_files = [
            f for f in os.listdir(directory_path)
            if os.path.isfile(os.path.join(directory_path, f)) and (f.endswith('.yaml'))
        ]
        for yaml in yaml_files:
            response.append(yaml.split(".")[0])
        return response
    except Exception as e:
        print(f"Error al listar archivos en el directorio: {e}")
        return []

def launch_simulation(config_path: str, stop_event: threading.Event):
    """
    Launch a ROS2 simulation with the given configuration file.

    :param config_path: Path to the configuration file.
    :param stop_event: Event to signal when to stop the simulation.
    """
    try:
        # Construir el comando a ejecutar
        command = [
            "ros2", "launch", "multi_robot_bringup", "multi_robot_simulation.launch.py",
            f"sim_param_file:={config_path}", "navigation:=true"
        ]

        # Ejecutar el comando
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        print("Se ejecuta el gazebo")

        # Esperar hasta que el evento de stop se establezca
        while not stop_event.is_set():
            if process.poll() is not None:  # Verificar si el proceso ha terminado
                break
        

        command_kill_gzclient = [
            "pkill", "gzclient"
        ]

        command_kill_gzserver = [
            "pkill", "gzserver"
        ]

        process_kill_gzclient = subprocess.Popen(command_kill_gzclient, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        process_kill_gzserver = subprocess.Popen(command_kill_gzserver, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        print("Se killea todo")
        # Terminar el proceso si aún está corriendo
        if process.poll() is None:
            process.terminate()
            process.wait()

    except Exception as e:
        print(f"Error al intentar lanzar la simulación: {e}")

def launch_rutina(config_path: str, stop_event: threading.Event):
    """
    Launch a routine with the given configuration file.

    :param config_path: Path to the configuration file.
    :param stop_event: Event to signal when to stop the simulation.
    """
    try:
        # Construir el comando a ejecutar
        command = [
            "ros2", "run", "multi_robot_master_slave", "nav_master_slave.py",
            f"{config_path}"
        ]

        # Ejecutar el comando
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Esperar hasta que el evento de stop se establezca
        while not stop_event.is_set():
            if process.poll() is not None:  # Verificar si el proceso ha terminado
                break
        
        # Terminar el proceso si aún está corriendo
        if process.poll() is None:
            process.terminate()
            process.wait()

    except Exception as e:
        print(f"Error al intentar lanzar la simulación: {e}")

def obtain_robots_to_gz(name: str):
    path = gazebo_dir + "/" + name + ".yaml"
    robots = list()
    with open(path, 'r') as file:
        try:
            data = yaml.safe_load(file)
            robots = data['robots']
            return robots
        except yaml.YAMLError as e:
            return []