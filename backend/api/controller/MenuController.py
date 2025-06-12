from flask import Blueprint, request, jsonify
from util.Database import obtener_conexion
from service.MenuService import MenuService

menu_controller = Blueprint('menu_controller', __name__)

@menu_controller.route('/menus/obtenerPorId', methods=['GET'])
def obtener_menu_por_id():
    id_menu = request.args.get('idMenu')
    return MenuService.obtener_menu_por_id(id_menu)

@menu_controller.route('/menus/agregar', methods=['POST'])
def agregar_menu():
    data = request.get_json()
    return MenuService.agregar_menu(data)