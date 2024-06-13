import yaml
import os
import subprocess
from ament_index_python import get_package_share_path
from user_controls.modelo import Modelo
from user_controls.robot import Robot
from user_controls.world import World

def obtain_models_path() -> str:
    model_list_path = ""
    try:
        model_list_path = os.path.join(get_package_share_path('multi_robot_gazebo'), 'config', 'models_register.yaml')
        return model_list_path
    except:
        print("Agregar correctamente el ws al sistema")
        return model_list_path

def obtain_model_list(path: str) -> list:
    model_list = list()
    # path = obtain_models_path()
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
    path = "/home/robot/app_multirobot/app_multi_robot/models_register.yaml"
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

def obtain_robots_path() -> str:
    robot_list_path = str()
    try:
        robot_list_path = os.path.join(get_package_share_path('multi_robot_gazebo'), 'config', 'robots_register.yaml')
        return robot_list_path
    except:
        print("Agregar correctamente el ws al sistema")
        return robot_list_path

def obtain_robot_list(path: str) -> list:
    robot_list = list()
    # path = "/home/robot/app_multirobot/app_multi_robot/robots_register.yaml"
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
    path = "/home/robot/app_multirobot/app_multi_robot/robots_register.yaml"
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

def obtain_worlds_path() -> str:
    pass

def obtain_world_list(path: str) -> list:
    world_list = list()
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
    path = "/home/robot/app_multirobot/app_multi_robot/worlds_register.yaml"
    worlds_old = obtain_world_list(path)
    worlds_old.append(world.to_yaml())
    with open(path, 'w') as file:
        data = {'worlds': worlds_old}
        yaml.dump(data, file)

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

def launch_simulation(config_path: str):
    """
    Launch a ROS2 simulation with the given configuration file.

    :param config_path: Path to the configuration file.
    """
    try:
        # Construir el comando a ejecutar
        command = [
            "ros2", "launch", "multi_robot_bringup", "multi_robot_simulation.launch.py",
            f"sim_param_file:={config_path}", "navigation:=true"
        ]

        # Ejecutar el comando
        result = subprocess.run(command, capture_output=True, text=True)

        # Verificar el resultado
        if result.returncode == 0:
            print("Simulación lanzada exitosamente.")
            print("Salida:")
            print(result.stdout)
        else:
            print("Error al lanzar la simulación.")
            print("Error:")
            print(result.stderr)

    except Exception as e:
        print(f"Error al intentar lanzar la simulación: {e}")