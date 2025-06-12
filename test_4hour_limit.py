"""
Test para verificar el límite de 4 horas para usuarios con rol especial
"""
import json
from time_tracker import TimeTracker

def test_4_hour_limit():
    """Test del límite de 4 horas para usuarios con rol especial"""
    tracker = TimeTracker()
    
    # ID de prueba para usuario con rol especial
    test_user_id = 888888888888888888
    test_user_name = "SpecialRoleUser"
    
    print("=== Test del límite de 4 horas (rol especial) ===")
    
    # Simular que el usuario ya tiene 4 horas (240 minutos)
    print(f"1. Agregando 4 horas manualmente para {test_user_name}...")
    tracker.add_minutes(test_user_id, test_user_name, 240)  # 240 minutos = 4 horas
    
    total_time = tracker.get_total_time(test_user_id)
    total_hours = total_time / 3600
    formatted_time = tracker.format_time_human(total_time)
    
    print(f"   Tiempo total: {total_hours} horas ({formatted_time})")
    
    # Verificar si puede iniciar más seguimiento (simulando usuario con rol especial)
    if total_hours >= 4.0:
        print(f"❌ {test_user_name} (rol especial) ya alcanzó el límite de 4 horas")
        print(f"   No se puede iniciar más seguimiento")
        print(f"   Tiempo actual: {formatted_time}")
    else:
        print(f"✅ {test_user_name} (rol especial) puede continuar seguimiento")
    
    # Test con 3.5 horas (debería permitir)
    print(f"\n2. Test con 3.5 horas...")
    tracker.cancel_user_tracking(test_user_id)
    tracker.add_minutes(test_user_id, test_user_name, 210)  # 210 minutos = 3.5 horas
    
    total_time = tracker.get_total_time(test_user_id)
    total_hours = total_time / 3600
    formatted_time = tracker.format_time_human(total_time)
    
    print(f"   Tiempo total: {total_hours} horas ({formatted_time})")
    
    if total_hours >= 4.0:
        print(f"❌ No se puede iniciar más seguimiento")
    else:
        print(f"✅ Se puede iniciar más seguimiento")
    
    # Limpiar datos de prueba
    print(f"\n3. Limpiando datos de prueba...")
    tracker.cancel_user_tracking(test_user_id)
    
    print("✅ Test completado")

if __name__ == "__main__":
    test_4_hour_limit()