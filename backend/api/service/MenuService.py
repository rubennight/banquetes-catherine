from flask import jsonify
from model.MenuModel import obtener_menu_con_detalle, insertar_menu, obtener_menus

class MenuService:

    @staticmethod
    def obtener_menu_por_id(id_menu):
        if not id_menu:
            return jsonify({"error": "Falta el parámetro idMenu", "codigo": 400}), 400
        return obtener_menu_con_detalle(id_menu)

    @staticmethod
    def agregar_menu(data):
        return insertar_menu(data)
    
    @staticmethod
    def obtener_menus():
        return obtener_menus()