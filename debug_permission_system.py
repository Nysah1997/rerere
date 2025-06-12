"""
Comprehensive debug script to identify permission system issues
"""
import json
import os

def debug_permission_system():
    """Debug the entire permission verification chain"""
    
    print("=== DEBUGGING PERMISSION SYSTEM ===")
    
    # 1. Check if config.json exists and is readable
    if not os.path.exists('config.json'):
        print("❌ ERROR: config.json no existe")
        return
    
    print("✅ config.json existe")
    
    # 2. Load and examine config
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
        print("✅ config.json cargado correctamente")
        print(f"Config completo: {json.dumps(config, indent=2)}")
    except Exception as e:
        print(f"❌ ERROR cargando config.json: {e}")
        return
    
    # 3. Check mi_tiempo_role_id specifically
    mi_tiempo_role_id = config.get('mi_tiempo_role_id')
    print(f"mi_tiempo_role_id desde config: {mi_tiempo_role_id} (tipo: {type(mi_tiempo_role_id)})")
    
    if mi_tiempo_role_id is None:
        print("❌ ERROR: mi_tiempo_role_id is None - no está configurado")
        return
    
    # 4. Simulate the exact role comparison that happens in Discord
    cyprian_roles = [
        {'name': '@everyone', 'id': 1366550916752216217},
        {'name': '✅ Verificad@', 'id': 1366550916752216221},
        {'name': '»𝓡;𝓢𝓚»𝗥𝗲𝗰𝗹𝘂𝘁𝗮 𝗦𝗲𝗸𝗵𝗺𝗲𝘁 »𝓡;𝓢𝓚»', 'id': 1366550916752216222},
        {'name': '👑︱𝐃𝐞𝐢𝐝𝐚𝐝 𝐒𝐞𝐤𝐡𝐦𝐞𝐭', 'id': 1366550916773318680}
    ]
    
    print(f"\nRoles de Cyprian:")
    for role in cyprian_roles:
        print(f"  - {role['name']} (ID: {role['id']}, tipo: {type(role['id'])})")
    
    # 5. Perform the exact comparison logic
    print(f"\nComparando con mi_tiempo_role_id: {mi_tiempo_role_id}")
    found_match = False
    
    for role in cyprian_roles:
        comparison_result = role['id'] == mi_tiempo_role_id
        print(f"  {role['id']} == {mi_tiempo_role_id}: {comparison_result}")
        if comparison_result:
            print(f"  ✅ MATCH ENCONTRADO: {role['name']}")
            found_match = True
    
    if not found_match:
        print("  ❌ NO SE ENCONTRÓ MATCH")
        
        # Additional debugging - check if it's a string vs int issue
        print(f"\nDebugging adicional:")
        print(f"mi_tiempo_role_id como string: '{str(mi_tiempo_role_id)}'")
        for role in cyprian_roles:
            if str(role['id']) == str(mi_tiempo_role_id):
                print(f"  ✅ MATCH encontrado como STRING: {role['name']}")
                found_match = True
    
    # 6. Test the load_config function behavior
    print(f"\n=== TESTING load_config FUNCTION ===")
    
    def load_config():
        """Simular la función load_config del bot"""
        try:
            with open('config.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError as e:
            print(f"Error decodificando JSON: {e}")
            return {}
    
    config_from_function = load_config()
    role_id_from_function = config_from_function.get('mi_tiempo_role_id')
    print(f"load_config() retorna mi_tiempo_role_id: {role_id_from_function} (tipo: {type(role_id_from_function)})")
    
    # 7. Final verification
    print(f"\n=== RESULTADO FINAL ===")
    if found_match:
        print("✅ El sistema de permisos DEBERÍA funcionar")
    else:
        print("❌ El sistema de permisos NO debería funcionar")
        print("Posibles causas:")
        print("- Configuración incorrecta en config.json")
        print("- Discrepancia en tipos de datos (int vs string)")
        print("- Roles de Discord han cambiado")
        print("- Error en la lógica de comparación")

if __name__ == "__main__":
    debug_permission_system()