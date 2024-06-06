import funciones
from user_controls.robot import Robot
from user_controls.modelo import Modelo

print(funciones.obtain_robot_list("/home/robot/app_multirobot/app_multi_robot/robots_register.yaml"))

modelo: Modelo = funciones.obtain_model_list("/home/robot/app_multirobot/app_multi_robot/models_register.yaml")[0]

new_robot = Robot("pepito2", modelo, "Differential", True)

funciones.add_robot(new_robot)