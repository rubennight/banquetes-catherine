from model.PlatilloModel import obtener_primeros_platillos
from model.IngredienteModel import obtener_ingredientes_por_platillo
from model.MenuModel import obtener_menus_por_platillo

def obtener_info_carta_service():
    platillos = obtener_primeros_platillos()
    resultado = []

    for p in platillos:
        id_platillo, descripcion, tipo, precio, imagen = p

        ingredientes = obtener_ingredientes_por_platillo(id_platillo)
        menus = obtener_menus_por_platillo(id_platillo)

        resultado.append({
            "idPlatillo": id_platillo,
            "descripcionPlatillo": descripcion,
            "tipoPlatillo": tipo,
            "precio": precio,
            "imagen": imagen,
            "ingredientes": ingredientes,
            "menus": menus
        })

    return resultado