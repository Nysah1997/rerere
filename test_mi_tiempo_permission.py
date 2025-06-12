"""
Test script to verify the mi_tiempo permission system
"""
import json

def test_permission_system():
    """Test the permission verification logic"""
    
    # Load config
    with open('config.json', 'r') as f:
        config = json.load(f)
    
    mi_tiempo_role_id = config.get('mi_tiempo_role_id')
    print(f"Configured role ID: {mi_tiempo_role_id}")
    print(f"Type: {type(mi_tiempo_role_id)}")
    
    # Simulate the roles from debug output
    user_roles = [
        {'name': '@everyone', 'id': 1366550916752216217},
        {'name': '✅ Verificad@', 'id': 1366550916752216221},
        {'name': '»𝓡;𝓢𝓚»𝗥𝗲𝗰𝗹𝘂𝘁𝗮 𝗦𝗲𝗸𝗵𝗺𝗲𝘁 »𝓡;𝓢𝓚»', 'id': 1366550916752216222},
        {'name': '👑︱𝐃𝐞𝐢𝐝𝐚𝐝 𝐒𝐞𝐤𝐡𝐦𝐞𝐭', 'id': 1366550916773318680}
    ]
    
    print("\nUser roles:")
    for role in user_roles:
        print(f"  {role['name']} (ID: {role['id']}, type: {type(role['id'])})")
    
    print(f"\nChecking for match with required ID: {mi_tiempo_role_id}")
    
    for role in user_roles:
        print(f"Comparing {role['id']} == {mi_tiempo_role_id}: {role['id'] == mi_tiempo_role_id}")
        if role['id'] == mi_tiempo_role_id:
            print(f"MATCH FOUND: {role['name']}")
            return True
    
    print("NO MATCH FOUND")
    return False

if __name__ == "__main__":
    result = test_permission_system()
    print(f"\nResult: {'PASS' if result else 'FAIL'}")