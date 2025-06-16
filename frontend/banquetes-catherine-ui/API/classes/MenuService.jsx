class MenuService{

    async obtenerMenus(){
        try {
            const response = await fetch('http://127.0.0.1:5000/menus');
            if(!response.ok){
                throw new Error('Error en la respuesta: ' + response.status);
            }
            return await response.json();
        } catch (error) {
            console.error("Error al obtener menus:", error);
            throw error;
        }
    }
}

export default MenuService;